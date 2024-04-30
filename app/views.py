import logging
from django.shortcuts import render
from django.http import JsonResponse
from .forms import MobileNumberForm
from .models import NumberRange
import json

logger = logging.getLogger(__name__)

def check_mobile_number(request):
    if request.method == 'POST':
        form = MobileNumberForm(request.POST)
        logger.debug(f"form is {'not ' if not form.is_valid() else ''}valid..")
        if form.is_valid():
            number = form.cleaned_data['number']
            operator, region = NumberRange.get_operator_and_region(number)
            if operator and region:
                context = {
                    'form': form,
                    'number': number,
                    'operator': operator,
                    'region': region,
                }
                logger.debug(f"{context=}")
                logger.debug(f"{operator=} | {region=}")
                return render(request, 'check_app/result.html', context)
            else:
                context = {
                    'form': form,
                    'error': 'Number onot found',
                }
                logger.debug(f"{context=}")
                logger.error(f"number not found")
                return render(request, 'check_app/result.html', context)
    else:
        form = MobileNumberForm()
    return render(request, 'check_app/index.html', {'form': form})

