from fastapi import FastAPI
import models
from database import engine, get_db
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)
