import logging

from django import forms
from .models import NumberRange

logger = logging.getLogger(__name__)

class MobileNumberForm(forms.Form):
    number = forms.CharField(max_length=20)
    logger.debug(f"{number}")

    def clean_number(self):
        number = self.cleaned_data.get('number')
        
        code, number_part = number[1:4], number[4:]
        logger.debug(f"{code=} | {number_part=}")
        try:
            number_part = int(number_part)
            # Adjust the query to filter based on the extracted code
            range_obj = NumberRange.objects.filter(code=code, from_number__lte=number_part, to_number__gte=number_part).first()
            if not range_obj:
                raise forms.ValidationError("Number not found in our database or does not match the code.")
        except ValueError:
            raise forms.ValidationError("Invalid number format.")
        return number
