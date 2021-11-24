import logging

from .config_handler import ConfigHandler
from .pages.planday_pages.login_page.pd_login_page import PlanDayLoginPage


class PlanDayApp(PlanDayLoginPage):
    def __init__(self):
        self.config_handler = ConfigHandler()
        super().__init__(config_handler=self.config_handler)

    def _initialize(self) -> 'PlanDayApp':
        logging.info("Trying to initialize PlanDayApp")
        return self

    def init_app(self):
        logging.info("Trying to lunch web PlanDay app")
        self.launch_app()
        return super()._initialize()
