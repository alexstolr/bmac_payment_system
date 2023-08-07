from typing import List

import requests

import constants
import env_parser
from datetime import datetime, timedelta

from BmacDonor import BmacDonor, BmacDonors
from BmacException import BmacException
from SubscriptionData import SubscriptionData
from UserData import UserData

donors_endpoint_url = "https://developers.buymeacoffee.com/api/v1/supporters?page=1"
BMAC_API_KEY = env_parser.get_env_var('BUY_ME_A_COFFEE_API_KEY')
headers = {"Authorization": f"Bearer {BMAC_API_KEY}"}

user_data: dict[int, UserData] = {}
valid_subscriptions: set = set()


def get_donors() -> List[BmacDonor]:
    donors: List[BmacDonor] = []
    next_donors_endpoint_url = donors_endpoint_url
    date_now = datetime.now()
    while next_donors_endpoint_url is not None:
        response = requests.get(next_donors_endpoint_url, headers=headers)
        if response.status_code == 200:
            supporters = response.json()
            if 'error' in supporters and supporters['error'] == 'No supporters':
                break
            next_donors_endpoint_url = supporters['next_page_url']
            bmac_donors = BmacDonors(**supporters)
            for donor in bmac_donors.data:
                if donor.support_note is None:
                    continue
                user_id = donor.support_note # Can make this structured data.
                existing_donor = user_data.get(user_id)
                if existing_donor is not None and existing_donor.subscription_data is not None and existing_donor.subscription_data.update_date == donor.support_updated_on:
                    next_donors_endpoint_url = None
                    continue
                donor_date: datetime = datetime.strptime(donor.support_updated_on, '%Y-%m-%d %H:%M:%S')
                donation_expiration_date: datetime = donor_date + timedelta(days=constants.SUBSCRIPTION_DAYS)
                donor.expiration_date_internal = donation_expiration_date
                if donor.is_subscription_valid(date_now) and not donor.is_refunded:
                    donor.expiration_date_internal = donation_expiration_date
                    donor.user_id_internal = user_id
                    if existing_donor is not None:
                        print(
                            f"New customer paid {donor.support_coffee_price}$ with expiration of {donor.expiration_date_internal}!")
                    donors.append(donor)
                else:
                    next_donors_endpoint_url = None
        else:
            raise BmacException(f"Failed to get buy me a coffee donors. error {response.status_code}")
    return donors


def init_subscriptions():
    date_now = datetime.now()
    donors: List[BmacDonor] = get_donors()
    for donor in donors:
        if donor.is_subscription_valid(date_now):
            current_user_data = user_data.get(donor.user_id_internal)
            subscription_data = SubscriptionData(
                donor.expiration_date_internal,
                donor.support_coffee_price,
                donor.support_created_on,
                donor.support_updated_on,
                is_valid=True
            )
            if current_user_data is None:
                user_data[donor.user_id_internal] = UserData(
                    subscription_data=subscription_data)
            else:
                current_user_data.subscription_data = subscription_data
            user_id = donor.support_note
            valid_subscriptions.add(user_id)


def clear_expired_subscribers():
    date_now = datetime.now()
    for subscribed_donor in valid_subscriptions:
        current_user_data: UserData = user_data.get(subscribed_donor)
        known_expiration_date = current_user_data.subscription_data.expiration_date
        if known_expiration_date < date_now:
            valid_subscriptions.remove(subscribed_donor)
            current_user_data.subscription_data.is_valid = False


def got_donors_printable(donors: List[BmacDonor]) -> str:
    printable = ""
    for donor in donors:
        printable += f"{donor.to_string()} \n"
    return printable
