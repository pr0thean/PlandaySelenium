import logging
from abc import ABCMeta
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .pd_web_controls import WebControl


class PlanDayBaseAbstractClass(metaclass=ABCMeta):
    def __init__(self,
                 config_handler,
                 page_initializer_control):
        self.config_handler = config_handler
        self._page_initializer_control = page_initializer_control
        self._page_name = self.__class__.__name__
        self._initialize()

    @property
    def _driver(self):
        return self.config_handler._driver

    @property
    def page_window_size(self):
        return self.config_handler.page_window_size

    @property
    def executable_path(self):
        return self.config_handler.executable_path

    @property
    def base_page_url(self):
        return self.config_handler.base_page_url

    def _initialize(self):
        if self._verify_app_page_body():
            logging.info(f"Successfully initialized page {self._page_name}")
            return self

    def _verify_app_page_body(self) -> bool:
        if self._wait_for_element(web_control=self._page_initializer_control):
            return True
        else:
            return False

    def launch_app(self, timeout: int = 10):
        chrome_options = Options()
        chrome_options.add_argument(self.page_window_size)
        self.config_handler._driver = webdriver.Chrome(executable_path=self.executable_path, options=chrome_options)
        self._driver.maximize_window()
        self._driver.get(self.base_page_url)
        logging.info("Trying to wait for page to load")
        WebDriverWait(self.config_handler._driver, timeout=timeout).until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')
        return self._driver

    def close_app(self):
        return self._driver.close()

    def _get_element_locator_for_control(self,
                                         web_control: WebControl,
                                         locator_strategy: By = None):
        web_selector = None
        if locator_strategy:
            if locator_strategy == By.CLASS_NAME:
                web_selector = web_control.class_name
            elif locator_strategy == By.ID:
                web_selector = web_control.id
            elif locator_strategy == By.TAG_NAME:
                web_selector = web_control.tag_name
            elif locator_strategy == By.CSS_SELECTOR:
                web_selector = web_control.css_selector
        else:
            if web_control.id:
                locator_strategy = By.ID
                web_selector = web_control.id
            elif web_control.class_name:
                locator_strategy = By.CLASS_NAME
                web_selector = web_control.class_name
            elif web_control.tag_name:
                locator_strategy = By.TAG_NAME
                web_selector = web_control.tag_name
            elif web_control.css_selector:
                locator_strategy = By.CSS_SELECTOR
                web_selector = web_control.css_selector

        return locator_strategy, web_selector

    def _find_element(
            self,
            web_control: WebControl,
            locator_strategy: By = None) -> WebElement:

        locator_strategy, element_selector = self._get_element_locator_for_control(web_control=web_control,
                                                                                   locator_strategy=locator_strategy)
        element = self._driver.find_element(locator_strategy, element_selector)
        return element

    def _find_elements(
            self,
            web_control: WebControl,
            locator_strategy: By = None) -> list:

        locator_strategy, element_selector = self._get_element_locator_for_control(web_control=web_control,
                                                                                   locator_strategy=locator_strategy)
        elements = self._driver.find_elements(locator_strategy, element_selector)
        return elements

    def _locate_element_with_expected_condition(
            self,
            web_control: WebControl,
            expected_condition = expected_conditions.visibility_of_element_located,
            locator_strategy: By = None,
            timeout: int = 4) -> WebElement:
        locator_strategy, element_selector = self._get_element_locator_for_control(web_control,
                                                                                   locator_strategy=locator_strategy
                                                                                   )
        element = WebDriverWait(
            driver=self._driver,
            timeout=timeout
        ).until(expected_condition((locator_strategy, element_selector)))
        return element

    def _wait_for_element(self,
                          web_control: WebControl,
                          locator_strategy: By = None,
                          timeout: int = 6,
                          ) -> WebElement:
        return self._locate_element_with_expected_condition(web_control=web_control,
                                                            timeout=timeout,
                                                            locator_strategy=locator_strategy)

    def _wait_for_number_of_elements_to_load(self,
                                             web_control: WebControl,
                                             expected_number_of_elements: int,
                                             timeout: int = 6):
        self._wait_for_element(web_control=web_control)
        number_of_located_elements = int(len(self._find_elements(web_control=web_control)))
        start_time = datetime.now().second
        while number_of_located_elements < expected_number_of_elements:
            number_of_located_elements = int(len(self._find_elements(web_control=web_control)))
            new_time = datetime.now().second
            if new_time-start_time >= timeout:
                break

    def _is_element_enable(self,
                           web_control: WebControl) -> bool:
        return self._find_element(web_control).is_enabled()

    def _wait_for_enable(self,
                         web_control: WebControl,
                         locator_strategy: By = None,
                         timeout: int = 4) -> WebElement:
        return self._locate_element_with_expected_condition(
            web_control=web_control,
            locator_strategy=locator_strategy,
            expected_condition=expected_conditions.element_to_be_clickable,
            timeout=timeout)

    def _wait_for_element_to_disappear(self,
                                       web_control: WebControl,
                                       locator_strategy: By = None,
                                       timeout: int = 5
                                       ) -> bool:

        element_locator = self._get_element_locator_for_control(web_control=web_control,
                                                                locator_strategy=locator_strategy
                                                                )
        if self._is_element_displayed(web_control):
            try:
                WebDriverWait(driver=self._driver, timeout=timeout).until_not(
                    expected_conditions.visibility_of_element_located(element_locator))
            except (NoSuchElementException, TimeoutException) as exception:
                raise exception
            else:
                return True
        else:
            return True

    def _is_element_displayed(self, web_control: WebControl) -> bool:
        return self._find_element(web_control=web_control).is_displayed()

    def _clear_text(self, web_control: WebControl):
        self._find_element(web_control=web_control).clear()

    def _click(self, web_control: WebControl):
        self._find_element(web_control=web_control).click()

    def _enter_text(self, web_control: WebControl, text: (str, int)):
        self._clear_text(web_control=web_control)
        self._find_element(web_control=web_control).send_keys(text)

    def _get_element_text(self, web_control: WebControl) -> str:
        return self._find_element(web_control=web_control).text

    def _get_element_attribute(self, web_control: WebControl, attribute: str):
        return self._find_element(web_control=web_control).get_attribute(attribute)

    def _get_page_url(self):
        return self._driver.current_url

    def _get_page_title(self):
        return self._driver.title

    def _switch_to_iframe(self, web_control: WebControl):
        iframe_element_to_switch = self._wait_for_element(web_control=web_control)
        self._driver.switch_to.frame(iframe_element_to_switch)

    def _switch_from_iframe_to_default(self):
        self._driver.switch_to.default_content()

    def _hover_on_element(self, web_control: WebControl):
        element = self._find_element(web_control=web_control)
        hover = ActionChains(self._driver).move_to_element(element)
        hover.perform()
