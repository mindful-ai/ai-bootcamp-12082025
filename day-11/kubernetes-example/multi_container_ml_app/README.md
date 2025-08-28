# Multi-Container ML App (Streamlit + FastAPI)

This project demonstrates a **multi-container** setup with Streamlit (frontend), FastAPI (backend), a model-serving service, and a logger service — all runnable locally via **Docker Compose**.

## Services
- **frontend**: Streamlit UI on port **8501**.
- **backend**: FastAPI that validates input and forwards to model-serving on port **5002**.
- **model_serving**: FastAPI that computes a simple prediction on port **5001**.
- **logger**: FastAPI that accepts logs at **/log** on port **5003**.

> The pipeline: `frontend` → POST `{"features": [...]}` → `backend` → forwards to `model_serving` → returns `{"prediction": ...}`.  
> The 422 error you saw was due to a request body mismatch; here it's fixed with a Pydantic model.

## Quick Start
```bash
docker compose up --build
# Open http://localhost:8501
```
Enter comma-separated numbers (e.g., `1.5, 2, 3.25`) and click **Predict**.

## Health Endpoints
- `GET http://localhost:5001/health` (model_serving)
- `GET http://localhost:5002/health` (backend)
- `GET http://localhost:5003/health` (logger)

## Tear Down
```bash
docker compose down -v
```

## Notes
- Backend validates payload shape via Pydantic (`{"features": [float, ...]}`) to avoid FastAPI 422 errors.
- Compose healthchecks ensure backend waits for model_serving to be ready.
- For a real ML model, replace the simple sum-based prediction with a persisted model.
