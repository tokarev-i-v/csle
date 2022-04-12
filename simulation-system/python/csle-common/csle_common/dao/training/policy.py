from typing import Union, List, Dict
from abc import ABC, abstractmethod
from csle_common.dao.training.agent_type import AgentType


class Policy(ABC):

    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type

    @abstractmethod
    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict) -> "Policy":
        pass