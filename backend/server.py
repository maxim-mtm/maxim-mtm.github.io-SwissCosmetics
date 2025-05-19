@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()

    if not data or 'cart' not in data:
        print("DEBUG: Invalid or missing cart:", data)
        return jsonify({'error': 'Missing cart'}), 400

    try:
        line_items = [{
            'price': item['id'],
            'quantity': item['quantity']
        } for item in data['cart']]

        print("DEBUG: Line items to Stripe:", line_items)

        session = stripe.checkout.Session.create(
            payment_method_types=['card', 'twint', 'klarna', 'giropay'],
            mode='payment',
            line_items=line_items,
            success_url='https://maxim-mtm.github.io/swiss-cosmetics/success',
            cancel_url='https://maxim-mtm.github.io/swiss-cosmetics/cancel'
        )
        return jsonify({'url': session.url})
    except Exception as e:
        print("DEBUG: Stripe error:", str(e))
        return jsonify({'error': str(e)}), 400
