import requests, os
from flask import Flask, request
from src.utils.logger import logger

BASE_API_URL = "https://localhost:5055/v1/api"
ACCOUNT_ID = os.environ['IBKR_ACCOUNT_ID']

os.environ['PYTHONHTTPSVERIFY'] = '0'

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main_route():

    try:
        r = requests.get(f"{BASE_API_URL}/portfolio/accounts", verify=False)
        accounts = r.json()
    except Exception as e:
        return '<a href="https://localhost:5055" target="_blank" rel="noopener noreferrer">Log in</a>'

    account = accounts[0]
    account_id = accounts[0]["id"]
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_id}/summary", verify=False)
    summary = response.json()
    
    return { "account": account, "summary": summary }

@app.route("/orders", methods=['GET'])
def orders_route():
    response = requests.get(f"{BASE_API_URL}/iserver/account/orders", verify=False)
    orders = response.json()["orders"]
    
    return { "orders": orders }

@app.route("/lookup", methods=['POST'])
def lookup_route():
    payload = request.get_json(force=True)
    symbol = payload['symbol']

    stocks = []
    if symbol is not None:
        response = requests.get(f"{BASE_API_URL}/iserver/secdef/search?symbol={symbol}&name=true", verify=False)
        stocks = response.json()
    else:
        stocks = []

    return {"stocks": stocks}

@app.route("/portfolio", methods=['GET'])
def portfolio_route():

    response = requests.get(f"{BASE_API_URL}/portfolio/{ACCOUNT_ID}/positions/0", verify=False)
    positions = response.json()
    return { "positions": positions }


@app.route("/scanner", methods=['GET'])
def scanner_route():
    response = requests.get(f"{BASE_API_URL}/iserver/scanner/params", verify=False)
    params = response.json()

    scanner_map = {}
    filter_map = {}

    for item in params['instrument_list']:
        scanner_map[item['type']] = {
            "display_name": item['display_name'],
            "filters": item['filters'],
            "sorts": []
        }

    for item in params['filter_list']:
        filter_map[item['group']] = {
            "display_name": item['display_name'],
            "type": item['type'],
            "code": item['code']
        }

    for item in params['scan_type_list']:
        for instrument in item['instruments']:
            scanner_map[instrument]['sorts'].append({
                "name": item['display_name'],
                "code": item['code']
            })

    for item in params['location_tree']:
        scanner_map[item['type']]['locations'] = item['locations']


    submitted = request.args.get("submitted", "")
    selected_instrument = request.args.get("instrument", "")
    location = request.args.get("location", "")
    sort = request.args.get("sort", "")
    scan_results = []
    filter_code = request.args.get("filter", "")
    filter_value = request.args.get("filter_value", "")

    if submitted:
        print("submitting")
        data = {
            "instrument": selected_instrument,
            "location": location,
            "type": sort,
            "filter": [
                {
                    "code": filter_code,
                    "value": filter_value
                }
            ]
        }
            
        r = requests.post(f"{BASE_API_URL}/iserver/scanner/run", json=data, verify=False)
        scan_results = r.json()

    return {
        "params": params,
        "scanner_map": scanner_map,
        "filter_map": filter_map,
        "scan_results": scan_results
    }