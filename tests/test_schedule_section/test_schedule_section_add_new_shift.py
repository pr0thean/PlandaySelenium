import logging
import pytest
import random
import string
from .user_account import username_correct, password_correct


class TestScheduleAddNewShift:

    @pytest.mark.usefixtures('init_browser')
    def test_schedule_section_add_today_new_shift_possible(self, init_plan_day):
        """
        @brief: Test case verifying if user can add new shift for employee for today.
        @precondition:
                  - user for test already created
        """

        logging.info("Log in already existing user with incorrect credentials")
        init_plan_day.log_in_with_incorrect_credentials(
            username=username_correct,
            password=''.join(random.choice(string.ascii_lowercase) for _ in range(15)))
        logging.info("Verify presence of message about incorrect credentials")
        assert init_plan_day.verify_incorrect_credentials_message()
        logging.info("Log in already existing user with correct credentials")
        home_page = init_plan_day.log_in_with_correct_credentials(
            username=username_correct,
            password=password_correct)
        logging.info("Navigate to 'Schedule' page from main navigation bar")
        schedule_page = home_page.navigate_to_schedule_page()
        logging.info("Verify if 'Schedule' page url contains substring")
        assert schedule_page.verify_schedule_page_url(sub_url="/page/schedule")
        logging.info("Verify if number of displayed employee is correct")
        assert schedule_page.verify_if_correct_number_of_employees(expected_number_of_employees=3)
        logging.info("Verify shown week interval period of time")
        assert schedule_page.verify_shown_week_interval_correctness()
        logging.info("Add standard shift for employee for today")
        schedule_page.add_employee_shift_for_today(
            employee_for_add_shift="Employee One",
            shift_start_hour=9,
            shift_end_hour=17)
        logging.info("Verify if shift is added for today for given employee")
        assert schedule_page.check_if_new_shift_added(employee_for_add_shift="Employee One")
