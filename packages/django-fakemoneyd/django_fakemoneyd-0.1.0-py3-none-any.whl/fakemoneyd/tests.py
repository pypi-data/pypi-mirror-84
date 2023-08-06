from typing import List
from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Currency, DemoFakeMoneyModelBase


class ModelTestCase(TestCase):
    def __create_currency(
        self,
        code: str, name: str, numeric: str,
        countries: List[str] = []
    ) -> Currency:
        return Currency.objects.create(
            code=code, name=name, numeric=numeric,
            countries=countries
        )

    def test_currency(self):
        usd = self.__create_currency('usd', 'US Dollar', '123', ['USA'])
        eur = self.__create_currency('eur', 'Euro', '124', ['EU'])

        self.assertEqual(usd.code, 'usd')
        self.assertEqual(usd.name, 'US Dollar')
        self.assertEqual(usd.numeric, '123')

        self.assertEqual(eur.code, 'eur')
        self.assertEqual(eur.name, 'Euro')
        self.assertEqual(eur.numeric, '124')

        self.assertNotEqual(usd, eur)

        self.assertListEqual(usd.countries, ['USA'])
        self.assertRaises(
            IntegrityError,
            lambda: self.__create_currency('usd', 'US Dollar', '123', ['USA'])
        )

    def __create_demo_money_row(self, currency: Currency, amount: float):
        return DemoFakeMoneyModelBase.objects.create(
            currency=currency, amount=amount
        )

    def test_money_model(self):
        usd = Currency.objects.create(
            code='usd', name='US Dollar', numeric='123',
            countries=['USA'])
        eur = Currency.objects.create(
            code='eur', name='Euro', numeric='124',
            countries=['EU'])

        row1 = self.__create_demo_money_row(usd, 100)
        row2 = self.__create_demo_money_row(eur, 200)

        self.assertEqual(row1.currency.code, 'usd')
        self.assertEqual(row1.amount, 100)

        self.assertEqual(row2.currency.code, 'eur')
        self.assertEqual(row2.amount, 200)
