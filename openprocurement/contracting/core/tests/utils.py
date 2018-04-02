# -*- coding: utf-8 -*-
import unittest

from mock import MagicMock, patch
from pyramid.request import Request
from schematics.types import StringType

from openprocurement.contracting.core.models import Contract as BaseContract
from openprocurement.contracting.core.utils import isContract, \
    register_contract_contractType, apply_patch, set_ownership


class Contract(BaseContract):
    contractType = StringType(choices=['esco', 'common'], default='common')


class TestisContract(unittest.TestCase):
    """ isContract tests"""

    def setUp(self):
        self.test_value = 'test_value'
        self.isContract = isContract(self.test_value, None)

    def test_init(self):
        self.assertEqual(self.test_value, self.isContract.val)

    def test_text(self):
        self.assertEqual(self.isContract.text(),
                         'contractType = %s' % (self.test_value,))

    def test_call(self):
        contract = Contract()
        request = Request(dict())

        request.contract = None
        self.assertEqual(self.isContract(None, request), False)

        request.contract = Contract()
        self.assertEqual(self.isContract(None, request), False)

        request.contract.contractType = 'common'
        self.isContract.val = 'common'
        self.assertEqual(self.isContract(None, request), True)


class TestUtilsFucntions(unittest.TestCase):
    """Testing all functions inside utils.py"""

    def test_register_contract_contractType(self):
        config = MagicMock()
        config.registry.contract_contractTypes = {}

        self.assertEqual(config.registry.contract_contractTypes, {})
        register_contract_contractType(config, Contract)
        common = config.registry.contract_contractTypes.get(
            'common'
        )
        self.assertEqual(common, Contract)

    @patch('openprocurement.contracting.core.utils.save_contract',
           return_value=True)
    @patch('openprocurement.contracting.core.utils.apply_data_patch')
    def test_apply_patch(self, mocked_apply_data_patch, mocked_save_contract):
        request = MagicMock()
        request.context = Contract()
        data = {'status': 'draft'}
        mocked_apply_data_patch.return_value = False
        self.assertEqual(apply_patch(request, data=data), None)

        mocked_apply_data_patch.return_value = request.context
        self.assertEqual(apply_patch(request, data=data, save=False), None)

        self.assertEqual(apply_patch(request, data=data, save=True), True)

    def test_set_ownership(self):
        item = MagicMock()
        set_ownership(item, None)
        self.assertIsNotNone(item.owner_token)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestisContract))
    suite.addTest(unittest.makeSuite(TestUtilsFucntions))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
