from app.services.category_service import CategoryService
from fastapi import UploadFile, HTTPException
from starlette.datastructures import Headers
from io import BytesIO
import pytest
from app.models.category import Category
from app.schemas.category_schemas import UpdateCategoryNameAndSlugSchema

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

def test_create_category_success(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    category = CategoryService.create_category("Lançamentos", "lancamentos", image, db_session, admin)

    assert category.name == "Lançamentos"
    assert category.slug == "lancamentos"

def test_create_category_fail_with_invalid_name(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.create_category("", "lancamentos", image, db_session, admin)

    assert exc.value.status_code == 400

def test_create_category_fail_with_invalid_slug(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.create_category("Lançamentos", "", image, db_session, admin)

    assert exc.value.status_code == 400

def test_create_category_fail_because_user_is_not_admin(db_session, create_user, tmp_path, monkeypatch):
    user = create_user(db_session)

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.create_category("Lançamentos", "lancamentos", image, db_session, user)

    assert exc.value.status_code == 403

def test_create_category_fail_because_user_not_authenticated(db_session, create_user, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.create_category("Lançamentos", "lancamentos", image, db_session, None)

    assert exc.value.status_code == 401

def test_create_category_fail_with_invalid_name(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Lançamentos", "lancamentos", "image_url")
    db_session.add(category)
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.create_category("Lançamentos", "lancamentos", image, db_session, admin)

    assert exc.value.status_code == 400

def test_get_all_categories(db_session):
    category = Category("Lançamentos", "lancamentos", "image_url")
    category2 = Category("Bebidas", "bebidas", "image_url")
    db_session.add(category)
    db_session.add(category2)
    db_session.commit()

    categories = CategoryService.get_all_categories(db_session)

    assert len(categories) == 2

def test_get_category_with_success(db_session):
    new_category = Category("Lançamentos", "lancamentos", "image_url")
    db_session.add(new_category)
    db_session.commit()

    category = CategoryService.get_category("lancamentos", db_session)

    assert category.name == new_category.name

def test_get_category_fail_because_slug_not_exists(db_session):

    with pytest.raises(HTTPException) as exc:
        CategoryService.get_category("lancamentos", db_session)

    assert exc.value.status_code == 404

def test_delete_category_success(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    category = Category("Teste", "teste", "test.png")
    db_session.add(category)
    db_session.commit()

    file_path = tmp_path / "test.png"
    file_path.write_text("fake image content")

    CategoryService.delete_category("teste", db_session, admin)

    deleted = db_session.query(Category).filter_by(slug="teste").first()
    assert deleted is None

    assert not file_path.exists()

def test_delete_category_fail_because_user_is_not_admin(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        CategoryService.delete_category("teste", db_session, user)
    
    assert exc.value.status_code == 403

def test_delete_category_fail_because_user_not_authenticated(db_session, create_user):
    with pytest.raises(HTTPException) as exc:
        CategoryService.delete_category("teste", db_session, None)
    
    assert exc.value.status_code == 401

def test_delete_category_fail_because_slug_doesnt_exists(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Teste", "teste", "test.png")
    db_session.add(category)
    db_session.commit()

    with pytest.raises(HTTPException) as exc:
        CategoryService.delete_category("lançamentos", db_session, admin)
    
    assert exc.value.status_code == 404

def test_update_category_success(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Teste", "teste", "image.png")
    db_session.add(category)
    db_session.commit()

    schema = UpdateCategoryNameAndSlugSchema(name="Teste atualizado", slug="teste")

    result = CategoryService.update_category("teste", schema, db_session, admin)

    assert result.name == schema.name
    assert result.slug == schema.slug

def test_update_category_fail_with_invalid_name(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateCategoryNameAndSlugSchema(name="", slug="teste")

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category("teste", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_category_fail_with_invalid_slug(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateCategoryNameAndSlugSchema(name="Test", slug="")

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category("teste", schema, db_session, admin)

    assert exc.value.status_code == 400

def test_update_category_fail_with_not_authenticated_user(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateCategoryNameAndSlugSchema(name="Teste", slug="teste")

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category("teste", schema, db_session, None)

    assert exc.value.status_code == 401

def test_update_category_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    schema = UpdateCategoryNameAndSlugSchema(name="Teste", slug="teste")

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category("teste", schema, db_session, user)

    assert exc.value.status_code == 403

def test_update_category_fail_with_not_found_category(db_session, create_user):
    admin = create_user(db_session)
    admin.is_admin = True
    db_session.commit()

    schema = UpdateCategoryNameAndSlugSchema(name="Teste", slug="teste")

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category("teste", schema, db_session, admin)

    assert exc.value.status_code == 404

def test_update_category_image_success(db_session, create_user, tmp_path, monkeypatch):
    admin = create_user(db_session)
    admin.is_admin = True
    category = Category("Teste", "teste", "image.png")
    db_session.add(category)
    db_session.commit()

    monkeypatch.setattr("app.services.category_service.UPLOAD_DIR", tmp_path)

    image = create_fake_image()

    result = CategoryService.update_category_image("teste", image, db_session, admin)

    assert result is not None

def test_update_category_image_fail_with_not_authenticated_user(db_session, create_user):
    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category_image("teste", None, db_session, None)

    assert exc.value.status_code == 401

def test_update_category_image_fail_with_not_admin_user(db_session, create_user):
    user = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category_image("teste", None, db_session, user)

    assert exc.value.status_code == 403

def test_update_category_image_fail_with_not_found_category(db_session, create_user):
    user = create_user(db_session)
    user.is_admin = True
    db_session.commit()

    image = create_fake_image()

    with pytest.raises(HTTPException) as exc:
        CategoryService.update_category_image("teste", image, db_session, user)

    assert exc.value.status_code == 404