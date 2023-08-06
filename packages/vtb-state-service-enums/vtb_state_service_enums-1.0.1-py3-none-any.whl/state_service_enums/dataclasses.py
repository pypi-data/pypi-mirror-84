from dataclasses import dataclass


@dataclass
class OrderAction:
    order_id: str
    action_id: str
    graph_id: str
