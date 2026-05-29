import os
import time

import requests
from playwright.sync_api import sync_playwright

TC_URL = "http://webapp:8111"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
TOKEN_NAME = "pytest-token"
ENV_FILE = os.environ.get("ENV_FILE", "/app/.env")


def setup_teamcity_ui() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()

        print("[setup] Открываем wizard...")
        page.goto(f"{TC_URL}/mnt")

        # Шаг 1 — выбор datadir ("TeamCity First Start")
        print("[setup] Ждём страницу First Start...")
        page.wait_for_selector("button:has-text('Proceed'), input[id='proceedButton']", timeout=60_000)
        page.locator("button:has-text('Proceed'), input[id='proceedButton']").first.click()
        page.wait_for_load_state("networkidle")
        print("[setup] Шаг 1 — datadir ✓")

        # Шаг 2 — настройка БД ("Database connection setup")
        print("[setup] Ждём страницу Database...")
        page.wait_for_selector("button:has-text('Proceed'), input[id='proceedButton']", timeout=60_000)
        page.locator("button:has-text('Proceed'), input[id='proceedButton']").first.click()
        page.wait_for_load_state("networkidle")
        print("[setup] Шаг 2 — DB ✓")

        # Шаг 3 — лицензионное соглашение ("License Agreement")
        print("[setup] Ждём страницу License Agreement...")
        page.wait_for_selector("button:has-text('Accept')", timeout=180_000)
        page.locator("button:has-text('Accept')").click()
        page.wait_for_load_state("networkidle")
        print("[setup] Шаг 3 — лицензия ✓")

        # TeamCity настраивается ~15 сек — ждём страницу создания админа
        print("[setup] Ждём страницу создания администратора...")
        page.wait_for_url("**/setupAdmin.html", timeout=120_000)

        # Шаг 4 — создание администратора
        page.wait_for_selector("#input_teamcityUsername", timeout=30_000)
        page.fill("#input_teamcityUsername", ADMIN_USER)
        page.fill("#password1", ADMIN_PASS)
        page.fill("#retypedPassword", ADMIN_PASS)
        page.locator("button:has-text('Create Account'), input[type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        print(f"[setup] Шаг 4 — пользователь '{ADMIN_USER}' создан ✓")

        browser.close()


def wait_for_rest_api(timeout: int = 120) -> None:
    """Ждёт пока REST API поднимется после wizard."""
    print("[setup] Ожидаем REST API...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(
                f"{TC_URL}/app/rest/server",
                auth=(ADMIN_USER, ADMIN_PASS),
                headers={"Accept": "application/json"},
                timeout=5,
            )
            if r.status_code == 200:
                print("[setup] REST API готов ✓")
                return
        except requests.RequestException:
            pass
        time.sleep(5)
    raise RuntimeError("REST API не поднялся за отведённое время")


def create_access_token() -> str:
    """Создаёт (или пересоздаёт) access token для admin."""
    r = requests.get(
        f"{TC_URL}/app/rest/users/username:{ADMIN_USER}",
        auth=(ADMIN_USER, ADMIN_PASS),
        headers={"Accept": "application/json"},
        timeout=10,
    )
    r.raise_for_status()
    user_id = r.json()["id"]

    # Удаляем старый токен если есть (идемпотентность при повторном запуске)
    requests.delete(
        f"{TC_URL}/app/rest/users/id:{user_id}/tokens/{TOKEN_NAME}",
        auth=(ADMIN_USER, ADMIN_PASS),
        timeout=10,
    )

    r = requests.post(
        f"{TC_URL}/app/rest/users/id:{user_id}/tokens/{TOKEN_NAME}",
        auth=(ADMIN_USER, ADMIN_PASS),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"name": TOKEN_NAME},
        timeout=10,
    )
    r.raise_for_status()
    token: str = r.json()["value"]
    print(f"[setup] Токен создан: {token[:8]}... ✓")
    return token


def save_env(token: str) -> None:
    """Записывает credentials в .env для python-dotenv в тестах."""
    env_dir = os.path.dirname(ENV_FILE)
    if env_dir:
        os.makedirs(env_dir, exist_ok=True)
    with open(ENV_FILE, "w") as f:
        f.write(f"TC_ADMIN_TOKEN={token}\n")
        f.write(f"TC_ADMIN_USERNAME={ADMIN_USER}\n")
        f.write(f"TC_ADMIN_PASSWORD={ADMIN_PASS}\n")
    print(f"[setup] Credentials сохранены → {ENV_FILE} ✓")


if __name__ == "__main__":
    setup_teamcity_ui()
    wait_for_rest_api()
    token = create_access_token()
    save_env(token)
    print("[setup] ✅ Готово")