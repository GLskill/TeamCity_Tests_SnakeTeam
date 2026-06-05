import base64
import time

import requests

from infra.docker_compose.setup.config import TC_URL


def wait_for_rest_api(token: str, timeout: int = 120) -> None:
    print("[setup] Ожидаем REST API...")
    credentials = base64.b64encode(f":{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json",
    }
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{TC_URL}/app/rest/server", headers=headers, timeout=5)
            if r.status_code == 200:
                print("[setup] REST API готов ✓")
                return
        except Exception:
            pass
        time.sleep(5)
    raise RuntimeError("REST API не поднялся за отведённое время")
