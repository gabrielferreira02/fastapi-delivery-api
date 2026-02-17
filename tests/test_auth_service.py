import pytest
from app.schemas.auth_schemas import RegisterSchema, LoginSchema, AuthResponseSchema
from app.services.auth_service import AuthService
from app.core.security import bcrypt_context
from fastapi import HTTPException

def test_register_success(db_session):
    schema = RegisterSchema(
        first_name="nome",
        last_name="sobrenome",
        password="12345678",
        email="nome@email.com"
    )

    result = AuthService.register(schema, db_session)

    assert result.first_name == schema.first_name
    assert result.last_name == schema.last_name
    assert result.email == schema.email

def test_register_fail_with_invalid_first_name(db_session):
    schema = RegisterSchema(
        first_name="",
        last_name="sobrenome",
        password="12345678",
        email="nome@email.com"
    )    

    with pytest.raises(HTTPException) as exc:
        AuthService.register(schema, db_session)

    assert exc.value.status_code == 400

def test_register_fail_with_invalid_last_name(db_session):
    schema = RegisterSchema(
        first_name="nome",
        last_name="",
        password="12345678",
        email="nome@email.com"
    )    

    with pytest.raises(HTTPException) as exc:
        AuthService.register(schema, db_session)

    assert exc.value.status_code == 400

def test_register_fail_with_invalid_email(db_session):
    schema = RegisterSchema(
        first_name="nome",
        last_name="sobrenome",
        password="12345678",
        email=""
    )    

    with pytest.raises(HTTPException) as exc:
        AuthService.register(schema, db_session)

    assert exc.value.status_code == 400

def test_register_fail_with_invalid_password(db_session):
    schema = RegisterSchema(
        first_name="nome",
        last_name="sobrenome",
        password="1234567",
        email="nome@email.com"
    )    

    with pytest.raises(HTTPException) as exc:
        AuthService.register(schema, db_session)

    assert exc.value.status_code == 400

def test_login_success(db_session, create_user):
    user = create_user(db_session)
    user.password = bcrypt_context.hash(user.password)
    db_session.commit()

    schema = LoginSchema(email=user.email,password="12345678")

    result = AuthService.login(schema, db_session)

    assert type(result) is AuthResponseSchema
    assert result.access_token is not None
    assert result.refresh_token is not None

def test_login_fail_with_invalid_email(db_session):
    schema = LoginSchema(email="",password="12345678")

    with pytest.raises(HTTPException) as exc:
        AuthService.login(schema, db_session)

    assert exc.value.status_code == 400

def test_login_fail_with_invalid_password(db_session):
    schema = LoginSchema(email="test@email.com",password="")

    with pytest.raises(HTTPException) as exc:
        AuthService.login(schema, db_session)

    assert exc.value.status_code == 400

def test_login_fail_with_not_found_email(db_session):
    schema = LoginSchema(email="test@email.com",password="12345678")

    with pytest.raises(HTTPException) as exc:
        AuthService.login(schema, db_session)

    assert exc.value.status_code == 404

def test_login_fail_with_incorrect_password(db_session, create_user):
    user = create_user(db_session)
    user.password = bcrypt_context.hash(user.password)
    db_session.commit()
    schema = LoginSchema(email=user.email, password="1234567")

    with pytest.raises(HTTPException) as exc:
        AuthService.login(schema, db_session)

    assert exc.value.status_code == 400

