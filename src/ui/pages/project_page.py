import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class ProjectPanel(BasePage):
    def url(self):
        return "/favorite/projects"

    @property  # Приветственный текст когда нету проектов
    def project_wellcome_text(self):
        return self.page.get_by_role("heading", name="Welcome to TeamCity")

    @property  # Точно было не помню когда ....
    def all_projects_text(self):
        return self.page.locator("span", has_text="All Projects")

    @property  # Текст если есть уже созданый проект
    def favorite_projects_text(self):
        return self.page.locator("span", has_text="Favorite Projects")

    @property  # Кнопка #1 - только когда проектов нет
    def admin_create_project_wellcome_button(self):
        return self.page.locator('[data-test="create-project"]')

    @property  # Кнопка #2 - всегда в сайдбаре
    def admin_create_project_main_button(self):
        return self.page.locator('[data-test="ring-tooltip"][data-test-title="Create"] a')

    @property  # Кнопка #3 - акутивно только когда есть проект в сисетеме, открывает дропдаун лист
    def admin_create_project_dropdown_button(self):
        return self.page.locator('[data-hint-container-id="project-create-entity"]')

    @property  # Пункт "New project" внутри дропдауна кнопки #3
    def admin_create_project_with_dropdown_button(self):
        return self.page.locator('[data-test="ring-list-item-label"]', has_text="New project")

    @property
    def create_new_project_page(self):
        return self.page.locator("h1.PageTitle-module__title--gU")

    def check_new_project_create_page(self):
        with allure.step("Проверить наличее текста 'New Project' "):
            expect(self.create_new_project_page).to_be_visible()
            expect(self.create_new_project_page).to_have_text(UiAlert.NEW_PROJECT_TEXT)

    def check_welcome_or_favorite(self):
        with allure.step("Проверить что мы на странице проектов"):
            expect(self.project_wellcome_text.or_(self.favorite_projects_text)).to_be_visible()
        return self

    def click_create_project_wellcome_button(self):
        self.admin_create_project_wellcome_button.click()
        return self

    def click_create_project_main_button(self):
        self.admin_create_project_main_button.click()
        return self

    def click_create_project_dropdown_button(self):
        self.admin_create_project_dropdown_button.click()
        self.admin_create_project_with_dropdown_button.click()
        return self
