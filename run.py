from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.utils.logger import logger
import requests
from src.components.account_manager import AccountManager

load_dotenv()

BASE_API_URL = "https://localhost:5055/v1/api"
account_manager = AccountManager()

def start_api():

    app = Flask(__name__, static_folder='static')
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initialize Limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["60 per minute"],
        storage_uri='memory://'
    )

    from src.app import portfolio
    app.register_blueprint(portfolio.bp, url_prefix='/')

    # Create index route
    @app.route("/", methods=['GET'])
    def main_route():
        try:
            logger.info("Attempting to fetch accounts...")
            r = requests.get(f"{BASE_API_URL}/portfolio/accounts", verify=False)
            accounts = r.json()
            logger.info(f"Received accounts response: {accounts}")
            if accounts and len(accounts) > 0:
                account = accounts[0]
                logger.info(f"Setting account_id to: {account['id']}")
                account_manager.account_id = account["id"]
                response = requests.get(f"{BASE_API_URL}/portfolio/{account_manager.account_id}/summary", verify=False)
                summary = response.json()
                return { "account": account, "summary": summary }
        except Exception as e:
            logger.error(f"Error in main_route: {str(e)}")
            return '<a href="https://localhost:5055" target="_blank" rel="noopener noreferrer">Log in</a>'
        logger.warning("No accounts found")
        return {"error": "No accounts found"}, 404

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500 

    @app.errorhandler(400)
    def bad_request_error(error):
        app.logger.error(f'Bad request: {error}')
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        app.logger.error(f'Unauthorized access attempt: {error}')
        return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.error(f'Forbidden access attempt: {error}')
        return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource"}), 403

    return app

app = start_api()
logger.announcement('Successfully started IBKR Trading API', type='success')
