import base64
import os
from dotenv import load_dotenv

from src.enums import UiFirstUp

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
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Bearer {os.getenv("TC_ADMIN_TOKEN")}'
        return headers

    @staticmethod
    def admin_basic_auth_headers():
        credentials = base64.b64encode(
            f"{UiFirstUp.ADMIN_USERNAME}:{UiFirstUp.ADMIN_PASSWORD}".encode()
        ).decode()
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Basic {credentials}'
        return headers
