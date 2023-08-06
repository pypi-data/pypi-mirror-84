from django.contrib import admin

from .models import get_currency_model


CurrencyModel = get_currency_model()


@admin.register(CurrencyModel)
class CurrencyModelAdmin(admin.ModelAdmin):
    model = CurrencyModel
    list_display = ('code', 'name', 'numeric', )
