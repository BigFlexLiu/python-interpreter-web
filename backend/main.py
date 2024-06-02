from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess
import tempfile
import sys

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CodeSubmission(Base):
    __tablename__ = "code_submissions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text, nullable=False)
    output = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

class Code(BaseModel):
    code: str

def check_forbidden_imports(code: str) -> bool:
    FORBIDDEN_MODULES = [
        'os', 'sys', 'subprocess', 'shutil', 'ctypes', 'socket', 'http', 'urllib', 'multiprocessing'
    ]
    for module in FORBIDDEN_MODULES:
        if f'import {module}' in code or f'from {module} import' in code:
            return True
    return False

# Replace file paths with <main.py> in traceback
def sanitize_traceback(tb: str) -> str:
    sanitized_tb = []
    for line in tb.splitlines():
        if 'File "' in line:
            sanitized_tb.append('  File "main.py",' + line.split('",', 1)[1])
        else:
            sanitized_tb.append(line)
    return '\n'.join(sanitized_tb)

def execute_code(code: str) -> dict:
    if check_forbidden_imports(code):
        return {"output": "", "error": "Code contains forbidden imports."}

    try:
        python_executable = sys.executable
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as tmpfile:
            tmpfile.write(code)
            tmpfile.flush()
            result = subprocess.run(
                [python_executable, tmpfile.name],
                capture_output=True,
                text=True,
                timeout=30
            )
            error_output = sanitize_traceback(result.stderr) if result.stderr else ""
            return {"output": result.stdout, "error": error_output}
    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Execution timed out"}

@app.post("/test-code")
async def test_code(code: Code):
    return execute_code(code.code)

# Saves code and output to the database if it runs without error
@app.post("/submit-code")
async def submit_code(code: Code):
    output = execute_code(code.code)
    if output["error"]:
        return {"error": output["error"]}

    db = SessionLocal()
    db_code_submission = CodeSubmission(code=code.code, output=output["output"])
    db.add(db_code_submission)
    db.commit()
    db.refresh(db_code_submission)
    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
