import os
import sys
from functools import partial

from pytorch_lightning import Trainer, seed_everything
from ray import tune as ray_tune
from ray.tune import CLIReporter
from ray.tune.logger import JsonLogger, MLFLowLogger
from yacs.config import CfgNode

from argos_trains.common import get_checkpoint_callback
from argos_trains.config import get_cfg
from argos_trains.callbacks import TuneReportCallback
from argos_trains.util import override_lightning_logger, import_module_attr, eval_tune_search_space


def trainable(hparams, cfg, num_gpus, checkpoint_dir=None):
    checkpoint_path = None
    if checkpoint_dir is not None:
        checkpoint_path = os.path.join(checkpoint_dir, 'last.ckpt')

    if checkpoint_path is None:
        seed_everything(cfg.seed)

    # add hparams to cfg
    cfg.defrost()
    cfg.hparams = CfgNode(hparams)
    cfg.freeze()

    os.makedirs(cfg.checkpoint_dir, exist_ok=True)

    # instantiate model and data modules
    model_cls = import_module_attr(cfg.model_module)
    if checkpoint_dir is None:
        model = model_cls(cfg)
    else:
        model = model_cls.load_from_checkpoint(checkpoint_path)
    data_cls = import_module_attr(cfg.data_module)
    data = data_cls(cfg)

    # setup model checkpoint callback
    checkpoint_callback = get_checkpoint_callback(cfg)

    tune_callback = TuneReportCallback(metrics=cfg.tune.metrics)

    # train
    cfg.trainer.pop('gpus', None)
    cfg.trainer.pop('progress_bar_refresh_rate', None)
    cfg.trainer.pop('num_sanity_val_steps', None)
    cfg.trainer.pop('weights_summary', None)

    trainer = Trainer(
        resume_from_checkpoint=checkpoint_path,
        checkpoint_callback=checkpoint_callback,
        callbacks=[tune_callback],
        deterministic=True,
        gpus=num_gpus,
        progress_bar_refresh_rate=0,
        num_sanity_val_steps=0,
        weights_summary=None,
        **cfg.trainer
    )
    trainer.fit(model=model, datamodule=data)

    # save final checkpoint
    trainer.save_checkpoint(os.path.join(cfg.checkpoint_dir, 'final.ckpt'))


def tune():
    # add working directory to the module search paths
    sys.path.append(os.getcwd())

    # parse config file with defaults
    cfg = get_cfg()

    override_lightning_logger()

    # fast dev run
    fast_dev_run = cfg.trainer.pop('fast_dev_run', False)
    if fast_dev_run:
        model_cls = import_module_attr(cfg.model_module)
        model = model_cls(cfg)
        data_cls = import_module_attr(cfg.data_module)
        data = data_cls(cfg)
        trainer = Trainer(
            fast_dev_run=True,
            logger=False,
            checkpoint_callback=False,
            weights_summary=None
        )
        trainer.fit(model=model, datamodule=data)

    # read search space
    search_space = eval_tune_search_space(cfg.tune.search_space)

    # setup loggers
    loggers = [JsonLogger]
    config = search_space

    if cfg.mlflow.enabled:
        from mlflow.tracking import MlflowClient        # noqa
        experiment_id = MlflowClient().create_experiment(cfg.experiment_name)
        config['logger_config'] = {
            'mlflow_tracking_uri': cfg.mlflow.tracking_uri,
            'mlflow_registry_uri': cfg.mlflow.tracking_uri,
            'mlflow_experiment_id': experiment_id,
        }
        loggers.append(MLFLowLogger)

    # setup reported
    reporter = CLIReporter(metric_columns=list(cfg.tune.metrics.keys()) + ['training_iteration'])

    # setup searcher
    searcher = None
    if isinstance(cfg.tune.searcher, str) and len(cfg.tune.searcher) > 0:
        searcher = ray_tune.create_searcher(search_alg=cfg.tune.searcher, **cfg.tune.searcher_parameters)

    # setup scheduler
    scheduler = None
    if isinstance(cfg.tune.scheduler, str) and len(cfg.tune.scheduler) > 0:
        kwargs = cfg.tune.scheduler_parameters
        if cfg.tune.scheduler == 'pbt':
            kwargs['hyperparam_mutations'] = config
        scheduler = ray_tune.create_scheduler(scheduler=cfg.tune.scheduler, **kwargs)

    num_gpus = cfg.tune.resources_per_trial.get('gpu', 0)

    objective_metric = cfg.objective_name
    # update objective_metric if it is renamed in cfg.tune.metrics
    for k, v in cfg.tune.metrics.items():
        if v == cfg.objective_name:
            objective_metric = k

    ray_tune.run(
        run_or_experiment=partial(trainable, cfg=cfg, num_gpus=num_gpus),
        name=cfg.experiment_name,
        metric=objective_metric,
        mode='min' if cfg.minimize_objective else 'max',
        config=config,
        resources_per_trial=cfg.tune.resources_per_trial,
        num_samples=cfg.tune.num_samples,
        local_dir=os.path.join(cfg.experiment_path, 'ray_results'),
        search_alg=searcher,
        scheduler=scheduler,
        progress_reporter=reporter,
        loggers=loggers,
        log_to_file=True
    )


if __name__ == '__main__':
    tune()
