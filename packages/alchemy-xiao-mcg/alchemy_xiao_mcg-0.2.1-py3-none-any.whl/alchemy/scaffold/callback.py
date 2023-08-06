# Base class for all callbacks during training.
# Based on Pytorch-lightning for abstract research code from engineering code.
# Anything is not related to kernel research flow should goes here.
# Example of usage of callbacks: logging image / add inspect code for debugging / etc.
# For each project, inherit this and implement project-specific callbacks.
# Reference and adapted from:
#  https://pytorch-lightning.readthedocs.io/en/latest/lightning-module.html
# Author: Xiao Li

from pytorch_lightning import Callback
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.utilities import rank_zero_only
from pytorch_lightning import _logger as log
from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger

import torch
import torchvision
import wandb
import numpy as np
import os


class ImageLoggingCallback(Callback):
    r"""
    Callback for logging image.
    The callback is activate every period_batch step.
    """

    def on_train_start(self, trainer, pl_module):
        super(ImageLoggingCallback, self).on_train_start(trainer, pl_module)
        # Setup loss log dict
        self.log_dict_name = 'log_image'
        setattr(pl_module, self.log_dict_name, dict())

    @rank_zero_only
    def on_batch_end(self, trainer, pl_module):
        super(ImageLoggingCallback, self).on_batch_end(trainer, pl_module)
        # Logging every period_batch
        # Assert using wandb logger or tensorboard logger.
        assert(isinstance(pl_module.logger, WandbLogger) or
               isinstance(pl_module.logger, TensorBoardLogger))

        # only run on main process
        if trainer.global_rank != 0:
            return

        step = trainer.global_step
        if(step % trainer.row_log_interval != 0):
            return

        log_dict = getattr(pl_module, self.log_dict_name)
        for k in log_dict:
            v = log_dict[k]
            img_grid = self._tensor_to_image(v)
            k_gpu = k + '_{:02d}'.format(trainer.global_rank)
            self._log_image(pl_module.logger, k_gpu, img_grid, step)

    def _log_image(self, logger, name, img, step):
        if(isinstance(logger, WandbLogger)):
            logger.experiment.log({
                name: [wandb.Image(img, caption=name)]
            }, step=step)
        elif(isinstance(logger, TensorBoardLogger)):
            logger.experiment.add_image(name, img,
                                        global_step=step, dataformats='HWC')

    # Override this for other image format (e.g. HDR images / multi-channel images, etc.)
    def _tensor_to_image(self, img_tensor: torch.Tensor, invert_channel: bool = False, **kwargs):
        # Assume img_tensor in channel-first format
        img_tensor_in = img_tensor.cpu().detach()
        if(invert_channel):
            img_tensor_in = torch.flip(img_tensor_in, dims=[-1])
        if(len(img_tensor_in) == 3):
            img_tensor_in.unsqueeze(0)
        img_grid = torchvision.utils.make_grid(img_tensor_in, **kwargs).numpy()
        img_grid = np.transpose(img_grid, (1, 2, 0))

        return img_grid


# Callback for checkpoint.
class EpochOrStepModelCheckpoint(ModelCheckpoint):
    r"""
    Implements a custom callback for checkpoint,
    inherited from Pytorch-lighting's default ModelCheckpoint.
    The main reason for inherit default one is to checkpoint with every given step instead of epoch.

    Usage:
    To enable / disable step-based checkpoint, set period_step to a positive number or -1;
    To enable / disable epoch-based checkpoint, set period_epoch to a positive number or -1.
    """

    def __init__(self, *args, period_step: int = -1, period_epoch: int = 1, **kwargs):
        super(EpochOrStepModelCheckpoint, self).__init__(*args, period=period_epoch, **kwargs)
        self.period_step = period_step
        self.current_step_checked = False

        self.step_last_check = None

    def format_step_checkpoint_name(self, cnt, ver=None):
        """Generate a filename according to the defined template.

        Example::

            >>> tmpdir = os.path.dirname(__file__)
            >>> ckpt = ModelCheckpoint(os.path.join(tmpdir, '{epoch}'))
            >>> os.path.basename(ckpt.format_checkpoint_name(0, {}))
            'epoch=0.ckpt'
            >>> ckpt = ModelCheckpoint(os.path.join(tmpdir, '{epoch:03d}'))
            >>> os.path.basename(ckpt.format_checkpoint_name(5, {}))
            'epoch=005.ckpt'
            >>> ckpt = ModelCheckpoint(os.path.join(tmpdir, '{epoch}-{val_loss:.2f}'))
            >>> os.path.basename(ckpt.format_checkpoint_name(2, dict(val_loss=0.123456)))
            'epoch=2-val_loss=0.12.ckpt'
            >>> ckpt = ModelCheckpoint(os.path.join(tmpdir, '{missing:d}'))
            >>> os.path.basename(ckpt.format_checkpoint_name(0, {}))
            'missing=0.ckpt'
        """
        # check if user passed in keys to the string
        filename = f'{self.prefix}_ckpt_step_{cnt}'
        str_ver = f'_v{ver}' if ver is not None else ''
        filepath = os.path.join(self.dirpath, filename + str_ver + '.ckpt')
        return filepath

    @rank_zero_only
    def on_batch_end(self, trainer, pl_module):
        # only run on main process
        if trainer.global_rank != 0:
            return

        step = trainer.global_step

        if self.step_last_check is not None and (step - self.step_last_check) < self.period_step:
            # skipping in this term
            return

        if (self.step_last_check is not None) and (step == self.step_last_check):
            # If this is true, then this is not the first call of current step;
            # Skipping in this case.
            if self.verbose > 0:
                log.info('\nMultiple call detected. This is mostly due to multiple callbacks inherited from BasicCallback.')
            return

        self.step_last_check = step

        filepath = self.format_step_checkpoint_name(step)
        version_cnt = 0
        while os.path.isfile(filepath):
            filepath = self.format_step_checkpoint_name(step, ver=version_cnt)
            # this step called before
            version_cnt += 1

        if self.verbose > 0:
            log.info(f'\nStep {step:05d}: saving model to {filepath}')
        self._save_model(filepath, trainer, pl_module)
