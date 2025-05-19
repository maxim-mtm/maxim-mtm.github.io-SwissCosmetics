from flask import Flask, request, jsonify
import stripe
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows frontend to make requests

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    items = data.get('cart', [])

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card', 'twint', 'klarna', 'giropay'],
            mode='payment',
            line_items=[{
                'price': item['id'],
                'quantity': item['quantity']
            } for item in items],
            success_url='https://maxim-mtm.github.io/swiss-cosmetics/success',
            cancel_url='https://maxim-mtm.github.io/swiss-cosmetics/cancel'
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/success')
def success():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Payment Successful</title>
      <style>
        body {
          margin: 0;
          font-family: 'Segoe UI', sans-serif;
          background-color: #121212;
          color: white;
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          animation: fadeIn 1s ease;
        }
        h1 {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          animation: slideUp 1s ease;
        }
        p {
          color: #ccc;
          margin-bottom: 2rem;
          animation: slideUp 1.2s ease;
        }
        a {
          background: #fff;
          color: #121212;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          font-weight: bold;
          text-decoration: none;
          transition: 0.3s ease;
          animation: slideUp 1.4s ease;
        }
        a:hover {
          background: #ccc;
          transform: scale(1.05);
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
      </style>
    </head>
    <body>
      <h1>Payment Successful!</h1>
      <p>Thank you for your purchase.</p>
      <a href="https://maxim-mtm.github.io/swiss-cosmetics/shop.html">Continue Shopping</a>
    </body>
    </html>
    """

@app.route('/cancel')
def cancel():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Payment Cancelled</title>
      <style>
        body {
          margin: 0;
          font-family: 'Segoe UI', sans-serif;
          background-color: #121212;
          color: white;
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          animation: fadeIn 1s ease;
        }
        h1 {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          animation: slideUp 1s ease;
        }
        p {
          color: #ccc;
          margin-bottom: 2rem;
          animation: slideUp 1.2s ease;
        }
        a {
          background: #fff;
          color: #121212;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          font-weight: bold;
          text-decoration: none;
          transition: 0.3s ease;
          animation: slideUp 1.4s ease;
        }
        a:hover {
          background: #ccc;
          transform: scale(1.05);
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
      </style>
    </head>
    <body>
      <h1>Payment Cancelled</h1>
      <p>Your transaction was not completed.</p>
      <a href="https://maxim-mtm.github.io/swiss-cosmetics/shop.html">Return to Shop</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=4242)
