# -*- coding: utf-8 -*-
from openprocurement.api.adapters import ContentConfigurator


class ContractConfigurator(ContentConfigurator):
    """ Contract configuration adapter """

    name = "Contract Configurator"
    model = None

    create_accreditation = 3
