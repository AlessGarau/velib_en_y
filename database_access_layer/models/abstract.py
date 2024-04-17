from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the model into a dictionary usable for different operations

        Returns a dict representation of the model
        """
        pass
