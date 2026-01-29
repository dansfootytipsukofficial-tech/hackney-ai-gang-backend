from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import os

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str  # python, javascript, bash

class CodeExecutionResponse(BaseModel):
    output: str
    error: str
    success: bool

@router.post("/code/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    try:
        if request.language == "python":
            return await execute_python(request.code)
        elif request.language == "javascript":
            return await execute_javascript(request.code)
        elif request.language == "bash":
            return await execute_bash(request.code)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code execution error: {str(e)}")

async def execute_python(code: str) -> CodeExecutionResponse:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        os.unlink(temp_file)

        return CodeExecutionResponse(
            output=result.stdout,
            error=result.stderr,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return CodeExecutionResponse(
            output="",
            error="Code execution timed out after 30 seconds",
            success=False
        )

async def execute_javascript(code: str) -> CodeExecutionResponse:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        result = subprocess.run(
            ['node', temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        os.unlink(temp_file)

        return CodeExecutionResponse(
            output=result.stdout,
            error=result.stderr,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return CodeExecutionResponse(
            output="",
            error="Code execution timed out after 30 seconds",
            success=False
        )

async def execute_bash(code: str) -> CodeExecutionResponse:
    try:
        result = subprocess.run(
            ['bash', '-c', code],
            capture_output=True,
            text=True,
            timeout=30
        )

        return CodeExecutionResponse(
            output=result.stdout,
            error=result.stderr,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired:
        return CodeExecutionResponse(
            output="",
            error="Command execution timed out after 30 seconds",
            success=False
        )