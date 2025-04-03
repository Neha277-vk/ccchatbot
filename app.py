'''from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your actual API key from ExchangeRate-API
API_KEY = ' e54e536172dfb19b340c6fea'
API_URL = 'https://v6.exchangeratesapi.io/latest'

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    print(json.dumps(data, indent=4))  # Debug: Print incoming JSON to check structure

    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    try:
        # Extract required parameters from the request
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        amount = data.get('amount')

        # Validate input
        if not all([source_currency, target_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Fetch conversion rate
        conversion_rate = get_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({'error': 'Invalid currency codes'}), 400

        # Perform currency conversion
        converted_amount = amount * conversion_rate

        # Return the result as JSON
        return jsonify({
            'original_amount': amount,
            'source_currency': source_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': target_currency,
            'conversion_rate': conversion_rate
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def get_conversion_rate(source_currency, target_currency):
    """Fetch conversion rate from the API."""
    params = {
        'base': source_currency,
        'symbols': target_currency,
        'apikey': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        rate = data.get('rates', {}).get(target_currency)
        return rate
    except:
        return None

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__,static_folder='static')

# Replace 'YOUR_API_KEY' with your actual API key from ExchangeRate-API
API_KEY = 'e54e536172dfb19b340c6fea'
API_URL = 'https://v6.exchangeratesapi.io/latest'

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    print(json.dumps(data, indent=4))  # Debug: Print incoming JSON to check structure

    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    try:
        # Extract required parameters from the request
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        amount = data.get('amount')

        # Validate input
        if not all([source_currency, target_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Fetch conversion rate
        conversion_rate = get_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({'error': 'Invalid currency codes'}), 400

        # Perform currency conversion
        converted_amount = amount * conversion_rate

        # Return the result as JSON
        return jsonify({
            'original_amount': amount,
            'source_currency': source_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': target_currency,
            'conversion_rate': conversion_rate
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def get_conversion_rate(source_currency, target_currency):
    """Fetch conversion rate from the API."""
    params = {
        'base': source_currency,
        'symbols': target_currency,
        'apikey': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        rate = data.get('rates', {}).get(target_currency)
        return rate
    except:
        return None

# List all available routes (for debugging)
@app.before_request
def list_routes():
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.endpoint}, URL: {rule.rule}")

if __name__ == '__main__':
    app.run(debug=True)'''

'''from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your actual API key for currency conversion
API_KEY = 'e54e536172dfb19b340c6fea'
API_URL = 'https://api.exchangerate-api.com/v4/latest/'

# Webhook endpoint for Dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print(req)  # Debugging: Check the incoming request

    # Check if it's the right intent
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')

    if intent == 'CurrencyConversion':
        return handle_conversion(req)
    else:
        return jsonify({'fulfillmentText': 'I can help with currency conversion.'})

# Handle currency conversion
def handle_conversion(req):
    params = req.get('queryResult', {}).get('parameters', {})
    amount = params.get('amount')
    source_currency = params.get('source_currency')
    target_currency = params.get('target_currency')

    if not amount or not source_currency or not target_currency:
        return jsonify({'fulfillmentText': 'Please provide valid currency information.'})

    conversion_rate = get_conversion_rate(source_currency, target_currency)

    if conversion_rate:
        converted_amount = round(amount * conversion_rate, 2)
        return jsonify({
            'fulfillmentText': f'{amount} {source_currency} is equal to {converted_amount} {target_currency} (Rate: {conversion_rate})'
        })
    else:
        return jsonify({'fulfillmentText': 'Invalid currency codes or API error.'})

# Fetch conversion rate from API
def get_conversion_rate(source_currency, target_currency):
    try:
        response = requests.get(f'{API_URL}{source_currency}')
        data = response.json()
        return data.get('rates', {}).get(target_currency)
    except Exception as e:
        print(f"Error fetching conversion rate: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__, static_folder='static')

# Replace 'YOUR_API_KEY' with your actual API key from ExchangeRate-API
API_KEY = 'e54e536172dfb19b340c6fea'
API_URL = 'https://v6.exchangeratesapi.io/latest'

# Root Route to Handle POST Requests
@app.route('/', methods=['POST'])
def root():
    return jsonify({'error': 'This endpoint is not supported. Please use /convert.'}), 404

# Currency Conversion Route
@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    print(json.dumps(data, indent=4))  # Debug: Print incoming JSON to check structure

    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    try:
        # Extract required parameters from the request
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        amount = data.get('amount')

        # Validate input
        if not all([source_currency, target_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Fetch conversion rate
        conversion_rate = get_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({'error': 'Invalid currency codes'}), 400

        # Perform currency conversion
        converted_amount = amount * conversion_rate

        # Return the result as JSON
        return jsonify({
            'original_amount': amount,
            'source_currency': source_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': target_currency,
            'conversion_rate': conversion_rate
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Function to Fetch Conversion Rate from API
def get_conversion_rate(source_currency, target_currency):
    """Fetch conversion rate from the API."""
    params = {
        'base': source_currency,
        'symbols': target_currency,
        'apikey': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        rate = data.get('rates', {}).get(target_currency)
        return rate
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None

# List all available routes (for debugging)
@app.before_request
def list_routes():
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.endpoint}, URL: {rule.rule}")

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)'''


'''from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__, static_folder='static')

# Replace with your actual API key from ExchangeRate-API
API_KEY = 'e54e536172dfb19b340c6fea'
API_URL = 'https://v6.exchangeratesapi.io/latest'

# ✅ Debugging: Log all incoming requests
@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.url}")

# ✅ Root Route - Handle GET and POST Requests
@app.route('/CONVERT', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to the Currency Converter API!'})
    elif request.method == 'POST':
        return jsonify({'error': 'This endpoint is not supported. Please use /convert.'}), 404


# ✅ Currency Conversion Route
@app.route('/convert', methods=['POST'])
def convert_currency():
    print("Handling /convert request...")  # Debugging log

    data = request.get_json()
    print(f"Received data: {json.dumps(data, indent=4)}")  # Debug: Print incoming JSON

    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    try:
        # Extract required parameters
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        amount = data.get('amount')

        # Validate input
        if not all([source_currency, target_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Fetch conversion rate
        conversion_rate = get_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({'error': 'Invalid currency codes'}), 400

        # Perform currency conversion
        converted_amount = amount * conversion_rate

        # Return the result as JSON
        return jsonify({
            'original_amount': amount,
            'source_currency': source_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': target_currency,
            'conversion_rate': conversion_rate
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# ✅ Function to Fetch Conversion Rate from API
def get_conversion_rate(source_currency, target_currency):
    params = {
        'base': source_currency,
        'symbols': target_currency,
        'apikey': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        rate = data.get('rates', {}).get(target_currency)
        return rate
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None

# ✅ List all available routes (for debugging)
@app.before_request
def list_routes():
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.endpoint}, URL: {rule.rule}")




# ✅ Run the Flask App (listening on all interfaces)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__, static_folder='static')

# Replace with your actual API key from ExchangeRate-API
API_KEY = 'e54e536172dfb19b340c6fea'
API_URL = 'https://v6.exchangeratesapi.io/latest'

# Log incoming requests for debugging
@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Request path: {request.path}")

# Root route
@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to the Currency Converter API!'})

# Convert Currency route
@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    try:
        # Extract required parameters from the request
        source_currency = data.get('source_currency')
        target_currency = data.get('target_currency')
        amount = data.get('amount')

        # Validate input
        if not all([source_currency, target_currency, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Fetch conversion rate
        conversion_rate = get_conversion_rate(source_currency, target_currency)
        if conversion_rate is None:
            return jsonify({'error': 'Invalid currency codes'}), 400

        # Perform currency conversion
        converted_amount = amount * conversion_rate

        return jsonify({
            'original_amount': amount,
            'source_currency': source_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': target_currency,
            'conversion_rate': conversion_rate
        })

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Function to fetch conversion rate from API
def get_conversion_rate(source_currency, target_currency):
    params = {
        'base': source_currency,
        'symbols': target_currency,
        'apikey': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        rate = data.get('rates', {}).get(target_currency)
        return rate
    except requests.exceptions.RequestException as e:
        return None

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Replace with your actual API key for ExchangeRate-API
API_KEY = "e54e536172dfb19b340c6fea"
BASE_URL = " https://v6.exchangerate-api.com/v6/e54e536172dfb19b340c6fea/latest/USD"


@app.route("/convert", methods=["POST"])
def convert_currency():
    try:
        req = request.get_json()
        logging.debug(f"Received request: {req}")

        # Extract parameters from Dialogflow request
        parameters = req.get("queryResult", {}).get("parameters", {})
        unit_currency = parameters.get("unit-currency", [{}])[0]
        target_currency = parameters.get("currency-name", "")

        amount = unit_currency.get("amount", 0)
        source_currency = unit_currency.get("currency", "")

        if not source_currency or not target_currency:
            return jsonify({"fulfillmentText": "Invalid currency conversion request."})

        # Fetch exchange rate
        response = requests.get(BASE_URL + source_currency)
        if response.status_code != 200:
            return jsonify({"fulfillmentText": "Error fetching exchange rate."})

        data = response.json()
        rates = data.get("conversion_rates", {})
        conversion_rate = rates.get(target_currency.upper(), None)

        if not conversion_rate:
            return jsonify({"fulfillmentText": f"Cannot find exchange rate for {target_currency}."})

        converted_amount = amount * conversion_rate
        result_text = f"{amount} {source_currency} is approximately {converted_amount:.2f} {target_currency}."

        return jsonify({"fulfillmentText": result_text})

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"fulfillmentText": "An error occurred while processing your request."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

EXCHANGE_RATE_API_KEY = "YOUR_EXCHANGE_RATE_API_KEY"
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"


def get_exchange_rate(base_currency, target_currency):
    url = EXCHANGE_RATE_API_URL.format(EXCHANGE_RATE_API_KEY, base_currency)
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and "conversion_rates" in data:
        return data["conversion_rates"].get(target_currency, None)
    return None


@app.route("/convert", methods=["POST"])
def convert_currency():
    req = request.get_json()
    parameters = req.get("queryResult", {}).get("parameters", {})

    unit_currency = parameters.get("unit-currency", [{}])[0]
    amount = unit_currency.get("amount", 1.0)
    base_currency = unit_currency.get("currency", "USD")
    target_currency = parameters.get("currency-name", "INR")

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        return jsonify({"fulfillmentText": "Sorry, I couldn't fetch the exchange rate."})

    converted_amount = amount * exchange_rate
    response_text = f"{amount} {base_currency} is approximately {converted_amount:.2f} {target_currency}."

    return jsonify({"fulfillmentText": response_text})


if __name__ == "__main__":
    app.run(debug=True)'''

'''m flask import Flask, request, jsonify
import requests

app = Flask(__name__)

EXCHANGE_RATE_API_KEY = "e54e536172dfb19b340c6fea"
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/e54e536172dfb19b340c6fea/latest/USD"


def get_exchange_rate(base_currency, target_currency):
    url = EXCHANGE_RATE_API_URL.format(EXCHANGE_RATE_API_KEY, base_currency)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()
        if "conversion_rates" in data:
            return data["conversion_rates"].get(target_currency, None)
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Failed to parse JSON response from API")
    return None


@app.route("/convert", methods=["POST"])
def convert_currency():
    req = request.get_json()
    parameters = req.get("queryResult", {}).get("parameters", {})

    unit_currency = parameters.get("unit-currency", [{}])[0]
    amount = unit_currency.get("amount", 1.0)
    base_currency = unit_currency.get("currency", "USD")
    target_currency = parameters.get("currency-name", "INR")

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate is None:
        return jsonify({"fulfillmentText": "Sorry, I couldn't fetch the exchange rate at this moment."})

    converted_amount = amount * exchange_rate
    response_text = f"{amount} {base_currency} is approximately {converted_amount:.2f} {target_currency}."

    return jsonify({"fulfillmentText": response_text})


if __name__ == "__main__":
    app.run(debug=True)'''

'''ort requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Use a real API to fetch exchange rates
API_KEY = "e54e536172dfb19b340c6fea"
EXCHANGE_API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"


@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        # Parse JSON request
        data = request.get_json()

        # Extract parameters
        amount = data["queryResult"]["parameters"]["unit-currency"][0]["amount"]
        from_currency = data["queryResult"]["parameters"]["unit-currency"][0]["currency"]
        to_currency = data["queryResult"]["parameters"]["currency-name"]

        # Fetch real-time exchange rate
        response = requests.get(f"{EXCHANGE_API_URL}{from_currency}")
        exchange_data = response.json()

        if "conversion_rates" not in exchange_data:
            return jsonify({"fulfillmentText": "Error fetching exchange rates."})

        conversion_rate = exchange_data["conversion_rates"].get(to_currency)
        if not conversion_rate:
            return jsonify({"fulfillmentText": f"Conversion rate for {to_currency} not available."})

        # Perform conversion
        converted_amount = amount * conversion_rate

        # Response message
        fulfillment_text = f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}."

        return jsonify({"fulfillmentText": fulfillment_text})

    except Exception as e:
        return jsonify({"fulfillmentText": "Error processing request: " + str(e)})


if __name__ == '__main__':
    app.run(debug=True)'''


'''ort requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔹 Use your real API Key from ExchangeRate-API
API_KEY = "e54e536172dfb19b340c6fea"
EXCHANGE_API_URL ="https://v6.exchangerate-api.com/v6/e54e536172dfb19b340c6fea/latest/USD"

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        # 🔹 Get request data from Dialogflow
        data = request.get_json()
        print("📥 Received request from Dialogflow:", data)  # Debugging

        # 🔹 Extract parameters
        parameters = data.get("queryResult", {}).get("parameters", {})
        unit_currency = parameters.get("unit-currency", {})
        amount = unit_currency.get("amount")
        from_currency = unit_currency.get("currency")
        to_currency = parameters.get("currency-name")

        # 🔹 Validate input
        if not amount or not from_currency or not to_currency:
            return jsonify({"fulfillmentText": "Invalid input. Please provide both currencies and an amount."})

        # 🔹 Fetch exchange rate
        response = requests.get(f"{EXCHANGE_API_URL}{from_currency}")
        exchange_data = response.json()

        if "conversion_rates" not in exchange_data:
            return jsonify({"fulfillmentText": "Error fetching exchange rates."})

        conversion_rate = exchange_data["conversion_rates"].get(to_currency)
        if not conversion_rate:
            return jsonify({"fulfillmentText": f"Conversion rate for {to_currency} not available."})

        # 🔹 Perform conversion
        converted_amount = amount * conversion_rate
        fulfillment_text = f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}."

        # 🔹 Print and send response
        response_json = jsonify({"fulfillmentText": fulfillment_text})
        print("📤 Sending response to Dialogflow:", response_json.get_json())  # Debugging
        return response_json

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"fulfillmentText": "An error occurred while processing your request."})
e54e536172dfb19b340c6fe
if __name__ == '__main__':
    app.run(debug=True)'''
'''from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Replace this with your actual ExchangeRate-API key
API_KEY = "e54e536172dfb19b340c6fe"
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/e54e536172dfb19b340c6fea/latest/USD"


@app.route("/", methods=["GET","POST"])
def home():
    return "Flask Webhook is Running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handles requests from Dialogflow"""
    req = request.get_json()

    # DEBUG: Print the received JSON
    print("Received JSON from Dialogflow:", req)

    try:
        query_result = req.get("queryResult", {})

        # Extract parameters safely
        parameters = query_result.get("parameters", {})

        # ✅ FIX: Extract 'unit-currency' safely from a list
        unit_currency_list = parameters.get("unit-currency", [])
        if isinstance(unit_currency_list, list) and len(unit_currency_list) > 0:
            amount = unit_currency_list[0].get("amount", 1)
            from_currency = unit_currency_list[0].get("currency")
        else:
            return jsonify({"fulfillmentText": "Error: Could not extract currency amount."})

        to_currency = parameters.get("currency-name")

        if not from_currency or not to_currency:
            return jsonify({"fulfillmentText": "Please specify both currencies."})

        # ✅ Fetch real-time exchange rate
        exchange_rate = get_exchange_rate(from_currency, to_currency)
        if exchange_rate is None:
            return jsonify(
                {"fulfillmentText": f"Sorry, I couldn't fetch exchange rates for {from_currency} to {to_currency}."})

        converted_amount = round(amount * exchange_rate, 2)

        response_text = f"{amount} {from_currency} is approximately {converted_amount} {to_currency}."

        # ✅ Return response to Dialogflow
        return jsonify({"fulfillmentText": response_text})

    except Exception as e:
        return jsonify({"fulfillmentText": f"An error occurred: {str(e)}"})


def get_exchange_rate(from_currency, to_currency):
    """Fetch exchange rates from ExchangeRate-API"""
    try:
        # ✅ Correct API request URL
        url = EXCHANGE_RATE_API_URL.format(API_KEY, from_currency)
        response = requests.get(url)
        data = response.json()

        # ✅ DEBUG: Print API response
        print("API Response:", data)

        if "conversion_rates" not in data or to_currency not in data["conversion_rates"]:
            return None

        return data["conversion_rates"][to_currency]

    except Exception as e:
        print("Error fetching exchange rate:", str(e))
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    e54e536172dfb19b340c6fea"
BASE_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{from_currency}'''

'''import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "e54e536172dfb19b340c6fea"  # Replace with your valid ExchangeRate API key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        print("Received request:", json.dumps(req, indent=2))  # Debugging

        parameters = req['queryResult']['parameters']
        from_currency = parameters['unit-currency'][0]['currency']
        to_currency = parameters['currency-name'][0]
        amount = parameters['unit-currency'][0]['amount']

        # Validate API Key and URL
        if not API_KEY or "YOUR_API_KEY" in API_KEY:
            return jsonify({'fulfillmentText': "API key is missing or invalid. Please check your configuration."})

        response = requests.get(BASE_URL + from_currency)

        if response.status_code != 200:
            return jsonify({'fulfillmentText': "Failed to fetch exchange rates. Please try again later."})

        exchange_data = response.json()
        if 'conversion_rates' not in exchange_data:
            return jsonify({'fulfillmentText': "Error retrieving conversion rates. Please check your API key."})

        # Perform currency conversion
        rate = exchange_data['conversion_rates'].get(to_currency)
        if rate is None:
            return jsonify({'fulfillmentText': f"Exchange rate for {to_currency} is not available."})

        converted_amount = amount * rate
        result_text = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}."

        return jsonify({'fulfillmentText': result_text})

    except Exception as e:
        return jsonify({'fulfillmentText': f"An unexpected error occurred: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)'''

import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mapping of countries to currencies
COUNTRY_CURRENCY = {
    "India": "Indian Rupee (INR)",
    "Japan": "Japanese Yen (JPY)",
    "Canada": "Canadian Dollar (CAD)",
    "United States": "US Dollar (USD)",
    "United Kingdom": "Pound Sterling (GBP)",
    "Germany": "Euro (EUR)",
    "France": "Euro (EUR)",
    "Australia": "Australian Dollar (AUD)",
    "Brazil": "Brazilian Real (BRL)"
}


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        print("Received request:", json.dumps(req, indent=2))

        intent_name = req['queryResult']['intent']['displayName']

        if intent_name == "currency_converter":
            parameters = req['queryResult']['parameters']
            from_currency = parameters['unit-currency'][0]['currency']
            to_currency = parameters['currency-name'][0]
            amount = parameters['unit-currency'][0]['amount']

            response_text = convert_currency(from_currency, to_currency, amount)

        elif intent_name == "get_country_currency":
            country = req['queryResult']['parameters'].get('geo-country', '')
            response_text = COUNTRY_CURRENCY.get(country, f"Sorry, I don't have currency information for {country}.")

        else:
            response_text = "I'm not sure how to help with that."

        return jsonify({'fulfillmentText': response_text})

    except Exception as e:
        return jsonify({'fulfillmentText': f"An error occurred: {str(e)}"})


def convert_currency(from_currency, to_currency, amount):
    API_KEY = "e54e536172dfb19b340c6fea"  # Replace with your valid API key
    BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

    response = requests.get(BASE_URL + from_currency)
    if response.status_code != 200:
        return "Failed to fetch exchange rates."

    exchange_data = response.json()
    rate = exchange_data['conversion_rates'].get(to_currency)

    if rate is None:
        return f"Exchange rate for {to_currency} is not available."

    converted_amount = amount * rate
    return f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}."


if __name__ == '__main__':
    app.run(debug=True)
