import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from .claude_client import (  # noqa: E402
    PDF_MEDIA_TYPE,
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_TEXT_TYPES,
    summarize_report,
)

ALLOWED_CONTENT_TYPES = {PDF_MEDIA_TYPE, *SUPPORTED_IMAGE_TYPES, *SUPPORTED_TEXT_TYPES}

# Browsers are inconsistent about the Content-Type they send for .md/.txt uploads
# (often "" or "application/octet-stream"), so fall back to the file extension.
EXTENSION_CONTENT_TYPES = {
    ".pdf": PDF_MEDIA_TYPE,
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".txt": "text/plain",
    ".md": "text/markdown",
}

MAX_FILE_SIZE_MB = int(os.environ.get("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

app = FastAPI(title="IVF Report Summary POC")

# CORS is not a real access control for this API (a non-browser client can call it
# regardless of Origin) — it only affects which *websites* can call it from a user's
# browser. The actual usage-fencing item (rate limiting / file-size cap / access gate)
# is tracked separately for Phase 5, before this is deployed publicly. "*" is fine here
# since we send no cookies/credentials and the file-size cap above is the real guard.
allowed_origins = os.environ.get("ALLOWED_ORIGIN", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


def _resolve_content_type(file: UploadFile) -> str | None:
    if file.content_type in ALLOWED_CONTENT_TYPES:
        return file.content_type
    suffix = Path(file.filename or "").suffix.lower()
    return EXTENSION_CONTENT_TYPES.get(suffix)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/summarize")
async def summarize(file: UploadFile = File(...)) -> dict:
    content_type = _resolve_content_type(file)
    if content_type is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. "
            "Upload a PDF, JPEG, PNG, TXT, or MD file.",
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {MAX_FILE_SIZE_MB}MB limit for this POC.",
        )

    try:
        summary = summarize_report(file_bytes, content_type)
    except RuntimeError as exc:
        # e.g. missing ANTHROPIC_API_KEY — a server misconfiguration, not a client error
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 - surface upstream LLM/API failures as 502
        raise HTTPException(
            status_code=502, detail=f"Failed to generate summary: {exc}"
        ) from exc

    return {
        "filename": file.filename,
        "contentType": content_type,
        "summary": summary,
    }
