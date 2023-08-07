# bmac_payment_system
Buy me a coffee based payment and subscription system

# Guide
Provide the user with the 
1. link to your Buy Me A Coffe page (same as you set in the BMAC_LINK env var).
2. A unique user id, which the user should write in the optional note field.

call ```bmac_client.init_subscriptions()``` to fetch all the new payments. the user id will be extracted and stored in 
user_data and valid_subscriptions. Use these to implement your custom logic.

call ```bmac_client.clear_expired_subscribers()``` to expire the subscriber.

# Environment variables
add a ```.env``` file
```commandline
BUY_ME_A_COFFEE_API_KEY=YOUR_API_KEY
BMAC_LINK=https://www.buymeacoffee.com/YOUR_PAGE
```

# Install dependencies
```commandline
pip install pipreqs
pipreqs --force .
pip install -r requirements.txt
```

# Support
Add a star :)

