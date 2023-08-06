import os
import sys
from argparse import ArgumentParser, FileType

from pytorch_lightning import seed_everything, Trainer

from argos_trains.common import get_checkpoint_callback, get_early_stopping_callback, get_tensorboard_logger, \
    get_lightning_mlflow_logger
from argos_trains.config import get_cfg
from argos_trains.util import import_module_attr, override_lightning_logger


def resume():
    # add working directory to the module search paths
    sys.path.append(os.getcwd())

    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('checkpoint_file', type=FileType('r'))
    parser.add_argument('config_file', type=FileType('r'), default='config.yaml')
    args = parser.parse_args()
    checkpoint_path = args.checkpoint_file.name
    config_file_path = args.config_file.name

    # parse config file
    cfg = get_cfg(config_file_path)

    # instantiate model and data modules
    model_cls = import_module_attr(cfg.model_module)
    model = model_cls.load_from_checkpoint(checkpoint_path)
    data_cls = import_module_attr(cfg.data_module)
    data = data_cls(cfg)

    # override model cfg with the current config
    cfg.defrost()
    cfg.start_time = model.cfg.start_time
    cfg.checkpoint_dir = model.cfg.checkpoint_dir
    cfg.freeze()
    model.cfg = cfg

    seed_everything(cfg.seed)

    override_lightning_logger()

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

    cfg.trainer.pop('fast_dev_run', False)
    # train
    trainer = Trainer(
        resume_from_checkpoint=checkpoint_path,
        checkpoint_callback=checkpoint_callback,
        callbacks=callbacks,
        deterministic=True,
        **cfg.trainer
    )
    trainer.fit(model=model, datamodule=data)

    # save final checkpoint
    trainer.save_checkpoint(os.path.join(cfg.checkpoint_dir, 'final.ckpt'))


if __name__ == '__main__':
    resume()
