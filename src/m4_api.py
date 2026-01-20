# src/m4_api.py

from fastapi import FastAPI, Depends, HTTPException
from src.m4_auth import authenticate_user, create_access_token
from src.m4_dependencies import get_current_user
from src.m4_models import LoginRequest, TokenResponse, ChatRequest, ChatResponse
from src.m3_rag_pipeline import ask

app = FastAPI(title="Secure Internal Chatbot API")


@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {
            "sub": user["username"],
            "role": user["role"],
        }
    )

    return {"access_token": token}


@app.post("/chat", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    role = current_user["role"]

    answer = ask(data.query, role)

    return {"answer": answer}
