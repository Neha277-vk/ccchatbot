from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your ExchangeRate API Key
API_KEY = "e54e536172dfb19b340c6fea"  # Replace with your actual API key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# Country-to-Currency Mapping (Case Insensitive)
country_currency = {
    "afghanistan": "Afghan Afghani (AFN)",
    "albania": "Albanian Lek (ALL)",
    "algeria": "Algerian Dinar (DZD)",
    "andorra": "Euro (EUR)",
    "angola": "Angolan Kwanza (AOA)",
    "argentina": "Argentine Peso (ARS)",
    "armenia": "Armenian Dram (AMD)",
    "australia": "Australian Dollar (AUD)",
    "austria": "Euro (EUR)",
    "azerbaijan": "Azerbaijani Manat (AZN)",
    "bangladesh": "Bangladeshi Taka (BDT)",
    "brazil": "Brazilian Real (BRL)",
    "canada": "Canadian Dollar (CAD)",
    "china": "Chinese Yuan (CNY)",
    "denmark": "Danish Krone (DKK)",
    "egypt": "Egyptian Pound (EGP)",
    "france": "Euro (EUR)",
    "germany": "Euro (EUR)",
    "india": "Indian Rupee (INR)",
    "indonesia": "Indonesian Rupiah (IDR)",
    "iran": "Iranian Rial (IRR)",
    "iraq": "Iraqi Dinar (IQD)",
    "israel": "Israeli New Shekel (ILS)",
    "italy": "Euro (EUR)",
    "japan": "Japanese Yen (JPY)",
    "kenya": "Kenyan Shilling (KES)",
    "south korea": "South Korean Won (KRW)",
    "mexico": "Mexican Peso (MXN)",
    "nepal": "Nepalese Rupee (NPR)",
    "netherlands": "Euro (EUR)",
    "norway": "Norwegian Krone (NOK)",
    "pakistan": "Pakistani Rupee (PKR)",
    "philippines": "Philippine Peso (PHP)",
    "poland": "Polish Zloty (PLN)",
    "portugal": "Euro (EUR)",
    "qatar": "Qatari Riyal (QAR)",
    "russia": "Russian Ruble (RUB)",
    "saudi arabia": "Saudi Riyal (SAR)",
    "south africa": "South African Rand (ZAR)",
    "spain": "Euro (EUR)",
    "sweden": "Swedish Krona (SEK)",
    "switzerland": "Swiss Franc (CHF)",
    "thailand": "Thai Baht (THB)",
    "turkey": "Turkish Lira (TRY)",
    "united arab emirates": "UAE Dirham (AED)",
    "united kingdom": "Pound Sterling (GBP)",
    "united states": "US Dollar (USD)",
    "vietnam": "Vietnamese Dong (VND)"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        intent_name = req['queryResult']['intent']['displayName']
        print("Received Intent:", intent_name)

        # 🔹 Intent 1: Currency Conversion
        if intent_name in ["convert_currency", "currency_converter"]:
            parameters = req['queryResult']['parameters']
            unit_currency = parameters.get('unit-currency')
            to_currency = parameters.get('currency-name')

            if not unit_currency or 'currency' not in unit_currency or 'amount' not in unit_currency:
                return jsonify({'fulfillmentText': "Invalid input. Please provide a valid currency and amount."})

            from_currency = unit_currency['currency'].upper()
            amount = unit_currency['amount']
            to_currency = to_currency.upper()

            print(f"Converting {amount} {from_currency} to {to_currency}")

            response = requests.get(BASE_URL + from_currency)
            if response.status_code != 200:
                print("API Error:", response.text)
                return jsonify({'fulfillmentText': "Failed to fetch exchange rates. Please try again later."})

            exchange_data = response.json()
            print("API Response:", exchange_data)

            if not exchange_data or 'conversion_rates' not in exchange_data:
                return jsonify({'fulfillmentText': "Failed to fetch valid exchange rates. Please try again later."})

            rate = exchange_data['conversion_rates'].get(to_currency)
            if rate is None:
                return jsonify({'fulfillmentText': f"Exchange rate for {to_currency} is not available."})

            converted_amount = amount * rate
            result_text = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}."
            return jsonify({'fulfillmentText': result_text})

        # 🔹 Intent 2: Get Country Currency Name
        elif intent_name == "get_country_currency":
            country_name = req['queryResult']['parameters'].get('geo-country', '').strip().lower()

            # Handle Common Misspellings
            country_name = country_name.replace("maxico", "mexico").replace("south corea", "south korea")

            currency = country_currency.get(country_name, None)

            if currency:
                return jsonify({'fulfillmentText': f"The currency of {country_name.title()} is {currency}."})
            else:
                return jsonify({'fulfillmentText': "Sorry, I don't have currency information for this country."})

        else:
            return jsonify({'fulfillmentText': "Intent not recognized by webhook."})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'fulfillmentText': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

