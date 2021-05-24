"""Models"""
from sqlalchemy import Column, Integer, String
from labbot.database import Base

class User(Base):
    """User Class"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'

    def test(self):
        """Just here for pylint right now"""
