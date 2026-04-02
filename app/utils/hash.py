from passlib.context import CryptContext # instala passlib[bcrypt]


# Configuración del hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)