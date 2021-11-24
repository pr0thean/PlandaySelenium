import logging

from ..schedule_page.pd_schedule_page import PlanDaySchedulePage
from ...pd_base_pages import PlanDayBaseAbstractClass
from ...pd_web_controls import WebControl


class PlanDayMainHomePage(PlanDayBaseAbstractClass):
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self._main_page_iframe_control = WebControl(
            tag_name='iframe'
        )
        self._navigation_bar_schedule_main_section_control = WebControl(
            css_selector="a[href='/page/schedule']"
        )
        self._navigation_bar_schedule_sub_section_control = WebControl(
            css_selector="a[href='/page/schedule-1']"
        )
        self._main_page_home_control = WebControl(
            class_name='basic-toolbar-title'
        )
        super().__init__(config_handler=self.config_handler,
                         page_initializer_control=self._main_page_iframe_control)

    def _initialize(self):
        self._switch_to_iframe(web_control=self._main_page_iframe_control)
        if self._wait_for_element(web_control=self._main_page_home_control):
            self._switch_from_iframe_to_default()
        return super()._initialize()

    def navigate_to_schedule_page(self):
        logging.info("Trying to navigate from Main page to Schedule page")
        self._hover_on_element(web_control=self._navigation_bar_schedule_main_section_control)
        self._click(web_control=self._navigation_bar_schedule_sub_section_control)
        return PlanDaySchedulePage(config_handler=self.config_handler)

    def verify_main_home_page_url(self, sub_url: str) -> bool:
        logging.info(f"Trying to verify if Home page url contains sub_url: {sub_url}")
        current_page_url = self._get_page_url()
        if current_page_url.find(sub_url) != -1:
            return True
        return False
