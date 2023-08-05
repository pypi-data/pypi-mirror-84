import numpy as np
import torch
import copy

from torch.optim import Adam
from d3rlpy.models.torch.q_functions import create_discrete_q_function
from .utility import hard_sync
from .utility import torch_api, train_api, eval_api
from .utility import compute_augemtation_mean
from .base import TorchImplBase


class DQNImpl(TorchImplBase):
    def __init__(self, observation_shape, action_size, learning_rate, gamma,
                 n_critics, bootstrap, share_encoder, eps, use_batch_norm,
                 q_func_type, use_gpu, scaler, augmentation, n_augmentations,
                 encoder_params):
        self.observation_shape = observation_shape
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.n_critics = n_critics
        self.bootstrap = bootstrap
        self.share_encoder = share_encoder
        self.eps = eps
        self.use_batch_norm = use_batch_norm
        self.q_func_type = q_func_type
        self.scaler = scaler
        self.augmentation = augmentation
        self.n_augmentations = n_augmentations
        self.encoder_params = encoder_params
        self.use_gpu = use_gpu

    def build(self):
        # setup torch models
        self._build_network()

        # setup target network
        self.targ_q_func = copy.deepcopy(self.q_func)

        if self.use_gpu:
            self.to_gpu(self.use_gpu)
        else:
            self.to_cpu()

        # setup optimizer after the parameters move to GPU
        self._build_optim()

    def _build_network(self):
        self.q_func = create_discrete_q_function(
            self.observation_shape,
            self.action_size,
            n_ensembles=self.n_critics,
            use_batch_norm=self.use_batch_norm,
            q_func_type=self.q_func_type,
            bootstrap=self.bootstrap,
            share_encoder=self.share_encoder,
            encoder_params=self.encoder_params)

    def _build_optim(self):
        self.optim = Adam(self.q_func.parameters(),
                          lr=self.learning_rate,
                          eps=self.eps)

    @train_api
    @torch_api
    def update(self, obs_t, act_t, rew_tp1, obs_tp1, ter_tp1):
        if self.scaler:
            obs_t = self.scaler.transform(obs_t)
            obs_tp1 = self.scaler.transform(obs_tp1)

        q_tp1 = compute_augemtation_mean(self.augmentation,
                                         self.n_augmentations,
                                         self.compute_target, {'x': obs_tp1},
                                         ['x'])
        q_tp1 *= (1.0 - ter_tp1)

        loss = compute_augemtation_mean(
            self.augmentation, self.n_augmentations, self._compute_loss, {
                'obs_t': obs_t,
                'act_t': act_t.long(),
                'rew_tp1': rew_tp1,
                'q_tp1': q_tp1
            }, ['obs_t'])

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss.cpu().detach().numpy()

    def _compute_loss(self, obs_t, act_t, rew_tp1, q_tp1):
        return self.q_func.compute_error(obs_t, act_t, rew_tp1, q_tp1,
                                         self.gamma)

    def compute_target(self, x):
        with torch.no_grad():
            max_action = self.targ_q_func(x).argmax(dim=1)
            return self.targ_q_func.compute_target(x, max_action)

    def _predict_best_action(self, x):
        return self.q_func(x).argmax(dim=1)

    @eval_api
    @torch_api
    def predict_value(self, x, action, with_std):
        assert x.shape[0] == action.shape[0]

        if self.scaler:
            x = self.scaler.transform(x)

        action = action.view(-1).long().cpu().detach().numpy()
        with torch.no_grad():
            values = self.q_func(x, reduction='none').cpu().detach().numpy()
            values = np.transpose(values, [1, 0, 2])

        mean_values = values.mean(axis=1)
        stds = np.std(values, axis=1)

        ret_values = []
        ret_stds = []
        for v, std, a in zip(mean_values, stds, action):
            ret_values.append(v[a])
            ret_stds.append(std[a])

        if with_std:
            return np.array(ret_values), np.array(ret_stds)

        return np.array(ret_values)

    def sample_action(self, x):
        return self.predict_best_action(x)

    def update_target(self):
        hard_sync(self.targ_q_func, self.q_func)


class DoubleDQNImpl(DQNImpl):
    def compute_target(self, x):
        with torch.no_grad():
            action = self._predict_best_action(x)
            return self.targ_q_func.compute_target(x, action)
