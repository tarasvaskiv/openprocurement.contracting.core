# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution

from openprocurement.contracting.core.utils import contract_from_data, extract_contract
from openprocurement.contracting.core.design import add_design


PKG = get_distribution(__package__)

LOGGER = getLogger(PKG.project_name)


def includeme(config):
    LOGGER.info('Init contracting plugin.')
    add_design()
    config.add_request_method(extract_contract, 'contract', reify=True)
    config.add_request_method(contract_from_data)
    config.scan("openprocurement.contracting.core.views")
