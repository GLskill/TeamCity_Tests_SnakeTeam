import base64
import os
from dotenv import load_dotenv

load_dotenv()


class RequestSpecs:
    @staticmethod
    def default_req_headers():
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @staticmethod
    def unauth_spec():
        return RequestSpecs.default_req_headers()

    @staticmethod
    def admin_base_headers():
        credentials = base64.b64encode(
            f":{os.getenv('TC_ADMIN_TOKEN')}".encode()
        ).decode()
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Basic {credentials}'
        return headers

    @staticmethod
    def super_user_headers():
        credentials = base64.b64encode(
            f":{os.getenv('TC_ADMIN_TOKEN')}".encode()
        ).decode()
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Basic {credentials}'
        return headers

    @staticmethod
    def admin_basic_auth_headers() -> dict:
        credentials = base64.b64encode(
            f"{os.getenv('TC_ADMIN_USERNAME')}:{os.getenv('TC_ADMIN_PASSWORD')}".encode()
        ).decode()
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Basic {credentials}'
        return headers

    @staticmethod
    def basic_auth_headers(username: str, password: str) -> dict:
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Basic {credentials}'
        return headers

    @staticmethod
    def token_auth_headers(token: str) -> dict:
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Bearer {token}'
        return headers
