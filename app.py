from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    symbol = ''
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        try:
            response = requests.get(EXCHANGE_URL + from_currency)
            data = response.json()
            rate = data['rates'].get(to_currency)
            if rate:
                result = round(rate * amount, 2)
                symbols = {
                    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥", 
                    "CAD": "C$", "AUD": "A$", "CNY": "¥", "RUB": "₽", "KRW": "₩", 
                    "BRL": "R$", "ZAR": "R"
                }
                symbol = symbols.get(to_currency, '')
            else:
                result = "Currency not supported."
        except:
            result = "Error fetching exchange rate."

    return render_template('index.html', result=result, symbol=symbol)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
