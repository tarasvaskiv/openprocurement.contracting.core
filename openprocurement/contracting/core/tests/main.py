# -*- coding: utf-8 -*-
import unittest

from pyramid.config import Configurator
from pyramid.request import Request

from openprocurement.contracting.core.adapters import ContractConfigurator
from openprocurement.contracting.core.models import Contract
from openprocurement.contracting.core.includeme import includeme
from openprocurement.contracting.core.utils import isContract
from openprocurement.api.interfaces import IContentConfigurator


class TestIncludeme(unittest.TestCase):
    """Test if plugin load works correct"""

    def setUp(self):
        self.contract = Contract()
        self.request = Request(dict())
        self.config = Configurator(settings={'plugins': 'fake_plugin'})
        self.config.include("cornice")

    def test_includeme(self):
        includeme(self.config)

        self.assertEquals(self.config.registry.contract_contractTypes, {})

        #  check if config has attribute add_contract_contractType,
        #  if config doesnt have getattr raises exception
        self.assertIsNotNone(getattr(self.config, 'add_contract_contractType'))

        #  check if adapter is registered
        adapter = self.config.registry.queryMultiAdapter(
            (self.contract, self.request),
            IContentConfigurator
        )
        self.assertIsInstance(adapter, ContractConfigurator)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIncludeme))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
