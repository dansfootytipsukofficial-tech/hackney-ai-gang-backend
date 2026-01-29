from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from app.routes import chat, images, code_execution, web_search, train

app = FastAPI(title="HACKNEY DOWNS AI", description="Advanced AI Platform with Multi-Model Support")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(images.router, prefix="/api", tags=["images"])
app.include_router(code_execution.router, prefix="/api", tags=["code_execution"])
app.include_router(web_search.router, prefix="/api", tags=["web_search"])
app.include_router(train.router, prefix="/api", tags=["train"])

# Static files for training data
# app.mount("/data", StaticFiles(directory="data"), name="data")

# Serve static files (HTML, CSS, JS)
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def root():
    return {"message": "HACKNEY DOWNS AI Platform", "status": "running"}

@app.get("/api/models")
async def get_available_models():
    return {
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI"},
            {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic"},
            {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
            {"id": "grok-code-fast-1", "name": "Grok Code Fast", "provider": "xAI"},
            {"id": "github-copilot", "name": "GitHub Copilot Style", "provider": "OpenAI"},
            {"id": "local-llama", "name": "Local Llama", "provider": "Local"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)