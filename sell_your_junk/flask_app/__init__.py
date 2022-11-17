import stripe
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "secret sales"

# stripe API addition is in progress
stripe.api_key = "sk_test_51M4IgCDNx1qFNcN0A8tlDps2ZgChZvVw81D6DYBmaKNcupRDqONGvnYGQPSTDs2hRoycj4Eyp01whLRAegLxpBLD00trf42JXi"

stripe.PaymentIntent.create(amount=500, currency="gbp", payment_method="pm_card_visa")