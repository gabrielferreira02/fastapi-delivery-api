import pytest
from fastapi import HTTPException
from app.models.order import Order
from app.models.product import Product
from app.models.category import Category
from app.enums.order_status import OrderStatus
from app.services.order_service import OrderService
from app.schemas.order_schemas import CreateOrderSchema, ItemSchema
from uuid import uuid4

def test_list_orders_user_success(db_session, create_user):
    user = create_user(db_session)
    order = Order(user.id, OrderStatus.OPEN)
    order2 = Order(user.id, OrderStatus.DELIVERED)
    db_session.add(order)
    db_session.add(order2)
    db_session.commit()

    orders = OrderService.list_user_orders(user.id, db_session, user)

    assert len(orders) == 2

def test_list_orders_user_fail_with_authenticated_user_different_from_id(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        OrderService.list_user_orders(uuid4(), db_session, user)

    assert exc.value.status_code == 403

def test_list_orders_user_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        OrderService.list_user_orders(uuid4(), db_session, None)

    assert exc.value.status_code == 401

def test_get_order_by_id_success(db_session, create_user):
    user = create_user(db_session)
    order = Order(user.id, OrderStatus.OPEN)
    db_session.add(order)
    db_session.commit()
    db_session.flush()

    result = OrderService.get_order_by_id(order.id, db_session, user)

    assert result.user_id == order.user_id
    assert result.status == order.status

def test_get_order_by_id_fail_with_authenticated_user_different_from_order_user_id(db_session, create_user):
    user = create_user(db_session)
    auth_user = create_user(db_session)
    order = Order(user.id, OrderStatus.OPEN)
    db_session.add(order)
    db_session.commit()
    db_session.flush()

    with pytest.raises(HTTPException) as exc:
        OrderService.get_order_by_id(order.id, db_session, auth_user)

    assert exc.value.status_code == 403

def test_get_order_by_id_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        OrderService.get_order_by_id(uuid4(), db_session, None)

    assert exc.value.status_code == 401

def test_get_order_by_id_fail_with_not_found_order(db_session, create_user):
    user = create_user(db_session)
    with pytest.raises(HTTPException) as exc:
        OrderService.get_order_by_id(uuid4(), db_session, user)

    assert exc.value.status_code == 404

def test_cancel_order_success(db_session, create_user):
    user = create_user(db_session)
    order = Order(user.id, OrderStatus.OPEN)
    db_session.add(order)
    db_session.commit()
    db_session.flush()

    result = OrderService.cancel_order(order.id, db_session, user)

    assert result.status == OrderStatus.CANCELED

def test_cancel_order_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        OrderService.cancel_order(uuid4(), db_session, None)

    assert exc.value.status_code == 401

def test_cancel_order_fail_with_not_found_order(db_session, create_user):
    user = create_user(db_session)
    with pytest.raises(HTTPException) as exc:
        OrderService.cancel_order(uuid4(), db_session, user)

    assert exc.value.status_code == 404

def test_cancel_order_fail_with_delivered_order(db_session, create_user):
    user = create_user(db_session)
    order = Order(user.id, OrderStatus.DELIVERED)
    db_session.add(order)
    db_session.commit()
    db_session.flush()

    with pytest.raises(HTTPException) as exc:
        OrderService.cancel_order(order.id, db_session, user)

    assert exc.value.status_code == 400

def test_delivered_order_success(db_session, create_user):
    user = create_user(db_session)
    user.is_admin = True
    order = Order(user.id, OrderStatus.OPEN)
    db_session.add(order)
    db_session.commit()
    db_session.flush()

    result = OrderService.delivered_order(order.id, db_session, user)

    assert result.status == OrderStatus.DELIVERED

def test_delivered_order_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        OrderService.delivered_order(uuid4(), db_session, None)

    assert exc.value.status_code == 401

def test_delivered_order_fail_with_not_found_order(db_session, create_user):
    user = create_user(db_session)
    user.is_admin = True
    db_session.commit()

    with pytest.raises(HTTPException) as exc:
        OrderService.delivered_order(uuid4(), db_session, user)

    assert exc.value.status_code == 404

def test_delivered_order_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)
    with pytest.raises(HTTPException) as exc:
        OrderService.delivered_order(uuid4(), db_session, user)

    assert exc.value.status_code == 403

def test_create_order_success(db_session, create_user):
    user = create_user(db_session)
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Product", "product", "description", 10, category.id, "prod.png", True)
    db_session.add(product)
    db_session.commit()
    db_session.flush()

    schema = CreateOrderSchema(user_id=user.id, items=[ItemSchema(id=product.id, quantity=1)])

    result = OrderService.create_order(schema, db_session, user)

    assert result.user_id == user.id
    assert result.status == OrderStatus.OPEN

def test_create_order_fail_with_not_authenticated_user(db_session):
    schema = CreateOrderSchema(user_id=uuid4(), items=[ItemSchema(id=uuid4(), quantity=1)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, None)

    assert exc.value.status_code == 401

def test_create_order_fail_with_authenticated_user_different_from_user_id(db_session, create_user):
    user = create_user(db_session)
    user2 = create_user(db_session)
    schema = CreateOrderSchema(user_id=user2.id, items=[ItemSchema(id=uuid4(), quantity=1)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 403

def test_create_order_fail_with_user_id_not_found(db_session, create_user):
    user = create_user(db_session)
    schema = CreateOrderSchema(user_id=uuid4(), items=[ItemSchema(id=uuid4(), quantity=1)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 400

def test_create_order_fail_with_no_items(db_session, create_user):
    user = create_user(db_session)
    schema = CreateOrderSchema(user_id=uuid4(), items=[])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 400

def test_create_order_fail_with_not_found_product(db_session, create_user):
    user = create_user(db_session)
    schema = CreateOrderSchema(user_id=uuid4(), items=[ItemSchema(id=uuid4(), quantity=1)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 400

def test_create_order_fail_with_invalid_item_quantity(db_session, create_user):
    user = create_user(db_session)
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Product", "product", "description", 10, category.id, "prod.png", True)
    db_session.add(product)
    db_session.commit()
    db_session.flush()

    schema = CreateOrderSchema(user_id=user.id, items=[ItemSchema(id=product.id, quantity=0)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 400

def test_create_order_fail_with_inactive_product(db_session, create_user):
    user = create_user(db_session)
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Product", "product", "description", 10, category.id, "prod.png", False)
    db_session.add(product)
    db_session.commit()
    db_session.flush()

    schema = CreateOrderSchema(user_id=user.id, items=[ItemSchema(id=product.id, quantity=1)])

    with pytest.raises(HTTPException) as exc:
        OrderService.create_order(schema, db_session, user)

    assert exc.value.status_code == 400