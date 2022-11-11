from django.db import models


class ExpirationDays(models.IntegerChoices):
    ONE = 1, '1 დღიანი'
    TWO = 2, '2 დღიანი'
    WEEK = 7, '1 კვირიანი'
    MONTH = 30, '1 თვიანი'
    THREE_MONTH = 90, '3 თვიანი'
    SIX_MONTH = 180, '6 თვიანი'
    YEAR = 365, '1 წლიანი'
    TWO_YEAR = 730, '2 წლიანი'
