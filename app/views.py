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
                # Prepare JSON data
                json_data = json.dumps({'operator': operator, 'region': region})
                # Pass the JSON data to the template context
                context = {
                    'form': form,
                    'json_data': json_data,
                }
                return render(request, 'check_app/result.html', context)
            else:
                # Prepare JSON data for error
                json_data = json.dumps({'error': 'Number not found'})
                context = {
                    'form': form,
                    'json_data': json_data,
                }
                return render(request, 'check_app/result.html', context)
    else:
        form = MobileNumberForm()
    return render(request, 'check_app/index.html', {'form': form})

