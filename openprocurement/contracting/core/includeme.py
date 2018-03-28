# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution, iter_entry_points

from openprocurement.contracting.core.utils import (
    contract_from_data,
    extract_contract,
    isContract,
    SubscribersPicker,
    register_contractType
)
from openprocurement.contracting.core.design import add_design


PKG = get_distribution(__package__)

LOGGER = getLogger(PKG.project_name)


def includeme(config):
    LOGGER.info('Init contracting plugin.')
    add_design()
    config.add_request_method(extract_contract, 'contract', reify=True)

    # contractType plugins support
    config.registry.contract_contractTypes = {}
    config.add_route_predicate('contractType', isContract)
    config.add_subscriber_predicate('contractType', SubscribersPicker)
    config.add_request_method(contract_from_data)
    config.add_directive('add_contractType',
                         register_contractType)
    config.scan("openprocurement.contracting.core.views")
    # TODO: we need adapters later
    # config.scan("openprocurement.contract.core.subscribers")
    # config.registry.registerAdapter(TenderConfigurator, (ITender, IRequest),
    #                                 IContentConfigurator)


    # search for plugins
    settings = config.get_settings()
    plugins = settings.get('plugins') and settings['plugins'].split(',')
    for entry_point in iter_entry_points(
            'openprocurement.contracting.core.plugins'):
        if not plugins or entry_point.name in plugins:
            plugin = entry_point.load()
            plugin(config)
