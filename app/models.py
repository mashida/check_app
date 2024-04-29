import logging

from django.db import models

logger = logging.getLogger(__name__)

class NumberRange(models.Model):
    code = models.IntegerField()
    from_number = models.IntegerField()
    to_number = models.IntegerField()
    capacity = models.IntegerField()
    operator = models.CharField(max_length=255)
    region = models.CharField()
    # Additional fields
    territory_gar = models.CharField(blank=True, null=True)
    inn = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.from_number} - {self.to_number} ({self.operator}, {self.region})"

    @classmethod
    def get_operator_and_region(cls, number):
        logger.debug(f"running get_operator_and_region_function..")
        try:
            # Extract the code and the rest of the number
            code, rest_number = str(number)[1:4], str(number)[4:]
            rest_number = int(rest_number)
            logger.debug(f"{code=} | {rest_number=}")
            # Find the range that matches the code and contains the rest of the number
            range_obj = cls.objects.filter(code=code, from_number__lte=rest_number, to_number__gte=rest_number).first()
            if range_obj:
                return range_obj.operator, range_obj.region
            else:
                return None, None
        except ValueError:
            # Handle the case where the number cannot be converted to an integer
            return None, None

