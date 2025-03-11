from fastapi import FastAPI
from .core.database import User, Session

app = FastAPI()

@app.get("/")
def read_root():
    session = Session()
    users = session.query(User).all()
    session.close()
    
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "address": user.address,
            "role": user.role,
            "is_active": user.is_active
        })
    
    return {"users": user_list}
