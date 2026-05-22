import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class CreateProjectPage(BasePage):
    def url(self):
        return "/createProject.html"

    @property
    def project_name_input(self):
        return self.page.locator('[data-test="project-name-input"]')

    @property
    def project_id_input(self):
        return self.page.locator('[data-test="project-id-input"]')

    @property
    def create_button(self):
        return self.page.locator('button[type="submit"]', has_text="Create")

    @property
    def cancel_button(self):
        return self.page.locator('button[type="button"]', has_text="Cancel")

    @property
    def page_title(self):
        return self.page.locator("h1.PageTitle-module__title--gU")

    def fill_project_name(self, name: str):
        with allure.step(f"Ввести название проекта: '{name}'"):
            self.project_name_input.fill(name)
        return self

    def fill_project_id(self, project_id: str):
        with allure.step(f"Ввести Project ID: '{project_id}'"):
            self.project_id_input.fill(project_id)
        return self

    def click_create(self):
        with allure.step("Нажать кнопку Create"):
            self.create_button.wait_for(state="visible")
            expect(self.create_button).to_be_enabled()
            self.create_button.click()
        return self

    def check_create_page_opened(self):
        with allure.step("Проверить что открыта страница создания проекта"):
            expect(self.page_title).to_be_visible()
            expect(self.page_title).to_have_text(UiAlert.NEW_PROJECT_TEXT)
        return self

