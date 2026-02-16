from app.services.user_service import UserService
import pytest
from fastapi import HTTPException
from uuid import uuid4

def test_get_user_data_success(db_session, create_user):
    user = create_user(db_session)
    result = UserService.get_user_data(user.id, db_session, user)
    assert result.id == user.id

def test_get_user_data_fail_because_user_not_authenticated(db_session, create_user):
    user = create_user(db_session)
    with pytest.raises(HTTPException) as exc:
        UserService.get_user_data(user.id, db_session, None)
    assert exc.value.status_code == 401

def test_get_user_data_fail_because_user_not_found(db_session, create_user):
    user = create_user(db_session)
    id = uuid4()
    with pytest.raises(HTTPException) as exc:
        UserService.get_user_data(id, db_session, user)
    assert exc.value.status_code == 404

def test_get_user_data_fail_because_user_id_is_not_equal_to_authenticated_user_id(db_session, create_user):
    user1 = create_user(db_session)
    user2 = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        UserService.get_user_data(user1.id, db_session, user2)
    assert exc.value.status_code == 403

def test_delete_account_success(db_session, create_user):
    user = create_user(db_session)
    result = UserService.delete_account(user.id, db_session, user)
    assert result["message"] == "Usuário deletado com sucesso"

def test_delete_account_fail_because_user_not_authenticated(db_session, create_user):
    user = create_user(db_session)
    with pytest.raises(HTTPException) as exc:
        UserService.delete_account(user.id, db_session, None)
    assert exc.value.status_code == 401

def test_delete_account_fail_because_user_id_not_found(db_session, create_user):
    user = create_user(db_session)
    id = uuid4()
    with pytest.raises(HTTPException) as exc:
        UserService.delete_account(id, db_session, user)
    assert exc.value.status_code == 404

def test_delete_account_fail_because_user_id_not_equal_to_user_authenticated(db_session, create_user):
    user1 = create_user(db_session)
    user2 = create_user(db_session)

    with pytest.raises(HTTPException) as exc:
        UserService.delete_account(user1.id, db_session, user2)
    assert exc.value.status_code == 403