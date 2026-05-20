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
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = f'Bearer {os.getenv("TC_ADMIN_TOKEN")}'
        return headers
