import pytest
from app.models.product import Product
from app.models.category import Category
from app.services.product_service import ProductService
from app.schemas.product_schemas import UpdateProductSchema
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers
from io import BytesIO
from uuid import uuid4

def create_fake_image():
    file = BytesIO(b"fake image content")

    headers = Headers({
        "content-type": "image/png"
    })

    return UploadFile(
        filename="test.png",
        file=file,
        headers=headers
    )

def test_get_product_success(db_session):
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.commit()

    result = ProductService.get_product("test", db_session)

    assert result.slug == product.slug
    assert result.category_id == category.id

def test_get_product_fail_with_not_found_slug(db_session):
    with pytest.raises(HTTPException) as exc:
        ProductService.get_product("test", db_session)
    
    assert exc.value.status_code == 404

def test_get_products_by_category_success(db_session):
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product1 = Product("Test 1", "test1", "description", 10, category.id, "test1.png", True)
    product2 = Product("Test 2", "test2", "description", 15, category.id, "test2.png", True)
    db_session.add(product1)
    db_session.add(product2)
    db_session.commit()

    result = ProductService.get_products_by_category("test", db_session)

    assert len(result) == 2

def test_deactivate_product_success(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.commit()

    ProductService.deactivate_product("test", db_session, admin)

    updated_product = db_session.query(Product).filter(Product.slug=="test").first()
    assert updated_product.is_active is False

def test_deactivate_product_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        ProductService.deactivate_product("test", db_session, None)

    assert exc.value.status_code == 401

def test_deactivate_product_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        ProductService.deactivate_product("test", db_session, user)

    assert exc.value.status_code == 403

def test_deactivate_product_fail_with_not_found_product(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    with pytest.raises(HTTPException) as exc:
        ProductService.deactivate_product("test", db_session, admin)

    assert exc.value.status_code == 404

def test_activate_product_success(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", False)
    db_session.add(product)
    db_session.commit()

    ProductService.activate_product("test", db_session, admin)

    updated_product = db_session.query(Product).filter(Product.slug=="test").first()
    assert updated_product.is_active is True

def test_activate_product_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        ProductService.activate_product("test", db_session, None)

    assert exc.value.status_code == 401

def test_activate_product_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        ProductService.activate_product("test", db_session, user)

    assert exc.value.status_code == 403

def test_activate_product_fail_with_not_found_product(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    with pytest.raises(HTTPException) as exc:
        ProductService.activate_product("test", db_session, admin)

    assert exc.value.status_code == 404

def test_update_product_success(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=15.5,
        category_id=category.id
    )

    result = ProductService.update_product("test", schema, db_session, admin)

    assert result.name == schema.name
    assert result.description == schema.description
    assert result.slug == schema.slug
    assert result.price == schema.price
    assert result.category_id == schema.category_id

def test_update_product_fail_with_invalid_name(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateProductSchema(
        name="",
        slug="test",
        description="description updated",
        price=15.5,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_product_fail_with_invalid_slug(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="",
        description="description updated",
        price=15.5,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_product_fail_with_invalid_description(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="",
        price=15.5,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_product_fail_with_invalid_price(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=0,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_product_fail_with_not_authenticated_user(db_session):
    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=0,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, None)

    assert exc.value.status_code == 401

def test_update_product_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)
    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=0,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, user)

    assert exc.value.status_code == 403

def test_update_product_fail_with_not_found_product(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=15,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 404

def test_update_product_fail_with_not_found_category(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test",
        description="description updated",
        price=15,
        category_id=uuid4()
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_product_fail_with_already_exists_new_slug(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Test", "test", "test.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    product2 = Product("Test2", "test2", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.add(product2)
    db_session.commit()

    schema = UpdateProductSchema(
        name="Test updated",
        slug="test2",
        description="description updated",
        price=15,
        category_id=category.id
    )

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product("test", schema, db_session, admin)

    assert exc.value.status_code == 400
    
def test_create_product_success(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Category", "category", "image.png")
    db_session.add(category)
    db_session.commit()
    db_session.flush()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    product = ProductService.create_product(
        "Test",
        "test",
        "description",
        10.5,
        category.id,
        image,
        db_session,
        admin
    )

    assert product.name == "Test"
    assert product.slug == "test"
    assert product.price == 10.5
    assert product.description == "description"

def test_create_product_fail_with_invalid_name(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
        "",
        "test",
        "description",
        10.5,
        uuid4(),
        image,
        db_session,
        admin
    )

    assert exc.value.status_code == 400

def test_create_product_fail_with_invalid_slug(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
        "Test",
        "",
        "description",
        10.5,
        uuid4(),
        image,
        db_session,
        admin
    )

    assert exc.value.status_code == 400

def test_create_product_fail_with_invalid_description(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
        "Test",
        "test",
        "",
        10.5,
        uuid4(),
        image,
        db_session,
        admin
    )

    assert exc.value.status_code == 400

def test_create_product_fail_with_invalid_price(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
        "Test",
        "test",
        "description",
        0,
        uuid4(),
        image,
        db_session,
        admin
    )

    assert exc.value.status_code == 400

def test_create_product_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
            "Test",
            "test",
            "description",
            0,
            uuid4(),
            None,
            db_session,
            None
        )

    assert exc.value.status_code == 401

def test_create_product_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
            "Test",
            "test",
            "description",
            0,
            uuid4(),
            None,
            db_session,
            user
        )

    assert exc.value.status_code == 403

def test_create_product_fail_with_already_exists_product_name(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Category", "category", "image.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Test", "test", "description", 10, category.id, "test.png", True)
    db_session.add(product)
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
            "Test",
            "test",
            "description",
            10.5,
            uuid4(),
            image,
            db_session,
            admin
        )

    assert exc.value.status_code == 400

def test_create_product_fail_with_not_found_category(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.create_product(
            "Test",
            "test",
            "description",
            10.5,
            uuid4(),
            image,
            db_session,
            admin
        )

    assert exc.value.status_code == 400

def test_update_product_image_success(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Teste", "teste", "image.png")
    db_session.add(category)
    db_session.flush()
    product = Product("Product", "product", "description", 10, category.id, "product.png")
    db_session.add(product)
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    result = ProductService.update_product_image("product", image, db_session, admin)

    assert result is not None

def test_update_product_image_fail_with_not_authenticated_user(db_session):
    with pytest.raises(HTTPException) as exc:
        ProductService.update_product_image("teste", None, db_session, None)

    assert exc.value.status_code == 401

def test_update_product_image_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product_image("teste", None, db_session, user)

    assert exc.value.status_code == 403

def test_update_product_image_fail_with_not_found(db_session, create_user, tmp_path, monkeypatch):
    user = create_user(db_session)
    user.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.product_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        ProductService.update_product_image("teste", image, db_session, user)

    assert exc.value.status_code == 404