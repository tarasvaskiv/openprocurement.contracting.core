# -*- coding: utf-8 -*-
import os
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch

from openprocurement.contracting.core.tests.base import (
    test_contract_data,
    test_contract_data_wo_items,
    BaseWebTest,
    BaseContractWebTest,
    documents
)
from openprocurement.contracting.core.tests.contract_blanks import (
    # ContractTest
    simple_add_contract,
    # ContractResourceTest
    empty_listing,
    listing,
    listing_changes,
    get_contract,
    not_found,
    create_contract_invalid,
    create_contract_generated,
    create_contract,
    # ContractWDocumentsWithDSResourceTest
    create_contract_w_documents,
    # ContractResource4BrokersTest
    contract_status_change,
    contract_items_change,
    patch_tender_contract,
    # ContractResource4AdministratorTest
    contract_administrator_change,
    # ContractCredentialsTest
    get_credentials,
    generate_credentials,
    # ContractWOItemsResource4BrokersTest
    contract_wo_items_status_change,
)


class ContractResourceTest(BaseWebTest):
    relative_to = os.path.dirname(__file__)

    def test_empty_listing(self):
        response = self.app.get('/contracts')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], [])
        self.assertNotIn('{\n    "', response.body)
        self.assertNotIn('callback({', response.body)
        self.assertEqual(response.json['next_page']['offset'], '')
        self.assertNotIn('prev_page', response.json)

        response = self.app.get('/contracts?opt_jsonp=callback')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/javascript')
        self.assertNotIn('{\n    "', response.body)
        self.assertIn('callback({', response.body)

        response = self.app.get('/contracts?opt_pretty=1')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn('{\n    "', response.body)
        self.assertNotIn('callback({', response.body)

        response = self.app.get('/contracts?opt_jsonp=callback&opt_pretty=1')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/javascript')
        self.assertIn('{\n    "', response.body)
        self.assertIn('callback({', response.body)

        response = self.app.get('/contracts?offset=2015-01-01T00:00:00+02:00&descending=1&limit=10')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], [])
        self.assertIn('descending=1', response.json['next_page']['uri'])
        self.assertIn('limit=10', response.json['next_page']['uri'])
        self.assertNotIn('descending=1', response.json['prev_page']['uri'])
        self.assertIn('limit=10', response.json['prev_page']['uri'])

        response = self.app.get('/contracts?feed=changes')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], [])
        self.assertEqual(response.json['next_page']['offset'], '')
        self.assertNotIn('prev_page', response.json)

        response = self.app.get('/contracts?feed=changes&offset=0', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Offset expired/invalid', u'location': u'params', u'name': u'offset'}
        ])

        response = self.app.get('/contracts?feed=changes&descending=1&limit=10')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], [])
        self.assertIn('descending=1', response.json['next_page']['uri'])
        self.assertIn('limit=10', response.json['next_page']['uri'])
        self.assertNotIn('descending=1', response.json['prev_page']['uri'])
        self.assertIn('limit=10', response.json['prev_page']['uri'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContractResourceTest))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

@unittest.skipIf(True, "Move to lower package")
class ContractTest(BaseWebTest):
    initial_data = test_contract_data

    test_simple_add_contract = snitch(simple_add_contract)

# class ContractResourceTest(BaseWebTest):
#     """ contract resource test """
#     initial_data = test_contract_data
# 
#     test_empty_listing = snitch(empty_listing)
#     test_listing = snitch(listing)
#     test_listing_changes = snitch(listing_changes)
#     test_get_contract = snitch(get_contract)
#     test_not_found = snitch(not_found)
#     test_create_contract_invalid = snitch(create_contract_invalid)
#     test_create_contract_generated = snitch(create_contract_generated)
#     test_create_contract = snitch(create_contract)

@unittest.skipIf(True, "Move to lower package")
class ContractWDocumentsWithDSResourceTest(BaseWebTest):
    docservice = True
    initial_data = deepcopy(test_contract_data)
    documents = deepcopy(documents)
    initial_data['documents'] = documents

    test_create_contract_w_documents = snitch(create_contract_w_documents)


@unittest.skipIf(True, "Move to lower package")
class ContractResource4BrokersTest(BaseContractWebTest):
    """ contract resource test """
    initial_auth = ('Basic', ('broker', ''))

    test_contract_status_change = snitch(contract_status_change)
    test_contract_items_change = snitch(contract_items_change)
    test_patch_tender_contract = snitch(patch_tender_contract)


test_contract_data_wo_items = deepcopy(test_contract_data)
del test_contract_data_wo_items['items']


@unittest.skipIf(True, "Move to lower package")
class ContractWOItemsResource4BrokersTest(BaseContractWebTest):
    initial_data = test_contract_data_wo_items
    initial_auth = ('Basic', ('broker', ''))

    def test_contract_wo_items_status_change(self):
        tender_token = self.initial_data['tender_token']

        response = self.app.get('/contracts/{}'.format(self.contract['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active")
        self.assertNotIn('items', response.json['data'])

        response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract['id'], tender_token),
                                       {"data": {"status": "active"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')

        response = self.app.patch_json('/contracts/{}/credentials?acc_token={}'.format(self.contract['id'], tender_token),
                                       {'data': ''})
        self.assertEqual(response.status, '200 OK')
        token = response.json['access']['token']

        # active > terminated allowed
        response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract['id'], token),
                                       {"data": {"status": "terminated"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.json['errors'], [
            {u'description': u"Can't terminate contract while 'amountPaid' is not set", u'location': u'body', u'name': u'data'}])

        response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract['id'], token),
                                       {"data": {"status": "terminated", "amountPaid": {"amount": 100, "valueAddedTaxIncluded": True, "currency": "UAH"}}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'terminated')

        # terminated > active not allowed
        response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract['id'], token),
                                       {"data": {"status": "active"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')


@unittest.skipIf(True, "Move to lower package")
class ContractResource4AdministratorTest(BaseContractWebTest):
    """ contract resource test """
    initial_auth = ('Basic', ('administrator', ''))

    test_contract_administrator_change = snitch(contract_administrator_change)


@unittest.skipIf(True, "Move to lower package")
class ContractCredentialsTest(BaseContractWebTest):
    """ Contract credentials tests """

    initial_auth = ('Basic', ('broker', ''))
    initial_data = test_contract_data

    test_get_credentials = snitch(get_credentials)
    test_generate_credentials = snitch(generate_credentials)

@unittest.skipIf(True, "Move to lower package")
class ContractWOItemsResource4BrokersTest(BaseContractWebTest):
    initial_data = test_contract_data_wo_items
    initial_auth = ('Basic', ('broker', ''))

    test_contract_wo_items_status_change = snitch(contract_wo_items_status_change)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContractTest))
    suite.addTest(unittest.makeSuite(ContractResourceTest))
    suite.addTest(unittest.makeSuite(ContractWDocumentsWithDSResourceTest))
    suite.addTest(unittest.makeSuite(ContractResource4BrokersTest))
    suite.addTest(unittest.makeSuite(ContractWOItemsResource4BrokersTest))
    suite.addTest(unittest.makeSuite(ContractResource4AdministratorTest))
    suite.addTest(unittest.makeSuite(ContractCredentialsTest))
    suite.addTest(unittest.makeSuite(ContractWOItemsResource4BrokersTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
