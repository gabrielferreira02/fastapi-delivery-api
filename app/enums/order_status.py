from enum import Enum

class OrderStatus(str, Enum):
    OPEN = "aberto",
    DELIVERED = "entregue",
    CANCELED = "cancelado"