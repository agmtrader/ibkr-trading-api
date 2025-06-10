from flask import Blueprint
from src.components.account_manager import AccountManager
from flask import request
import requests
from src.utils.logger import logger

BASE_API_URL = "https://localhost:5055/v1/api"

account_manager = AccountManager()

bp = Blueprint('contracts', __name__)

@bp.route("/search", methods=['POST'])
def secdef_search_route():
    logger.info(f"Starting contract search")
    
    try:
        url = f"{BASE_API_URL}/iserver/secdef/search"
        logger.info(f"Base URL: {url}")
        
        payload = request.get_json(force=True)
        logger.info(f"Received payload: {payload}")
        
        symbol = payload.get("symbol", None)
        secType = payload.get("secType", None)
        name = payload.get("name", None)
        more = payload.get("more", None)
        fund = payload.get("fund", None)
        fundFamilyConidEx = payload.get("fundFamilyConidEx", None)
        pattern = payload.get("pattern", None)
        referrer = payload.get("referrer", None)
        
        if symbol:
            url += f"?symbol={symbol}"
        if secType:
            url += f"&secType={secType}"
        if name:
            url += f"&name={name}"
        if more:
            url += f"&more={more}"
        if fund:
            url += f"&fund={fund}"
        if fundFamilyConidEx:
            url += f"&fundFamilyConidEx={fundFamilyConidEx}"
        if pattern:
            url += f"&pattern={pattern}"
        if referrer:
            url += f"&referrer={referrer}"
            
        logger.info(f"Final URL: {url}")
        logger.info(f"Making request to IBKR API...")
        
        response = requests.get(url, verify=False, timeout=30)
        logger.info(f"Received response with status code: {response.status_code}")
        
        response_json = response.json()
        logger.info(f"Response JSON: {response_json}")
        
        return response_json
        
    except requests.exceptions.Timeout:
        logger.error("Request to IBKR API timed out")
        return {"error": "Request timed out"}, 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {"error": f"Request failed: {str(e)}"}, 500
    except Exception as e:
        logger.error(f"Unexpected error in contract search: {str(e)}")
        return {"error": f"Internal error: {str(e)}"}, 500

@bp.route("/info", methods=['POST'])
def secdef_info_route():
    logger.info(f"Fetching contract information")
    url = f"{BASE_API_URL}/iserver/secdef/info"
    payload = request.get_json(force=True)
    conid = payload.get("conid", None)
    sectype = payload.get("sectype", None)
    month = payload.get("month", None)
    exchange = payload.get("exchange", None)
    strike = payload.get("strike", None)
    right = payload.get("right", None)
    issuerId = payload.get("issuerId", None)
    filters = payload.get("filters", None)
    if conid:
        url += f"?conid={conid}"
    if sectype:
        url += f"&sectype={sectype}"
    if month:
        url += f"&month={month}"
    if exchange:
        url += f"&exchange={exchange}"
    if strike:
        url += f"&strike={strike}"
    if right:
        url += f"&right={right}"
    if issuerId:
        url += f"&issuerId={issuerId}"
    if filters:
        url += f"&filters={filters}"
    response = requests.get(url, verify=False)
    return response.json()