from django.apps import apps
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractCurrency(models.Model):
    code = models.CharField(
        _('currency code'), max_length=10, unique=True,
        help_text=_('fake currency code real currency')
    )
    name = models.CharField(
        _('currency name'), max_length=128,
        help_text=_('currency name to be shown as caption')
    )
    numeric = models.CharField(
        _('currency numeric for real currency'), max_length=3,
        null=True, blank=True,
        help_text=_('Currency numeric for real currency. (nullable)')
    )
    countries = JSONField(
        _('countries'), null=True, blank=True,
        help_text=_('Countries the currency is used in')
    )

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')
        ordering = ('code', )
        abstract = True

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"<{self.Meta.verbose_name}:{self.code}>"

    def __hash__(self):
        hash(self.code)

    def __eq__(self, other):
        return type(self) is type(other) and self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)


class Currency(AbstractCurrency):
    class Meta(AbstractCurrency.Meta):
        pass


def get_currency_model() -> Currency.__class__:
    app_name, model_name = settings.FAKEMONEY_CURRENCY_MODEL.split('.')
    return apps.get_model(app_name, model_name)


class AbstractFakeMoneyModel(models.Model):
    """Use this abstract model to define a model with amount and currency
    """
    currency = models.ForeignKey(
        settings.FAKEMONEY_CURRENCY_MODEL, on_delete=models.CASCADE,
        verbose_name=_('currency'),
        help_text=_('this can be real world currency or virtual currency.'))
    amount = models.DecimalField(
        _('amount'), default=0, max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class DemoFakeMoneyModelBase(AbstractFakeMoneyModel):
    class Meta:
        verbose_name = _('demo fake money')
        verbose_name_plural = _('demo fake monies')
