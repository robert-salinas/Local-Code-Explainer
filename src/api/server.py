from fastapi import FastAPI, HTTPException
from api.schemas import ExplainRequest, ExplainResponse
from explainer.explainer import CodeExplainer
import os

app = FastAPI(
    title="Local Code Explainer API",
    description="API para explicar código localmente usando LLMs.",
    version="0.1.0",
)


@app.post("/explain", response_model=ExplainResponse)
async def explain_code(request: ExplainRequest):
    if not os.path.exists(request.path):
        raise HTTPException(
            status_code=404, detail=f"Archivo '{request.path}' no encontrado."
        )

    try:
        explainer = CodeExplainer(model=request.model, use_cache=request.use_cache)
        result = explainer.explain(request.path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
