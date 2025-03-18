from flask import Blueprint
from src.utils.logger import logger
from src.components.account_manager import AccountManager
import requests

BASE_API_URL = "https://localhost:5055/v1/api"

account_manager = AccountManager()

bp = Blueprint('portfolio', __name__)

# Portfolio
@bp.route("/portfolio", methods=['GET'])
def portfolio_route():
    logger.info(f"account_id: {account_manager.account_id}")
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/positions/0", verify=False)
    positions = response.json()
    return { "positions": positions }

@bp.route("/account/allocation", methods=['GET'])
def account_allocation_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/allocation", verify=False)
    return response.json()

@bp.route("/positions", methods=['GET'])
def positions_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/positions/0", verify=False)
    return response.json()

@bp.route("/account/summary", methods=['GET'])
def account_summary_route():
    logger.info(f"Accessing account summary with account_id: {account_manager.account_id}")
    if account_manager.account_id is None:
        logger.error("No account selected. Please ensure you've logged in and accessed the main route first.")
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/summary", verify=False)
    return response.json()

@bp.route("/account/ledger", methods=['GET'])
def account_ledger_route():
    if account_manager.account_id is None:
        return {"error": "No account selected"}, 400
    response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/ledger", verify=False)
    return response.json()
