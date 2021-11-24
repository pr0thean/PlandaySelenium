import pytest
from ..plan_day.plan_day_app import PlanDayApp
import logging


@pytest.fixture
def init_plan_day():
    """
    :brief: Fixture to initialize plan_day module
    """
    plan_day = PlanDayApp()
    logging.info("Trying to init Login main page")
    return plan_day


@pytest.fixture
def init_browser(init_plan_day):
    """
    :brief: Fixture to initialize and close browser
    """
    init_plan_day.init_app()
    yield
    logging.info("Trying to close session")
    init_plan_day.close_app()
