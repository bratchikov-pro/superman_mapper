from abc import ABC, abstractmethod
from typing import List, Dict

from cmd.config import Category
from dal.entities import Node, Location


class GeoService(ABC):
    @abstractmethod
    def get_nodes_for_category(self, category: str, user_location: Location) -> List[Node]: ...
