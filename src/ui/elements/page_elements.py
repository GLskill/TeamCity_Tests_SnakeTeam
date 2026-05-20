from __future__ import annotations
from playwright.sync_api import Page


class PageElements:
    def __init__(self, page: Page):
        self.page = page

    @property
    def projects_button(self):
        return self.page.locator('[data-test-title="Projects"]')

    @property
    def changes_button(self):
        return self.page.locator('[data-test-title="Changes"]')

    @property
    def agents_button(self):
        return self.page.locator('a[data-test="ring-link"][href*="/agents"]')

    @property
    def queue_button(self):
        return self.page.locator('[data-test-title*="Queue"]')

    @property
    def administration_button(self):
        return self.page.locator('[data-test-title="Administration"]')

    @property
    def my_investigations_button(self):
        return self.page.locator('[data-test-title*="My Investigations"]')

    @property
    def whats_new_button(self):
        return self.page.locator('[data-test-title="What\'s New"]')

    @property
    def help_button(self):
        return self.page.locator('[data-test-title="Help"]')

    @property
    def account_menu_button(self):
        return self.page.locator('[data-hint-container-id="header-user-menu"]')

    @property
    def account_menu_profile(self):
        return self.page.locator('[id*="profile.html"]')

    @property
    def account_menu_appearance(self):
        return self.page.locator('[id*="Appearance"]')

    @property
    def account_menu_favorite_builds(self):
        return self.page.locator('[id*="/favorite/builds"]')

    @property
    def account_menu_logout(self):
        return self.page.locator('[id*="logout"]')

    @property
    def switch_to_classic_ui_button(self):
        return self.page.locator('a[title="Switch to Classic UI"]')

    def click_projects(self):
        self.projects_button.click()

    def click_changes(self):
        self.changes_button.click()

    def click_agents(self):
        self.agents_button.click()

    def click_queue(self):
        self.queue_button.click()

    def click_administration(self):
        self.administration_button.click()

    def click_my_investigations(self):
        self.my_investigations_button.click()

    def click_whats_new(self):
        self.whats_new_button.click()

    def click_help(self):
        self.help_button.click()

    def go_to_profile(self):
        self.account_menu_button.click()
        self.account_menu_profile.click()

    def go_to_appearance(self):
        self.account_menu_button.click()
        self.account_menu_appearance.click()

    def go_to_favorite_builds(self):
        self.account_menu_button.click()
        self.account_menu_favorite_builds.click()

    def go_to_logout(self):
        self.account_menu_button.click()
        self.account_menu_logout.click()

    def go_to_classic_ui(self):
        self.switch_to_classic_ui_button.click()