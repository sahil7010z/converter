from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API endpoint and your key if needed
EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
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
            else:
                result = "Currency not supported."
        except:
            result = "Error fetching exchange rate."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
