from app.models.models import ProductModels

class ProductRepository:
    """
    Repository responsible for product CRUD operations
    """

    def __init__(self, conn):
        self.conn = conn

    def insert_product(self, name, description, unit_price, stock_quantity, is_active=True):
        """
        Inserts a new product into the database
        """
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO product (name, description, unit_price, stock_quantity, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING product_id
                    """,
                    (name, description, unit_price, stock_quantity, is_active),
                )
                product_id = cur.fetchone()[0]
                self.conn.commit()
            return product_id
        return None

    def list_all_products(self):
        """
        Lists all active products
        """
        products = []
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT product_id, name, description, unit_price, stock_quantity, is_active
                    FROM product
                    WHERE is_active = TRUE
                    ORDER BY product_id
                    """
                )
                rows = cur.fetchall()
                for row in rows:
                    products.append(ProductModels(*row))
        return products

    def update_product(self, product_id, name, description, unit_price, stock_quantity):
        """
        Updates a product's information
        """
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE product 
                    SET name = %s, description = %s, unit_price = %s, stock_quantity = %s
                    WHERE product_id = %s
                    """,
                    (name, description, unit_price, stock_quantity, product_id),
                )
                self.conn.commit()
                
    def get_product_by_id(self, product_id):
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT product_id, name, description, unit_price, stock_quantity, is_active FROM product WHERE product_id=%s",
                    (product_id,)
                )
                row = cur.fetchone()
                if row:
                    return [ProductModels(*row)]
                else:
                    return None
                
                
    def delete_product(self, product_id):
        """
        Physically deletes a product from the database
        """
        if self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM product WHERE product_id = %s",
                    (product_id,),
                )
                self.conn.commit()