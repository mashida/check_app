import logging

from django.shortcuts import render
from .forms import MobileNumberForm
from .models import NumberRange

logger = logging.getLogger(__name__)

def check_mobile_number(request):
    if request.method == 'POST':
        form = MobileNumberForm(request.POST)
        logger.debug(f"form is {'not ' if not form.is_valid() else ''}valid..")
        if form.is_valid():
            number = form.cleaned_data['number']
            operator, region = NumberRange.get_operator_and_region(number)
            if operator and region:
                return render(request, 'check_app/result.html', {'operator': operator, 'region': region})
            else:
                return render(request, 'check_app/result.html', {'error': 'Number not found'})
    else:
        form = MobileNumberForm()
    return render(request, 'check_app/index.html', {'form': form})

