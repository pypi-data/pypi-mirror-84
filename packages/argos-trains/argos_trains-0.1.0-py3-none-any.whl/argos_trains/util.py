from importlib import import_module
import logging
from argos_trains.logging import get_default_handler


def override_lightning_logger():
    logger = logging.getLogger('lightning')
    logger.handlers = []
    handler = get_default_handler()
    logger.addHandler(handler)
    logger.propagate = False


def import_module_attr(name):
    name_parts = name.split('.')
    module = import_module('.'.join(name_parts[:-1]))
    cls = getattr(module, name_parts[-1])
    return cls


def eval_tune_search_space(search_space_cfg_node):
    from ray import tune
    d = {}
    for param_name, opts in search_space_cfg_node.items():
        t = opts.pop('type')
        func = getattr(tune, t)
        d[param_name] = func(**opts)
    return d
