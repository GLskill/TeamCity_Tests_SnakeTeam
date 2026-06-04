import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

from infra.docker_compose.tc_mnt_page import MntStartedPage

sys.path.insert(0, "/app")
TC_URL = os.environ.get("UI_BASE_URL", "http://webapp:8111")
ENV_FILE = os.environ.get("ENV_FILE", "/app/.env")
TC_LOG = os.environ.get("TC_LOG_FILE", "/teamcity-logs/teamcity-server.log")


def get_super_user_token(timeout: int = 120) -> str:
    print(f"[setup] Ждём super user token в {TC_LOG} ...")

    if not os.path.exists(TC_LOG):
        raise RuntimeError(f"Лог-файл не найден: {TC_LOG}")

    deadline = time.time() + timeout
    while time.time() < deadline:
        with open(TC_LOG, "r", errors="replace") as f:
            logs = f.read()
        matches = re.findall(r"Super user authentication token:\s*(\d+)", logs)
        if matches:
            token = matches[-1]
            print(f"[setup] Super user token получен: {token[:6]}...")
            return token
        print("[setup] Токен ещё не появился, ждём 5 сек...")
        time.sleep(5)

    raise RuntimeError(f"Super user token не появился в {TC_LOG} за {timeout} сек.")


def setup_teamcity_ui() -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()

        (
            MntStartedPage(page)
            .open()
            .accept_first_start()
            .accept_database_setup()
            .accept_license_agreement()     #.create_admin_account()
        )

        token = get_super_user_token()

        browser.close()

    print("[setup] UI wizard завершён ✓")
    return token


def wait_for_rest_api(token: str, timeout: int = 120) -> None:
    import base64
    import requests

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


def authorize_agent(token: str, timeout: int = 180) -> None:
    import base64
    import requests

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

    # Шаг 2: ждём пока агент полностью зарегистрируется на сервере
    print("[setup] Ждём полной регистрации агента (15 сек)...")
    time.sleep(15)

    # Шаг 3: отправляем PUT на авторизацию
    # Accept: application/json нельзя — PUT возвращает plain text, нужен Accept: text/plain
    put_r = requests.put(
        f"{TC_URL}/app/rest/agents/id:{agent_id}/authorized",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "text/plain",
            "Accept": "text/plain",
        },
        data="true",
        timeout=10
    )

    # Шаг 4: ждём пока агент реально появится в authorized:true
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


def save_token_to_env(token: str) -> None:
    env_dir = os.path.dirname(ENV_FILE)
    if env_dir:
        os.makedirs(env_dir, exist_ok=True)
    with open(ENV_FILE, "w") as f:
        f.write(f"TC_ADMIN_TOKEN={token}\n")
        f.write(f"TC_ADMIN_USERNAME=admin\n")
        f.write(f"TC_ADMIN_PASSWORD=admin123\n")
    print(f"[setup] Credentials сохранены → {ENV_FILE} ✓")


if __name__ == "__main__":
    if os.path.exists(ENV_FILE):
        os.remove(ENV_FILE)
        print(f"[setup] Старый {ENV_FILE} удалён")

    token = setup_teamcity_ui()
    wait_for_rest_api(token)
    authorize_agent(token)
    save_token_to_env(token)
    print("[setup] ✅ Готово")
