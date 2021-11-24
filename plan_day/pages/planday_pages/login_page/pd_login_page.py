import logging

from ..home_page.pd_main_home_page import PlanDayMainHomePage
from ...pd_base_pages import PlanDayBaseAbstractClass
from ...pd_web_controls import WebControl


class PlanDayLoginPage(PlanDayBaseAbstractClass):
    def __init__(self, config_handler):
        self.config_handler = config_handler

        # cookies banner
        self._cookies_banner_header_description_control = WebControl(id="cookie-banner"
)
        self._cookies_banner_ok_button_control = WebControl(
            class_name='button-success'
        )

        # login form
        self._login_form_main_control = WebControl(
            class_name='login-form'
        )
        self._login_form_email_input_control = WebControl(
            id="Username"
        )
        self._login_form_password_input_control = WebControl(
            id='Password'
        )
        self._login_form_log_in_button_control = WebControl(
            id='MainLoginButton'
        )
        self._login_form_incorrect_user_name_control = WebControl(
            id='Username-validation-error'
        )
        self._login_form_incorrect_password_control = WebControl(
            id='Username-validation-error'
        )

        self.employee_details_before_update = None
        self.employee_details_after_update = None
        self.number_of_shift_from_header_before_update = None
        self.number_of_shift_from_header_after_update = None
        super().__init__(config_handler=self.config_handler,
                         page_initializer_control=self._login_form_main_control)

    def _initialize(self):
        if self._wait_for_element(web_control=self._cookies_banner_header_description_control):
            self.confirm_banner_with_cookies()
        return super()._initialize()

    def confirm_banner_with_cookies(self):
        logging.info("Trying to confirm CookiesBanner popup")
        self._click(web_control=self._cookies_banner_ok_button_control)

    def fill_login_form(self, username: str, password: str):
        logging.info(f"Trying to fill login form with following credentials: {username}, {password}")
        self._enter_text(web_control=self._login_form_email_input_control, text=username)
        self._enter_text(web_control=self._login_form_password_input_control, text=password)

    def log_in_with_correct_credentials(self, username: str, password: str):
        logging.info(f"Trying to login user with correct credentials: {username}, {password}")
        self.fill_login_form(username=username, password=password)
        self._click(self._login_form_log_in_button_control)
        return PlanDayMainHomePage(config_handler=self.config_handler)

    def log_in_with_incorrect_credentials(self, username: str, password: str):
        logging.info(f"Trying to login user with incorrect credentials: {username}, {password}")
        self.fill_login_form(username=username, password=password)
        self._click(self._login_form_log_in_button_control)
        return self

    def verify_incorrect_credentials_message(self) -> bool:
        incorrect_credentials_message_const = "The username or password is incorrect."
        logging.info(f"Trying to verify if message about incorrect credentials is present and equal to "
                     f"'{incorrect_credentials_message_const}'")
        incorrect_username_message = self._get_element_text(self._login_form_incorrect_user_name_control)
        incorrect_password_message = self._get_element_text(self._login_form_incorrect_password_control)
        return incorrect_username_message == incorrect_credentials_message_const and \
            incorrect_password_message == incorrect_credentials_message_const
