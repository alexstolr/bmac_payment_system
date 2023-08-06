from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BmacDonor(BaseModel):
    """
    @:param expiration_date_internal internally calculated subscription expiration date
    """
    support_id: int
    support_note: Optional[str]
    support_coffees: int
    transaction_id: str
    support_visibility: int
    support_created_on: str
    support_updated_on: str
    transfer_id: Optional[str]
    supporter_name: Optional[str]
    support_coffee_price: float
    support_email: Optional[str]
    is_refunded: Optional[str]
    support_currency: str
    # support_note_pinned: int
    referer: Optional[str]
    country: Optional[str]
    payer_email: str
    payment_platform: str
    payer_name: str
    expiration_date_internal: Optional[datetime] = None
    user_id_internal: Optional[int] = None

    def is_subscription_valid(self, date_now: datetime):
        # should pass date_now = datetime.now(). passing it to avoid re calculation every time.
        return self.expiration_date_internal > date_now

    def to_string(self):
        return f"transaction id: {self.transaction_id} support note: {self.support_note} payer email: {self.payer_email}"


class BmacDonors(BaseModel):
    current_page: int
    data: List[BmacDonor]
    first_page_url: str
    # from: int reserved word. I'll add manually if required.
    last_page: int
    last_page_url: str
    next_page_url: Optional[str]
    path: str
    per_page: int
    prev_page_url: Optional[str]
    to: int
    total: int
