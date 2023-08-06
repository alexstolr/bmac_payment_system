from datetime import datetime


class SubscriptionData:
    def __init__(self, expiration_date, price, create_date, update_date, is_valid):
        self.expiration_date = expiration_date
        self.price = price
        self.create_date = create_date
        self.update_date = update_date
        self.is_valid: bool = is_valid

    def is_subscription_valid(self, date_now: datetime):
        # should pass date_now = datetime.now(). passing it to avoid re calculation every time.
        return self.expiration_date > date_now
