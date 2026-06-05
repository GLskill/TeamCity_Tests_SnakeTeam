import os
import re
import time

from infra.docker_compose.setup.config import TC_LOG


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
