from typing import Dict, List, Optional, Union

from pytorch_lightning import Callback, Trainer, LightningModule
from ray import tune


class TuneReportCallback(Callback):
    def __init__(self, metrics: Union[List[str], Dict[str, str]]):
        self._metrics = metrics

    def on_validation_end(self, trainer: Trainer, pl_module: LightningModule):
        report_dict = {}
        for key in self._metrics:
            if isinstance(self._metrics, dict):
                metric = self._metrics[key]
            else:
                metric = key
            try:
                report_dict[key] = trainer.callback_metrics[metric].item()
            except KeyError:
                report_dict[key] = trainer.logged_metrics[metric].item()
        tune.report(**report_dict)
