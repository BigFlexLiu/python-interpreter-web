Great, thank you for providing the additional details. Here's the updated README file with the information you've provided:

---

# Python Interpreter Web

## Description

Python Interpreter Web is an online Python interpreter that includes an editor and an interpreter. It allows users to submit Python code for execution securely, providing a robust environment for data analysis and scientific computing with libraries such as `pandas` and `scipy`.

## Prerequisites

- Python 3.11+
- Node.js (for TypeScript and other frontend dependencies)
- Virtual environment (venv) for Python dependencies

## Installation

### Frontend (in frontend/)

1. **Install Node.js dependencies**:

    ```bash
    npm install
    ```

2. **Run the frontend development server**:

    ```bash
    npm run dev
    ```

### Backend (in backend/)

1. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:

    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3. **Install Python dependencies**:

    ```bash
    pip install -r dependencies.txt
    ```

4. **Run the FastAPI server**:

    ```bash
    uvicorn main:app --reload
    ```

## Usage

### Starting the FastAPI Server
1. **Start UI**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Run the FastAPI server**:

    ```bash
    cd backend
    uvicorn main:app --reload
    ```
