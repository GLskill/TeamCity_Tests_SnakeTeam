import allure

from playwright.sync_api import expect
from src.ui.pages.base_page import BasePage


class MntStartedPage(BasePage):
    def url(self):
        return "/mnt"

    @property
    def page_banner_on_step1(self):
        return self.page.get_by_role("heading", name="TeamCity First Start")

    @property
    def page_banner_on_step2_database(self):
        return self.page.get_by_role("heading", name="Database connection setup")

    @property
    def page_banner_on_step3_license_agreement(self):
        return self.page.get_by_role("heading", name="License Agreement")

    @property
    def page_banner_on_step4_teamcity_starting(self):
        return self.page.get_by_role("heading", name="TeamCity is starting")

    @property
    def proceed_button(self):
        return self.page.get_by_role("button", name="Proceed")

    @property
    def restore_from_backup(self):
        return self.page.get_by_role("button", name="Restore from backup")

    @property
    def accept_license_button(self):
        return self.page.get_by_role("button", name="Accept")

    def check_first_start_page_open(self):
        with allure.step("Проверить что страница первого старта откртыа"):
            expect(self.page_banner_on_step1).to_be_visible()

    def check_db_page2_open(self):
        with allure.step("Проверить что страница изменилась на настрйоку бзаы"):
            expect(self.page_banner_on_step2_database).to_be_visible()

    def check_license_agreement_page3_open(self):
        with allure.step("Проверить что страница изменилась на принятие лицензии"):
            expect(self.page_banner_on_step3_license_agreement).to_be_visible()

    def check_page_banner_page4_open(self):
        with allure.step("Проверить что страница изменилась на настройку тимсити"):
            expect(self.page_banner_on_step4_teamcity_starting).to_be_visible()

    def click_proceed_button(self):
        with allure.step("Нажать кнопку Proceed"):
            self.proceed_button.click()
        return self

    def click_backup_button(self):
        with allure.step("Нажать кнопку Backup"):
            self.restore_from_backup.click()
        return self

    def click_accept_license_button(self):
        with allure.step("Нажать кнопку Accept"):
            self.accept_license_button.click()
        return self

    def accept_first_start(self):
        self.check_first_start_page_open()
        self.click_proceed_button()
        return self

    def accept_database_setup(self):
        self.check_db_page2_open()
        self.click_proceed_button()
        return self

    def accept_license_agreement(self):
        self.check_license_agreement_page3_open()
        self.click_accept_license_button()
        return self
