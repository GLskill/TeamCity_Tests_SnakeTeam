import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class QueuePanel(BasePage):
    def url(self):
        return "/queue"

    @property
    def queue_page_text(self):
        return self.page.locator("h1.QueuePageHeader-module__header--dj")

    def check_queue_page(self):
        with allure.step("Проверить наличие текста 'Builds in queue' на странице очереди"):
            expect(self.queue_page_text).to_be_visible()
            expect(self.queue_page_text).to_have_text(UiAlert.QUEUE)
        return self
