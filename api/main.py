from fastapi import FastAPI

from api.routes.articles import router as articles_router

app = FastAPI(
    title="Orbis API",
    version="0.1.0",
    description="API inicial para consulta de artigos no banco de dados.",
)

app.include_router(articles_router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
