from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import json
from typing import List

router = APIRouter()

class TrainRequest(BaseModel):
    data: str
    model_name: str = "hackney_downs_custom"

class TrainResponse(BaseModel):
    message: str
    training_data_size: int

@router.post("/train", response_model=TrainResponse)
async def train_model(request: TrainRequest):
    try:
        # Save training data
        training_file = f"data/{request.model_name}_training.json"

        # Load existing training data if it exists
        existing_data = []
        if os.path.exists(training_file):
            with open(training_file, 'r') as f:
                existing_data = json.load(f)

        # Add new training data
        new_entry = {
            "input": request.data,
            "timestamp": str(pd.Timestamp.now()) if 'pd' in globals() else "2025-01-01",
            "model": request.model_name
        }
        existing_data.append(new_entry)

        # Save updated training data
        os.makedirs("data", exist_ok=True)
        with open(training_file, 'w') as f:
            json.dump(existing_data, f, indent=2)

        return TrainResponse(
            message=f"Training data added to {request.model_name} model",
            training_data_size=len(existing_data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

@router.post("/train/file")
async def train_from_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        # Save the file
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"
        with open(file_path, 'wb') as f:
            f.write(content)

        # Process the training data
        training_data = []
        lines = text_content.split('\n')
        for line in lines:
            if line.strip():
                training_data.append({
                    "input": line.strip(),
                    "timestamp": "2025-01-01",
                    "source": file.filename
                })

        # Save processed training data
        training_file = f"data/{file.filename}_processed.json"
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)

        return {
            "message": f"Training file processed: {file.filename}",
            "training_samples": len(training_data),
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File training error: {str(e)}")

@router.get("/training/status")
async def get_training_status():
    try:
        training_files = []
        if os.path.exists("data"):
            training_files = [f for f in os.listdir("data") if f.endswith('.json')]

        total_samples = 0
        for file in training_files:
            try:
                with open(f"data/{file}", 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        total_samples += len(data)
            except:
                pass

        return {
            "training_files": training_files,
            "total_training_samples": total_samples,
            "status": "ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check error: {str(e)}")