from dataclasses import dataclass

@dataclass
class ProductModels:
    """
    Data model representing a product in the inventory
    """
    product_id: int = None
    name: str = ""
    description: str = ""
    unit_price: float = 0.0
    stock_quantity: int = 0
    is_active: bool = True
