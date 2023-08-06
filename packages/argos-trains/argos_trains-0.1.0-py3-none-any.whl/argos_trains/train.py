import os
import sys

from pytorch_lightning import Trainer, seed_everything

from argos_trains.common import get_checkpoint_callback, get_early_stopping_callback, get_tensorboard_logger, \
    get_lightning_mlflow_logger
from argos_trains.util import override_lightning_logger, import_module_attr
from argos_trains.config import get_cfg


def train():
    # add working directory to the module search paths
    sys.path.append(os.getcwd())

    # parse config file with defaults
    cfg = get_cfg()

    seed_everything(cfg.seed)

    override_lightning_logger()

    # instantiate model and data modules
    model_cls = import_module_attr(cfg.model_module)
    model = model_cls(cfg)
    data_cls = import_module_attr(cfg.data_module)
    data = data_cls(cfg)

    callbacks = []

    # setup model checkpoint callback
    checkpoint_callback = get_checkpoint_callback(cfg)

    # setup early stopping
    if cfg.early_stop_patience >= 0:
        callbacks.append(get_early_stopping_callback(cfg))

    # setup loggers
    loggers = [get_tensorboard_logger(cfg)]
    if cfg.mlflow.enabled:
        loggers.append(get_lightning_mlflow_logger(cfg))

    # fast dev run
    fast_dev_run = cfg.trainer.pop('fast_dev_run', False)
    if fast_dev_run:
        trainer = Trainer(
            fast_dev_run=True,
            logger=False,
            checkpoint_callback=False,
            weights_summary=None
        )
        trainer.fit(model=model, datamodule=data)

    # train
    trainer = Trainer(
        checkpoint_callback=checkpoint_callback,
        callbacks=callbacks,
        logger=loggers,
        deterministic=True,
        **cfg.trainer
    )
    trainer.fit(model=model, datamodule=data)

    # save final checkpoint
    trainer.save_checkpoint(os.path.join(cfg.checkpoint_dir, 'final.ckpt'))


if __name__ == '__main__':
    train()
