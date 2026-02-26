from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.user import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Agro test task",
)

app.include_router(user_router)