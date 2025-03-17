from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from app.config.settings import get_settings

from app import routes

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Examboard AI API Infrastructure"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
