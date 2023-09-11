from fastapi import FastAPI

from app.bookings.router import router as router_bookings


app = FastAPI()
app.include_router(router_bookings)


@app.get("/hello")
def get_hello():
    return {"message": "Hello"}


@app.post("/message")
def post_message(message: str):
    return {"message": f"I got your message: '{message}'"}
