from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load country-currency mappings
with open("country_currency.json", "r", encoding="utf-8") as cc_file:
    country_currency = json.load(cc_file)

# Load transfer fee data
with open("transfer_fees.json", "r", encoding="utf-8") as fee_file:
    transfer_fees = json.load(fee_file)

# ExchangeRate API key
EXCHANGE_RATE_API_KEY = "e54e536172dfb19b340c6fea"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json()
        print("Received request:", json.dumps(req, indent=2))
        intent = req["queryResult"]["intent"]["displayName"]

        if intent == "currency_converter":
            return handle_currency_converter(req)
        elif intent == "get_country_currency":
            return handle_get_country_currency(req)
        elif intent == "get_transfer_info":
            return handle_get_transfer_info(req)
        else:
            return jsonify({"fulfillmentText": "I'm not sure how to help with that."})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"fulfillmentText": f"An error occurred: {str(e)}"})

# Intent: Convert Currency
def handle_currency_converter(req):
    parameters = req["queryResult"]["parameters"]
    from_currency = parameters["unit-currency"][0]["currency"]
    amount = float(parameters["unit-currency"][0]["amount"])
    to_currency = parameters["currency-name"][0] if isinstance(parameters["currency-name"], list) else parameters["currency-name"]

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()

    if data["result"] == "success":
        rate = data["conversion_rate"]
        converted_amount = round(rate * amount, 2)
        return jsonify({
            "fulfillmentText": f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."
        })
    else:
        return jsonify({
            "fulfillmentText": "Sorry, I couldn't fetch the exchange rate right now."
        })

# Intent: Get Country Currency
def handle_get_country_currency(req):
        parameters = req["queryResult"]["parameters"]
        countries = parameters.get("geo-country", [])

        country = countries[0] if isinstance(countries, list) and countries else countries
        original_country = country
        country = country.strip().lower()

        print(f"Looking for country: '{country}'")

        currency_info = country_currency.get(country)

        if currency_info:
            return jsonify({
                "fulfillmentText": f"The currency of {original_country} is {currency_info}."
            })
        else:
            return jsonify({
                "fulfillmentText": f"Sorry, I couldn't find the currency information for {original_country}."
                           })

            return jsonify({
                      "fulfillmentText": "Sorry, I couldn't process your request."
                })

# Intent: Get Transfer Info
def handle_get_transfer_info(req):

    parameters = req["queryResult"]["parameters"]

    # Fix: Use correct parameter keys
    source_currency = parameters.get("currency-name", "").upper()
    target_currency = parameters.get("currency-name1", "").upper()

    pair_key = f"{source_currency} to {target_currency}"
    print(f"Looking for transfer fee for: {pair_key}")

    fee = transfer_fees.get(pair_key)

    if fee:
        return jsonify({
            "fulfillmentText": f"The transfer fee from {source_currency} to {target_currency} is {fee} USD."
        })
    else:
        return jsonify({
            "fulfillmentText": f"Sorry, I couldn't find transfer fee details for {source_currency} to {target_currency}."
        })


if __name__ == "__main__":
    app.run(debug=True)
