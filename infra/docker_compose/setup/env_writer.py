import os

from infra.docker_compose.setup.config import ENV_FILE


def save_token_to_env(token: str) -> None:
    env_dir = os.path.dirname(ENV_FILE)
    if env_dir:
        os.makedirs(env_dir, exist_ok=True)
    with open(ENV_FILE, "w") as f:
        f.write(f"TC_ADMIN_TOKEN={token}\n")
    print(f"[setup] Credentials сохранены → {ENV_FILE} ✓")
