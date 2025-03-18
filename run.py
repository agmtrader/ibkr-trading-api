import requests, os
from flask import Flask, request
from src.utils.logger import logger

BASE_API_URL = "https://localhost:5055/v1/api"

os.environ['PYTHONHTTPSVERIFY'] = '0'

class AccountManager:
    _instance = None
    _account_id = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    def clear(self):
        self._account_id = None

app = Flask(__name__)
account_manager = AccountManager.get_instance()

# Authentication
@app.route("/", methods=['GET'])
def main_route():
    try:
        r = requests.get(f"{BASE_API_URL}/portfolio/accounts", verify=False)
        accounts = r.json()
        if accounts and len(accounts) > 0:
            account = accounts[0]
            account_manager.account_id = account["id"]
            response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/summary", verify=False)
            summary = response.json()
            return { "account": account, "summary": summary }
    except Exception as e:
        return '<a href="https://localhost:5055" target="_blank" rel="noopener noreferrer">Log in</a>'
    return {"error": "No accounts found"}, 404

@app.route("/logout", methods=['POST'])
def logout_route():
    account_manager.clear()
    response = requests.post(f"{BASE_API_URL}/logout", verify=False)
    return response.json()

@app.route("/auth/status", methods=['GET'])
def auth_status_route():
    response = requests.get(f"{BASE_API_URL}/iserver/auth/status", verify=False)
    return response.json()

@app.route("/auth/init", methods=['POST'])
def auth_init_route():
    response = requests.post(f"{BASE_API_URL}/iserver/auth/ssodh/init?publish=true&compete=true", verify=False)
    return response.json()

@app.route("/sso/validate", methods=['GET'])
def sso_validate_route():
    response = requests.get(f"{BASE_API_URL}/sso/validate", verify=False)
    return response.json()

# Contracts
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

# FYI and Notifications
@app.route("/fyi/unreadnumber", methods=['GET'])
def fyi_unreadnumber_route():
    response = requests.get(f"{BASE_API_URL}/fyi/unreadnumber", verify=False)
    return response.json()

@app.route("/fyi/settings", methods=['GET'])
def fyi_settings_route():
    response = requests.get(f"{BASE_API_URL}/fyi/settings", verify=False)
    return response.json()

@app.route("/fyi/settings/<typecode>", methods=['POST'])
def fyi_settings_typecode_route(typecode):
    data = request.get_json(force=True)
    response = requests.post(f"{BASE_API_URL}/fyi/settings/{typecode}", json=data, verify=False)
    return response.json()

@app.route("/fyi/disclaimer/<typecode>", methods=['GET'])
def fyi_disclaimer_get_route(typecode):
    response = requests.get(f"{BASE_API_URL}/fyi/disclaimer/{typecode}", verify=False)
    return response.json()

@app.route("/fyi/disclaimer/<typecode>", methods=['PUT'])
def fyi_disclaimer_put_route(typecode):
    data = request.get_json(force=True)
    response = requests.put(f"{BASE_API_URL}/fyi/disclaimer/{typecode}", json=data, verify=False)
    return response.json()

@app.route("/fyi/deliveryoptions", methods=['GET'])
def fyi_deliveryoptions_route():
    response = requests.get(f"{BASE_API_URL}/fyi/deliveryoptions", verify=False)
    return response.json()

@app.route("/fyi/deliveryoptions/email", methods=['PUT'])
def fyi_deliveryoptions_email_route():
    data = request.get_json(force=True)
    response = requests.put(f"{BASE_API_URL}/fyi/deliveryoptions/email", json=data, verify=False)
    return response.json()

@app.route("/fyi/deliveryoptions/device", methods=['POST'])
def fyi_deliveryoptions_device_route():
    data = request.get_json(force=True)
    response = requests.post(f"{BASE_API_URL}/fyi/deliveryoptions/device", json=data, verify=False)
    return response.json()

@app.route("/fyi/deliveryoptions/<deviceId>", methods=['DELETE'])
def fyi_deliveryoptions_device_delete_route(deviceId):
    response = requests.delete(f"{BASE_API_URL}/fyi/deliveryoptions/{deviceId}", verify=False)
    return response.json()

@app.route("/fyi/notifications", methods=['GET'])
def fyi_notifications_route():
    response = requests.get(f"{BASE_API_URL}/fyi/notifications", verify=False)
    return response.json()

@app.route("/fyi/notifications/more", methods=['GET'])
def fyi_notifications_more_route():
    response = requests.get(f"{BASE_API_URL}/fyi/notifications/more", verify=False)
    return response.json()

@app.route("/fyi/notifications/<notificationId>", methods=['PUT'])
def fyi_notifications_update_route(notificationId):
    data = request.get_json(force=True)
    response = requests.put(f"{BASE_API_URL}/fyi/notifications/{notificationId}", json=data, verify=False)
    return response.json()

# Market Data
@app.route("/market-data", methods=['GET'])
def market_data_route():
    conids = request.args.get("conids", "")
    fields = request.args.get("fields", "31,55,6509,84")  # Default fields for price, volume, etc.
    
    response = requests.get(f"{BASE_API_URL}/iserver/marketdata/snapshot?conids={conids}&fields={fields}", verify=False)
    return response.json()

@app.route("/market-data/snapshot", methods=['GET'])
def market_data_snapshot_route():
    conids = request.args.get("conids", "")
    fields = request.args.get("fields", "31,55,6509,84")
    response = requests.get(f"{BASE_API_URL}/iserver/marketdata/snapshot?conids={conids}&fields={fields}", verify=False)
    return response.json()

@app.route("/portfolio/accounts", methods=['GET'])
def portfolio_accounts_route():
    response = requests.get(f"{BASE_API_URL}/portfolio/accounts", verify=False)
    return response.json()

@app.route("/portfolio/subaccounts", methods=['GET'])
def portfolio_subaccounts_route():
    response = requests.get(f"{BASE_API_URL}/portfolio/subaccounts", verify=False)
    return response.json()

@app.route("/portfolio/pnl/partitioned", methods=['GET'])
def portfolio_pnl_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/iserver/account/pnl/partitioned", verify=False)
    return response.json()

# Orders
@app.route("/orders", methods=['GET'])
def orders_route():
    response = requests.get(f"{BASE_API_URL}/iserver/account/orders", verify=False)
    orders = response.json()["orders"]
    return { "orders": orders }

@app.route("/trades", methods=['GET'])
def trades_route():
    response = requests.get(f"{BASE_API_URL}/iserver/account/trades", verify=False)
    return response.json()

# Portfolio
@app.route("/portfolio", methods=['GET'])
def portfolio_route():
    logger.info(f"account_id: {account_manager.account_id}")
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/positions/0", verify=False)
    positions = response.json()
    return { "positions": positions }

@app.route("/account/allocation", methods=['GET'])
def account_allocation_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/allocation", verify=False)
    return response.json()

@app.route("/positions", methods=['GET'])
def positions_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/positions/0", verify=False)
    return response.json()

@app.route("/account/summary", methods=['GET'])
def account_summary_route():
    logger.info(f"account_id: {account_manager.account_id}")
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/summary", verify=False)
    return response.json()

@app.route("/account/ledger", methods=['GET'])
def account_ledger_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/ledger", verify=False)
    return response.json()

# Portfolio Analyst
@app.route("/pa/performance", methods=['POST'])
def pa_performance_route():
    data = request.get_json(force=True)
    response = requests.post(f"{BASE_API_URL}/pa/performance", json=data, verify=False)
    return response.json()

@app.route("/pa/summary", methods=['POST'])
def pa_summary_route():
    data = request.get_json(force=True)
    response = requests.post(f"{BASE_API_URL}/pa/summary", json=data, verify=False)
    return response.json()

@app.route("/pa/transactions", methods=['POST'])
def pa_transactions_route():
    data = request.get_json(force=True)
    response = requests.post(f"{BASE_API_URL}/pa/transactions", json=data, verify=False)
    return response.json()

# Scanner
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


@app.route("/tickle", methods=['GET'])
def tickle_route():
    response = requests.get(f"{BASE_API_URL}/tickle", verify=False)
    return response.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055, debug=True)