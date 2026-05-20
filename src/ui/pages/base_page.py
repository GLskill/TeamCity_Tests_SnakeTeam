from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TypeVar, Type
from playwright.sync_api import Page
from src.api.configs.config import Config

T = TypeVar('T', bound="BasePage")


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).strip('/')

    @property
    def admin_name_input(self):
        return self.page.locator("#username")

    @property
    def admin_password_input(self):
        return self.page.locator("#password")

    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    @property  # Кнопка на переход во вкладку "Projects"
    def admin_projects_button(self):
        return self.page.locator('[data-test-title="Projects"]')

    @property  # Кнопка на переход во вкладку "Changes"
    def admin_changes_button(self):
        return self.page.locator('[data-test-title="Changes"]')

    @property  # Кнопка на переход во вкладку "Agents"
    def admin_agents_button(self):
        return self.page.locator('a[data-test="ring-link"][href*="/agents"]')

    @property  # Кнопка на переход во вкладку "Queue"
    def admin_queue_button(self):
        return self.page.locator('[data-test-title*="Queue"]')

    @property  # Кнопка на переход во вкладку "Admin"
    def admin_administration_button(self):
        return self.page.locator('[data-test-title="Administration"]')

    @property  # Кнопка на переход во вкладку "My investigations"
    def admin_my_investigations_button(self):
        return self.page.locator('[data-test-title*="My Investigations"]')

    @property  # Кнопка на переход во вкладку "Whot's new"
    def admin_whot_new_button(self):
        return self.page.locator('[data-test-title="What\'s New"]')

    @property  # Кнопка на переход во вкладку "Help"
    def admin_help_button(self):
        return self.page.locator('[data-test-title="Help"]')

    @property  # Кнопка на переход к дроп список аккаунта
    def account_menu_button(self):
        return self.page.locator('[data-hint-container-id="header-user-menu"]')

    @property  # строка 'Profile'
    def account_menu_profile(self):
        return self.page.locator('[id*="profile.html"]')

    @property  # строка 'Appearance'
    def account_menu_appearance(self):
        return self.page.locator('[id*="Appearance"]')

    @property  # строка 'My Builds'
    def account_menu_favorite_builds(self):
        return self.page.locator('[id*="/favorite/builds"]')

    @property  # строка 'Logout'
    def account_menu_logout(self):
        return self.page.locator('[id*="logout"]')

    @property  # переключение на классический UI
    def admin_switch_to_classic_ui_button(self):
        return self.page.locator('a[title="Switch to Classic UI"]')

    def click_switch_to_projects(self):
        from src.ui.pages.project_page import ProjectPanel
        self.admin_projects_button.click()
        return ProjectPanel(self.page)

    def click_switch_to_changes(self):
        from src.ui.pages.changes_page import ChangesPanel
        self.admin_changes_button.click()
        return ChangesPanel(self.page)

    def click_switch_to_agents(self):
        from src.ui.pages.agents_page import AgentsPanel
        self.admin_agents_button.click()
        return AgentsPanel(self.page)

    def click_switch_to_queue(self):
        from src.ui.pages.queue_page import QueuePanel
        self.admin_queue_button.click()
        return QueuePanel(self.page)

    def click_switch_to_administration(self):
        from src.ui.pages.administration_page import AdminPanel
        self.admin_administration_button.click()
        return AdminPanel(self.page)

    def click_switch_to_my_investigations(self):
        self.admin_my_investigations_button.click()
        return self

    def click_switch_to_whots_new(self):
        self.admin_whot_new_button.click()
        return self

    def click_switch_to_help(self):
        self.admin_help_button.click()

    def click_go_to_profile_menu(self):
        self.account_menu_button.click()
        self.account_menu_profile.click()

    def click_go_to_appearance(self):
        self.account_menu_button.click()
        self.account_menu_appearance.click()

    def click_go_to_favorite_builds(self):
        self.account_menu_button.click()
        self.account_menu_favorite_builds.click()

    def click_go_to_log_out(self):
        from src.ui.pages.login_page import LoginPage
        self.account_menu_button.click()
        self.account_menu_logout.click()
        return LoginPage(self.page)

    def click_go_to_classic_ui(self):
        self.admin_switch_to_classic_ui_button.click()

    def open(self: T) -> T:
        target = self.url()
        if self.base_url and target.startswith('/'):
            target = f'{self.base_url}{target}'
        self.page.goto(target, wait_until="domcontentloaded")
        return self

    def get_page(self, page_cls: Type[T]) -> T:
        return page_cls(self.page)
