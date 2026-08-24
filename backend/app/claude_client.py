import base64
import os

from anthropic import Anthropic

from .prompt import SYSTEM_PROMPT, USER_PROMPT

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
MAX_TOKENS = int(os.environ.get("CLAUDE_MAX_TOKENS", "2048"))

PDF_MEDIA_TYPE = "application/pdf"
SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png"}
SUPPORTED_TEXT_TYPES = {"text/plain", "text/markdown"}


def _client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    return Anthropic(api_key=api_key)


def _content_block(file_bytes: bytes, content_type: str) -> dict:
    data = base64.standard_b64encode(file_bytes).decode("utf-8")
    if content_type == PDF_MEDIA_TYPE:
        return {
            "type": "document",
            "source": {"type": "base64", "media_type": PDF_MEDIA_TYPE, "data": data},
        }
    if content_type in SUPPORTED_IMAGE_TYPES:
        media_type = "image/jpeg" if content_type == "image/jpg" else content_type
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": data},
        }
    if content_type in SUPPORTED_TEXT_TYPES:
        # Plain text/Markdown reports (e.g. a lab's exported text report) have no
        # document/image content-block type in the API — just pass the decoded text.
        text = file_bytes.decode("utf-8", errors="replace")
        return {"type": "text", "text": f"Report content follows:\n\n{text}"}
    raise ValueError(f"Unsupported content type: {content_type}")


def summarize_report(file_bytes: bytes, content_type: str) -> str:
    """Send a report (PDF or image) directly to Claude and return the Markdown summary."""
    client = _client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    _content_block(file_bytes, content_type),
                    {"type": "text", "text": USER_PROMPT},
                ],
            }
        ],
    )
    text_parts = [block.text for block in message.content if block.type == "text"]
    return "\n".join(text_parts).strip()
