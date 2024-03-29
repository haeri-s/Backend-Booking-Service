from fastapi import APIRouter, Depends, HTTPException, status, Header
# from server.accounts.db import account_tb
from fastapi.security import OAuth2PasswordRequestForm
from server.database import database, get_db
from server.accounts.models import Account, AccountCreateForm
from server.utils.exceptions import CustomHTTPException
import uuid
from server.auth.models import LoginForm, LoginToken, Token, TokenData
from server.accounts.schemas import AccountDB
from server.auth.auth import create_access_token
from .dependencies import get_token_header
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["auths"],
)

@router.post('/login', response_model=LoginToken)
def login(data: LoginForm, db: Session=Depends(get_db)):
    user = db.query(AccountDB).filter(AccountDB.email == data.username).first()
    if not user.password == data.password:
        raise CustomHTTPException(msg="비밀번호를 다시 확인해주세요.", code="NOT_MATCH_PASSWORD")
    result = create_access_token({'email': user.email, 'name': user.name, 'mobile': user.mobile})
    result['user'] = user

    return result
