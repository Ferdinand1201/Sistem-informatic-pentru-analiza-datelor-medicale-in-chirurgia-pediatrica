from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from datetime import timezone

# Inițializare context pentru parole
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret JWT
SECRET_KEY = "secrettoken2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Bază de utilizatori (cu parole hash)
fake_users_db = {
    "medic": {
        "username": "medic",
        "hashed_password": pwd_context.hash("1234"),
        "role": "doctor"
    },
    "asistent": {
        "username": "asistent",
        "hashed_password": pwd_context.hash("4321"),
        "role": "nurse"
    },
    "researcher": {
        "username": "researcher",
        "hashed_password": pwd_context.hash("0000"),
        "role": "researcher"
    }
}

# Creează token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verifică token JWT și extrage userul
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")

# Decorator pentru roluri
def role_required(required_roles: list):
    def verifier(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied.")
        return user
    return verifier
