from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import MLFlowLogger, TensorBoardLogger


def get_checkpoint_callback(cfg):
    return ModelCheckpoint(
        dirpath=cfg.checkpoint_dir,
        # filename=f'{{epoch}}_{{{cfg.objective_name}}}',
        filename='{epoch}',
        monitor=cfg.objective_name,
        mode='min' if cfg.minimize_objective else 'max',
        save_top_k=cfg.save_top_k,
        save_last=True
    )


def get_early_stopping_callback(cfg):
    return EarlyStopping(
        monitor=cfg.objective_name,
        mode='min' if cfg.minimize_objective else 'max',
        patience=cfg.early_stop_patience
    )


def get_lightning_mlflow_logger(cfg):
    return MLFlowLogger(
        experiment_name=cfg.experiment_name,
        tracking_uri=cfg.mlflow.tracking_uri,
        save_dir='./mlflow'
    )


def get_tensorboard_logger(cfg):
    return TensorBoardLogger(
        save_dir='.',
        name='logs',
        version=cfg.start_time
    )
