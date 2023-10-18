from passlib.context import CryptContext


class Hasher:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, secret: str) -> None:
        self.secret = secret

    def hash(self) -> str:
        return self._context.hash(secret=self.secret)

    def verify(self, hash: str) -> bool:
        return self._context.verify(secret=self.secret, hash=hash)
