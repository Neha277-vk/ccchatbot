from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load country-currency mappings
with open("country_currency.json", "r", encoding="utf-8") as cc_file:
    country_currency = json.load(cc_file)

# Load transfer fee data
with open("transfer_fees.json", "r", encoding="utf-8") as fee_file:
    raw_fees = json.load(fee_file)
    transfer_fees = {k.upper(): v for k, v in raw_fees.items()}

# ExchangeRate API key
EXCHANGE_RATE_API_KEY = "e54e536172dfb19b340c6fea"
NEWS_API_KEY = "1082e2b1f6d7415d80cb322101bdb0dc"


def get_cleaned_param(params, key, transform=None):
    value = params.get(key)

    # If it's a list, get the first non-empty element
    if isinstance(value, list):
        value = value[0] if value else None

    # If still None or empty
    if not value:
        return None

    # Apply transformation like .upper(), .lower(), .title()
    if transform == "upper":
        return value.upper()
    elif transform == "lower":
        return value.lower()
    elif transform == "title":
        return value.title()

    return value
def get_forex_news(query="forex OR currency OR exchange rate", language="en"):
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={query}&language={language}&category=business"

    response = requests.get(url)
    data = response.json()

    print("🔍 Raw News API Response:", json.dumps(data, indent=2))  # Debugging line

    if data.get("status") != "success":
        raise Exception(f"News API failed: {data.get('message', 'Unknown error')}")

    articles = data.get("results", [])[:3]  # Top 3 headlines
    if not articles:
        return "Sorry, no recent Forex news was found."

    news_list = [f"🔹 {article['title']} ({article['source_id']})" for article in articles]
    return "\n\n".join(news_list)

def handle_forex_news(req):
    params = req["queryResult"]["parameters"]
    currency = get_cleaned_param(params, "currency-name", "upper")

    try:
        query = f"{currency} forex OR exchange rate" if currency else "forex OR currency OR exchange rate"
        news_text = get_forex_news(query=query)

        return jsonify({
            "fulfillmentText": f"📰 Here are the latest news headlines about {currency if currency else 'Forex'}:\n\n{news_text}"
        })
    except Exception as e:
        print("❌ News fetch error:", e)
        return jsonify({
            "fulfillmentText": "⚠️ Sorry, I couldn’t fetch news at the moment. Please try again later."
        })



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
        elif intent == "get_forex_news":
              return handle_forex_news(req)
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

    # Extract normally
    source_currency = get_cleaned_param(parameters, "currency-name", "upper")
    target_currency = get_cleaned_param(parameters, "currency-name1", "upper")

    # Special case: both currencies are in "currency-name" (e.g. ["USD", "INR"])
    currency_list = parameters.get("currency-name", [])
    if isinstance(currency_list, list) and len(currency_list) == 2:
        source_currency = currency_list[0].upper()
        target_currency = currency_list[1].upper()

    print("Cleaned source:", source_currency)
    print("Cleaned target:", target_currency)

    if not source_currency or not target_currency:
        return jsonify({
            "fulfillmentText": "Please provide both source and target currencies for the transfer."
        })

    pair_key = f"{source_currency} to {target_currency}".upper()
    print("Looking for fee for:", pair_key)

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
