from app.repositories.repositorie_product import ProductRepository
from app.utils.logger import logger

class ProductsServices:
    
    def __init__(self, conn):
        self.products = ProductRepository(conn)
        
    def _as_dict(self, product):
        return [dict(
                    product_id=product.product_id,
                    name=product.name,
                    description=product.description,
                    unit_price=product.unit_price,
                    is_active=product.is_active,
                    stock_quantity=product.stock_quantity,
                ) 
                for product in product]
    
    def list_all_products(self) -> dict:
        try:
            result =  self.products.list_all_products()
            if result:
                result = self._as_dict(result)
            return result
        except Exception as e:
            logger.warning(f"Error get all products: {e}")
    
    def register_products(self, request):
        try:
            name = request.form["name"]
            description = request.form["description"]
            unit_price = request.form["unit_price"]
            stock_quantity = request.form["stock_quantity"]
            
            self.products.insert_product(name, description, unit_price, stock_quantity)
            return True
            
        except Exception as e:
            logger.warning(f"Error get all products: {e}")
            return False
        
    def update_product(self, id, request):
        try:
            name = request.form["name"]
            description = request.form["description"]
            unit_price = request.form["unit_price"]
            stock_quantity = request.form["stock_quantity"]
            
            self.products.update_product(id, name, description, unit_price, stock_quantity)
            return True
        
        except Exception as e:
            logger.warning(f"Error putting stock quantity: {e}")
            return False
            
    def get_product_by_id(self, product_id):
        result = self.products.get_product_by_id(product_id)
        if result:
            result = self._as_dict(result)[0]
        return result
    
    def delete_product(self, product_id):
        try:
            self.products.delete_product(product_id)
            return True
        
        except Exception as e:
            logger.warning(f"Error when deleting product: {e}")
            return False
        
    
    