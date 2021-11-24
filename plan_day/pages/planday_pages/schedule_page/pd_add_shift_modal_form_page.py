from ...pd_base_pages import PlanDayBaseAbstractClass
from ...pd_web_controls import WebControl
import logging


class PlanDayAddShiftModalFormPage(PlanDayBaseAbstractClass):
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self._add_shift_modal_view_control = WebControl(
            class_name='edit-shift-modal__box'
        )
        self._shift_start_hour_modal_view_input_control = WebControl(
            id='shiftStartEnd_start'
        )
        self._shift_end_hour_modal_view_input_control = WebControl(
            id='shiftStartEnd_end'
        )
        self._create_shift_modal_view_button_control = WebControl(
            class_name='button--primary'
        )

        super().__init__(config_handler=self.config_handler,
                         page_initializer_control=self._add_shift_modal_view_control)

    def _verify_if_modal_view_closed(self):
        from .pd_schedule_page import PlanDaySchedulePage
        self._switch_from_iframe_to_default()
        return PlanDaySchedulePage(config_handler=self.config_handler)

    def fill_modal_form_to_add_employee_shift(self, shift_start_hour: int, shift_end_hour: int):
        logging.info(f"Trying to fill and accept modal form with shift details: shift start hour: {shift_start_hour} "
                     f"and shift end hour: {shift_end_hour}")
        self._enter_text(web_control=self._shift_start_hour_modal_view_input_control,
                         text=shift_start_hour)
        self._enter_text(web_control=self._shift_end_hour_modal_view_input_control,
                         text=shift_end_hour)
        self._click(web_control=self._create_shift_modal_view_button_control)
        return self._verify_if_modal_view_closed()
