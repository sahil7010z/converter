from flask import Flask, render_template, request
import requests

app = Flask(__name__)

EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/"

# Include currency symbols
CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥",
    "AUD": "A$", "CAD": "C$", "CHF": "CHF", "CNY": "¥", "HKD": "HK$",
    "NZD": "NZ$", "BRL": "R$", "ZAR": "R", "SGD": "S$", "KRW": "₩",
    "MXN": "$", "SEK": "kr", "NOK": "kr", "DKK": "kr"
}

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
                symbol = CURRENCY_SYMBOLS.get(to_currency, '')
            else:
                result = "Currency not supported."
        except Exception as e:
            result = "Error fetching exchange rate."
            print(e)

    return render_template('index.html', result=result, symbol=symbol)

if __name__ == '__main__':
    app.run(debug=True)
