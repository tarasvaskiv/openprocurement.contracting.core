# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    apply_data_patch,
    generate_id,
)
from openprocurement.contracting.api.utils import save_contract


class isContract(object):
    """ Route predicate. """

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'contractType = %s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        if request.contract is not None:
            c_type = getattr(request.contract, 'contractType',
                             None) or "common"
            return c_type == self.val
        return False


def register_contract_contractType(config, model):
    """Register a contract contractType.
    :param config:
        The pyramid configuration object that will be populated.
    :param model:
        The contract model class
    """
    contract_type = model.contractType.default or 'common'
    config.registry.contract_contractTypes[contract_type] = model


def apply_patch(request, data=None, save=True, src=None):
    data = request.validated['data'] if data is None else data
    patch = data and apply_data_patch(src or request.context.serialize(), data)
    if patch:
        request.context.import_data(patch)
        if save:
            return save_contract(request)


def set_ownership(item, request):
    item.owner_token = generate_id()
