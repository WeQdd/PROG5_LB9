from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt


app = FastAPI(title="Бонусная система", description="Простая бонусная система")


JWT_SECRET = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(BaseModel):
    username: str
    password: str
    spending: float


class BonusLevel(BaseModel):
    level: str
    min_spending: float
    cashback: float


bonus_levels = [
    BonusLevel(level="Серебро", min_spending=0, cashback=0.01),
    BonusLevel(level="Золото", min_spending=10000, cashback=0.02),
    BonusLevel(level="Платина", min_spending=20000, cashback=0.03),
]


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


users_db = {
    "admin": dict(username="admin", password="admin", spending=5000.0),
    "user": dict(username="user", password="user", spending=15000.0),
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user = users_db.get(payload["sub"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return User(**user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/bonus", response_model=dict)
async def read_bonus_data(current_user: User = Depends(get_current_user)):
    user_spending = current_user.spending
    sorted_levels = sorted(bonus_levels, key=lambda x: x.min_spending)
    current_level = None
    next_level = None
    for level in sorted_levels:
        if user_spending >= level.min_spending:
            current_level = level
        else:
            if current_level:
                next_level = level
            break
    if not next_level:
        next_level = "No higher level"
    return {
        "current_level": current_level,
        "next_level": next_level
    }