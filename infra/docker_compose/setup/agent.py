import base64
import time

import requests

from infra.docker_compose.setup.config import TC_URL


def authorize_agent(token: str, timeout: int = 180) -> None:
    print("[setup] Ждём и авторизуем агента...")
    credentials = base64.b64encode(f":{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json",
    }
    deadline = time.time() + timeout

    # Шаг 1: ждём пока агент появится в unauthorized
    agent_id = None
    while time.time() < deadline:
        try:
            r = requests.get(
                f"{TC_URL}/app/rest/agents?locator=authorized:false",
                headers=headers,
                timeout=5
            )
            if r.status_code == 200:
                agents = r.json().get("agent", [])
                if agents:
                    agent_id = agents[0]["id"]
                    print(f"[setup] Агент id:{agent_id} найден в unauthorized, авторизуем...")
                    break
        except Exception as e:
            print(f"[setup] Ошибка: {e}")
        print("[setup] Агент ещё не подключился, ждём 5 сек...")
        time.sleep(5)

    if agent_id is None:
        raise RuntimeError("Агент не появился за отведённое время")

    # Шаг 2: ждём полной регистрации агента
    print("[setup] Ждём полной регистрации агента (15 сек)...")
    time.sleep(15)

    # Шаг 3: авторизуем агента
    requests.put(
        f"{TC_URL}/app/rest/agents/id:{agent_id}/authorized",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "text/plain",
            "Accept": "text/plain",
        },
        data="true",
        timeout=10
    )

    # Шаг 4: ждём подтверждения авторизации
    print("[setup] Ждём подтверждения авторизации...")
    while time.time() < deadline:
        try:
            r = requests.get(
                f"{TC_URL}/app/rest/agents?locator=authorized:true",
                headers=headers,
                timeout=5
            )
            if r.status_code == 200:
                agents = r.json().get("agent", [])
                if any(a["id"] == agent_id for a in agents):
                    print(f"[setup] Агент id:{agent_id} авторизован и подтверждён ✓")
                    return
        except Exception as e:
            print(f"[setup] Ошибка при проверке: {e}")
        time.sleep(5)

    raise RuntimeError("Агент не перешёл в authorized за отведённое время")
