import logging
from copy import deepcopy
from datetime import datetime

from .pd_add_shift_modal_form_page import PlanDayAddShiftModalFormPage
from ...pd_base_pages import PlanDayBaseAbstractClass
from ...pd_web_controls import WebControl


class PlanDaySchedulePage(PlanDayBaseAbstractClass):
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self._schedule_page_iframe_control = WebControl(
            tag_name='iframe'
        )
        self._schedule_page_control = WebControl(
            class_name='board__cell'
        )
        self._header_grid_with_date = WebControl(
            class_name='board-header__cell'
        )
        self._schedule_menu_control = WebControl(
            class_name='scheduling__period-menu'
        )
        self._grid_slot = WebControl(
            class_name='board-slot'
        )

        # shift details from the grid
        self._all_rows_on_grid_control = WebControl(
            class_name='virtualized-board__row'
        )
        self._shift_on_grid_control = WebControl(
            class_name='shift-tile'
        )

        # employee details from left side columns
        self._employee_name_control = WebControl(
            class_name='row-header3__text__title'
        )
        self._employee_shift_details_control = WebControl(
            class_name='row-header3__subtitle-time'
        )
        self._employee_details_before_update = None
        self._employee_details_after_update = None
        self._number_of_shift_from_today_header_before_update = None
        self._number_of_shift_from_today_header_after_update = None
        super().__init__(config_handler=self.config_handler,
                         page_initializer_control=self._header_grid_with_date)

    def _initialize(self):
        self._switch_to_iframe(web_control=self._schedule_page_iframe_control)
        self._wait_for_number_of_elements_to_load(web_control=self._grid_slot, expected_number_of_elements=14)
        return super()._initialize()

#   basic page verification

    def verify_schedule_page_url(self, sub_url: str) -> bool:
        logging.info(f"Trying to verify if Schedule page url contains sub_url: {sub_url}")
        current_page_url = self._get_page_url()
        if current_page_url.find(sub_url) != -1:
            return True
        return False

    def verify_shown_week_interval_correctness(self, expected_interval: str = "Week") -> bool:
        logging.info(f"Trying to verify if shown on grid time interval equal to: {expected_interval}")
        time_interval_menu = self._get_element_text(web_control=self._schedule_menu_control)
        number_of_weekdays_grid = len(self._find_elements(web_control=self._header_grid_with_date))
        return time_interval_menu == expected_interval and number_of_weekdays_grid == 7

#   get grid details

    def _get_all_employee_details(self) -> list:
        all_employees_rows = self._find_elements(web_control=self._all_rows_on_grid_control)[1:]
        all_employees_with_details = []
        employee_details = {}

        for employee in all_employees_rows:
            employee_name = employee.find_element_by_class_name(self._employee_name_control.class_name).text
            employee_shift_details = employee.find_element_by_class_name(self._employee_shift_details_control.class_name).text
            grid_slots_with_shift = employee.find_elements_by_class_name(self._shift_on_grid_control.class_name)
            number_of_shifts_from_grid = len(grid_slots_with_shift)

            employee_details["name"] = employee_name
            employee_details["shift_info"] = employee_shift_details
            employee_details["number_of_shifts"] = number_of_shifts_from_grid
            all_employees_with_details.append(deepcopy(employee_details))
        return all_employees_with_details

    def verify_if_correct_number_of_employees(self, expected_number_of_employees: int):
        logging.info(f"Trying to verify if number of employees equal to: {expected_number_of_employees}")
        number_of_employees = int(len(self._get_all_employee_details()))
        return number_of_employees == expected_number_of_employees

    def verify_if_employee_exists_on_shifts_list(self, employee_name: str) -> bool:
        logging.info(f"Trying to verify if employee: {employee_name} exists on available employee list")
        if_exist = False
        for el in self._get_all_employee_details():
            if el['name'] == employee_name:
                if_exist = True
        return if_exist

#   add employee shift

    def click_on_today_cell_to_add_employee_shift(self, employee_for_add_shift: str = "Employee One"):
        logging.info(f"Trying to click on Today grid cell to add shift for employee: {employee_for_add_shift}")
        all_employees_rows = self._find_elements(web_control=self._all_rows_on_grid_control)[1:]
        for employee in all_employees_rows:
            employee_name = employee.find_element_by_class_name(self._employee_name_control.class_name).text
            if employee_name == employee_for_add_shift:
                employee.find_elements_by_class_name(self._grid_slot.class_name)[datetime.today().weekday()].click()
                return PlanDayAddShiftModalFormPage(config_handler=self.config_handler)

    def add_employee_shift_for_today(self,
                                     employee_for_add_shift: str,
                                     shift_start_hour: int,
                                     shift_end_hour: int):
        logging.info(f"Trying to add employee: {employee_for_add_shift} shift for today with following parameters: "
                     f"start of the shift: {shift_start_hour}, end of the shift: {shift_end_hour}")
        self._employee_details_before_update = self._get_all_employee_details()
        self._number_of_shift_from_today_header_before_update = self._get_today_number_of_shifts()

        add_shift_modal_page = self.click_on_today_cell_to_add_employee_shift(
            employee_for_add_shift=employee_for_add_shift)
        schedule_page = add_shift_modal_page.fill_modal_form_to_add_employee_shift(shift_start_hour=shift_start_hour,
                                                                                   shift_end_hour=shift_end_hour)

        self._employee_details_after_update = self._get_all_employee_details()
        self._number_of_shift_from_today_header_after_update = self._get_today_number_of_shifts()
        return schedule_page

    def check_if_new_shift_added(self, employee_for_add_shift: str):
        logging.info(f"Trying to check if shift is added for employee: {employee_for_add_shift}")
        # number of shifts before adding new shift
        employee_details_before = [el for el in self._employee_details_before_update if
                                   el['name'] == employee_for_add_shift][0]
        cards_with_shift_before = employee_details_before['number_of_shifts']
        shift_number_before_from_label_raw = employee_details_before['shift_info'].split('/')
        shift_number_before_from_label = int(shift_number_before_from_label_raw[1].strip()[0])
        shift_number_before_from_today_header = self._number_of_shift_from_today_header_before_update

        # number of shifts before after new shift
        employee_details_after = [el for el in self._employee_details_after_update if
                                  el['name'] == employee_for_add_shift][0]
        cards_with_shift_after = employee_details_after['number_of_shifts']

        shift_number_after_from_label_raw = employee_details_after['shift_info'].split('/')
        shift_number_after_from_label = int(shift_number_after_from_label_raw[1].strip()[0])
        shift_number_after_from_today_header = self._number_of_shift_from_today_header_after_update

        return cards_with_shift_before + 1 == cards_with_shift_after and  \
            shift_number_before_from_label + 1 == shift_number_after_from_label and \
            shift_number_before_from_today_header + 1 == shift_number_after_from_today_header

    def _get_today_number_of_shifts(self) -> int:
        today_header = "board-header__cell--today"
        today_header = self._driver.find_element_by_class_name(today_header)
        today_shift = today_header.find_element_by_class_name("board-header__details-counter").text[0]
        return int(today_shift)
