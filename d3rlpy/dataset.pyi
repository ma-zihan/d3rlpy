import numpy as np

from typing import Any, Dict, List, Optional, Sequence, Union
from typing_extensions import Protocol

class Transition:
    def __init__(
        self,
        observation_shape: Sequence[int],
        action_size: int,
        observation: np.ndarray,
        action: Union[int, np.ndarray],
        reward: float,
        next_observation: np.ndarray,
        next_action: Union[int, np.ndarray],
        next_reward: float,
        terminal: float,
        prev_transition: Optional[Transition] = ...,
        next_transition: Optional[Transition] = ...,
    ): ...
    def get_observation_shape(self) -> Sequence[int]: ...
    def get_action_size(self) -> int: ...
    @property
    def observation(self) -> np.ndarray: ...
    @property
    def action(self) -> Union[int, np.ndarray]: ...
    @property
    def reward(self) -> float: ...
    @property
    def next_observation(self) -> np.ndarray: ...
    @property
    def next_action(self) -> Union[int, np.ndarray]: ...
    @property
    def next_reward(self) -> float: ...
    @property
    def terminal(self) -> float: ...
    @property
    def prev_transition(self) -> Optional[Transition]: ...
    @prev_transition.setter
    def prev_transition(self, transition: Transition) -> None: ...
    @property
    def next_transition(self) -> Optional[Transition]: ...
    @next_transition.setter
    def next_transition(self, transition: Transition) -> None: ...
    def clear_links(self) -> None: ...

class TransitionMiniBatch:
    def __init__(
        self,
        transitions: List[Transition],
        n_frames: int = ...,
        n_steps: int = ...,
        gamma: float = ...,
    ): ...
    @property
    def observations(self) -> np.ndarray: ...
    @property
    def actions(self) -> np.ndarray: ...
    @property
    def rewards(self) -> np.ndarray: ...
    @property
    def next_observations(self) -> np.ndarray: ...
    @property
    def next_actions(self) -> np.ndarray: ...
    @property
    def next_rewards(self) -> np.ndarray: ...
    @property
    def transitions(self) -> List[Transition]: ...
    @property
    def terminals(self) -> np.ndarray: ...
    @property
    def n_steps(self) -> np.ndarray: ...

def trace_back_and_clear(transition: Transition) -> None: ...

class Episode:
    def __init__(
        self,
        observation_shape: Sequence[int],
        action_size: int,
        observations: np.ndarray,
        actions: np.ndarray,
        rewards: np.ndarray,
    ): ...
    @property
    def observations(self) -> np.ndarray: ...
    @property
    def actions(self) -> np.ndarray: ...
    @property
    def rewards(self) -> np.ndarray: ...
    @property
    def transitions(self) -> List[Transition]: ...
    def build_transitions(self) -> None: ...
    def size(self) -> int: ...
    def get_observation_shape(self) -> Sequence[int]: ...
    def get_action_size(self) -> int: ...
    def compute_return(self) -> float: ...

class MDPDataset:
    def __init__(
        self,
        observations: np.ndarray,
        actions: np.ndarray,
        rewards: np.ndarray,
        terminals: np.ndarray,
        discrete_action: bool = ...,
    ): ...
    @property
    def observations(self) -> np.ndarray: ...
    @property
    def actions(self) -> np.ndarray: ...
    @property
    def rewards(self) -> np.ndarray: ...
    @property
    def terminals(self) -> np.ndarray: ...
    @property
    def episodes(self) -> List[Episode]: ...
    def size(self) -> int: ...
    def get_action_size(self) -> int: ...
    def get_observation_shape(self) -> Sequence[int]: ...
    def is_action_discrete(self) -> bool: ...
    def compute_stats(self) -> Dict[str, Any]: ...
    def clip_reward(
        self, low: Optional[float], high: Optional[float]
    ) -> None: ...
    def append(
        self,
        observations: np.ndarray,
        actions: np.ndarray,
        rewards: np.ndarray,
        terminals: np.ndarray,
    ) -> None: ...
    def extend(self, dataset: MDPDataset) -> None: ...
    def dump(self, fname: str) -> None: ...
    @classmethod
    def load(cls, fname: str) -> MDPDataset: ...
    def build_episodes(self) -> None: ...

class _ValueProtocol(Protocol):
    def predict_value(self, x: Union[np.ndarray, list]) -> np.ndarray: ...

def compute_lambda_return(
    transition: Transition,
    algo: _ValueProtocol,
    gamma: float,
    lam: float,
    n_frames: int,
) -> float: ...
