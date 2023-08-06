import os
from argparse import ArgumentParser, FileType
from datetime import datetime

from yacs.config import CfgNode


_C = CfgNode()

_C.experiment_path = ''

_C.experiment_name = ''

_C.model_module = ''

_C.data_module = ''

_C.seed = 123

_C.mlflow = CfgNode()

_C.mlflow.enabled = False

_C.mlflow.tracking_uri = ''

_C.objective_name = 'loss/val'

_C.minimize_objective = True

_C.batch_size = 64

_C.num_workers = 0

_C.save_top_k = -1

_C.early_stop_patience = -1     # -1 to disable

_C.model = CfgNode(new_allowed=True)

_C.data = CfgNode(new_allowed=True)

_C.trainer = CfgNode(new_allowed=True)

_C.hparams = CfgNode(new_allowed=True)

_C.tune = CfgNode()

_C.tune.metrics = CfgNode(new_allowed=True)

_C.tune.search_space = CfgNode(new_allowed=True)

# "ax" "dragonfly" "skopt" "hyperopt" "bayesopt" "bohb" "nevergrad" "optuna" "zoopt" "sigopt"
_C.tune.searcher = ''

_C.tune.searcher_parameters = CfgNode(new_allowed=True)

# "async_hyperband" "median_stopping_rule" "hyperband" "hb_bohb" "pbt"
_C.tune.scheduler = ''

_C.tune.scheduler_parameters = CfgNode(new_allowed=True)

_C.tune.resources_per_trial = CfgNode(new_allowed=True)

_C.tune.num_samples = 10


def get_cfg(config_file_path=None):
    if config_file_path is None:
        parser = ArgumentParser()
        parser.add_argument('config_file', type=FileType('r'), default='config.yaml')
        args = parser.parse_args()
        config_file_path = args.config_file.name

    cfg = _C.clone()
    cfg.merge_from_file(config_file_path)
    cfg.start_time = datetime.now().strftime('%y%m%d_%H%M%S')
    cfg.checkpoint_dir = os.path.join(cfg.experiment_path, 'checkpoints', cfg.start_time)
    cfg.freeze()
    return cfg
