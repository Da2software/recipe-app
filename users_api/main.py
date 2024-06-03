from fastapi import FastAPI
from core import auth, users
from core import models, utils
from core.database import engine
import uvicorn

app = FastAPI(title="Recipe Users API")
app.add_middleware(utils.SessionMiddleware)
app.include_router(auth.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)


def run_file_mode():
    """
    this way we can run the file with pycharm in debug mode and also allow
    the reload property, remember main.app means main.py > app value inside
    :return: None
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_file_mode()
