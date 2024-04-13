from typing import Dict, List

from cmd.config import Category
from dal.entities import Node, GeoBroker, Location
from services.geo.entities import GeoService


class OSMService(GeoService):

    def __init__(self, categories: Dict[str, Category], osm_broker: GeoBroker) -> None:
        self.osm_categories_map = categories
        self.osm_broker = osm_broker

    def get_nodes_for_category(self, category: str, user_location: Location) -> List[Node]:
        category_nodes: List[Node] = []
        for amenity in self.osm_categories_map[category].amenities:
            category_nodes.append(self.osm_broker.get_nodes_by_amenity(amenity, user_location))

        return category_nodes
