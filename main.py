from app.api import app

# entrypoint for uvicorn; module should expose `app`

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=app.extra.get("PORT", 8080))
