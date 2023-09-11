from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels


app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)


@app.get("/hello")
def get_hello():
    return {"message": "Hello"}


@app.post("/message")
def post_message(message: str):
    return {"message": f"I got your message: '{message}'"}
