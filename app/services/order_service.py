from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.order_schemas import CreateOrderSchema
from app.models.product import Product
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from fastapi import HTTPException
from app.enums.order_status import OrderStatus

class OrderService:
    def create_order(body: CreateOrderSchema, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="É preciso estar logado para fazer um pedido")
        
        user = session.query(User).filter(User.id == body.user_id).first()

        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")

        if not body.items:
            raise HTTPException(status_code=400, detail="Pedido inválido. Precisa conter ao menos um produto")
        
        if auth_user.id != user.id:
            raise HTTPException(status_code=403, detail="Operação não autorizada")
        
        order = Order(user.id, OrderStatus.OPEN)
        session.add(order)
        
        product_ids = [item.id for item in body.items]
        products = session.query(Product).filter(Product.id.in_(product_ids)).all()
        products_dict = {product.id: product for product in products}

        for item in body.items:
            product = products_dict[item.id]
            if not product:
                raise HTTPException(status_code=400, detail=f"Produto {item.id} não encontrado")
            if not product.is_active:
                raise HTTPException(status_code=400, detail=f"Produto {product.name} não está disponível")
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail=f"Produto {product.name} precisa conter uma ou mais unidades")
            order_item = OrderItem(order.id, item.id, item.quantity, product.price)
            session.add(order_item)
        
        order.calculate_price()

        try:
            session.commit()
        except:
            session.rollback()
            raise
        
        return order

    def list_user_orders(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="É preciso estar logado para acessar as informações")
        if not auth_user.is_admin and auth_user != id:
            raise HTTPException(status_code=403, detail="Acesso não permitido as informações")
        
        orders = session.query(Order).filter(Order.user_id == id).all()
        return orders

    def get_order_by_id(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="É preciso estar logado para acessar as informações")
        
        order = session.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        if auth_user.id != order.user_id and not auth_user.is_admin:
            raise HTTPException(status_code=403, detail="Operação não autorizada")
        
        return order

    def cancel_order(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="É preciso estar logado para acessar as informações")
        order = session.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        if auth_user.is_admin == False and auth_user != order.user_id:
            raise HTTPException(status_code=403, detail="Operação não autorizada")
        
        if order.status == OrderStatus.DELIVERED:
            raise HTTPException(status_code=400, detail="Não é permitido cancelar um pedido já entregue")
        order.status = OrderStatus.CANCELED
        session.commit()
        return order

    def delivered_order(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="É preciso estar logado para acessar as informações")
        if not auth_user.is_admin:
            raise HTTPException(status_code=403, detail="Apenas admins podem realizar a operação")
        order = session.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        order.status = OrderStatus.DELIVERED
        session.commit()
        return order