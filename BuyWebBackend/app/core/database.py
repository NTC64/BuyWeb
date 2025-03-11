from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Integer, default=1)
    role = Column(String(20), default='user')

# Create database engine
engine = create_engine('sqlite:///buywebapp.db')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
# Create sample users
sample_users = [
    User(
        username="john_doe",
        email="john@example.com",
        password="hashed_password_1",  # In real app, this should be properly hashed
        first_name="John",
        last_name="Doe",
        phone="123-456-7890",
        address="123 Main St, City, Country",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=1,
        role="user"
    ),
    User(
        username="jane_smith", 
        email="jane@example.com",
        password="hashed_password_2",  # In real app, this should be properly hashed
        first_name="Jane",
        last_name="Smith",
        phone="098-765-4321",
        address="456 Oak Ave, Town, Country",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=1,
        role="admin"
    )
]

# Add sample users to database
session = Session()
for user in sample_users:
    session.add(user)
session.commit()
session.close()
