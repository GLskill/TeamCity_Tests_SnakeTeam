from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Type

from playwright.sync_api import Page
from src.api.configs.config import Config
from src.ui.elements.page_elements import PageElements

T = TypeVar('T', bound="BasePage")


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).strip('/')
        self.header = PageElements(page)

    @property
    def admin_name_input(self):
        return self.page.locator("#username")

    @property
    def admin_password_input(self):
        return self.page.locator("#password")

    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def click_switch_to_projects(self):
        from src.ui.pages.project_page import ProjectPanel
        self.header.click_projects()
        return ProjectPanel(self.page)

    def click_switch_to_changes(self):
        from src.ui.pages.changes_page import ChangesPanel
        self.header.click_changes()
        return ChangesPanel(self.page)

    def click_switch_to_agents(self):
        from src.ui.pages.agents_page import AgentsPanel
        self.header.click_agents()
        return AgentsPanel(self.page)

    def click_switch_to_queue(self):
        from src.ui.pages.queue_page import QueuePanel
        self.header.click_queue()
        return QueuePanel(self.page)

    def click_switch_to_administration(self):
        from src.ui.pages.administration_page import AdminPanel
        self.header.click_administration()
        return AdminPanel(self.page)

    def click_switch_to_my_investigations(self):
        self.header.click_my_investigations()
        return self

    def click_switch_to_whots_new(self):
        self.header.click_whats_new()
        return self

    def click_switch_to_help(self):
        self.header.click_help()

    def click_go_to_profile_menu(self):
        self.header.go_to_profile()

    def click_go_to_appearance(self):
        self.header.go_to_appearance()

    def click_go_to_favorite_builds(self):
        self.header.go_to_favorite_builds()

    def click_go_to_log_out(self):
        from src.ui.pages.login_page import LoginPage
        self.header.go_to_logout()
        return LoginPage(self.page)

    def click_go_to_classic_ui(self):
        self.header.go_to_classic_ui()

    def open(self: T) -> T:
        target = self.url()
        if self.base_url and target.startswith('/'):
            target = f'{self.base_url}{target}'
        self.page.goto(target, wait_until="domcontentloaded")
        return self

    def get_page(self, page_cls: Type[T]) -> T:
        return page_cls(self.page)
