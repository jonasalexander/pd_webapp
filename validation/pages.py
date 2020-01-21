from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from captcha.fields import ReCaptchaField


class Validation(Page):
    __allow_custom_attributes = True
    form_model = 'player'
    form_fields = []

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields['captcha'] = ReCaptchaField()
        return frm

page_sequence = [Validation]
