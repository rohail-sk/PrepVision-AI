"""Helper functions for AI-powered question answering."""

import os
import time
import requests

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)
HF_API_KEY = os.getenv("HF_API_KEY")
# Hugging Face router OpenAI-compatible chat endpoint
HF_MODEL_URL = os.getenv(
    "HF_MODEL_URL",
    "https://router.huggingface.co/v1/chat/completions"
)
HF_CHAT_MODEL = os.getenv("HF_CHAT_MODEL", "Qwen/Qwen2.5-7B-Instruct")


def _resolve_hf_url():
    """Return a router.huggingface.co URL and normalize old/deprecated values."""
    url = (HF_MODEL_URL or "").strip()
    deprecated_host = "https://api-inference.huggingface.co"
    router_host = "https://router.huggingface.co"

    if url.startswith(deprecated_host):
        return "https://router.huggingface.co/v1/chat/completions"

    # If an old hf-inference router URL is provided, move to chat completions endpoint.
    if "/hf-inference/" in url:
        return "https://router.huggingface.co/v1/chat/completions"

    return url or "https://router.huggingface.co/v1/chat/completions"


def _build_exam_prompt(question):
    """Create a consistent exam-oriented prompt."""
    return (
        "Answer the following question in a clear and exam-oriented manner.\n\n"
        "Include:\n"
        "- Definition\n"
        "- Explanation\n"
        "- Example (if applicable)\n\n"
        f"Question: {question}"
    )


def _extract_text_from_response(response):
    """Safely extract plain text from Gemini response object."""
    text = getattr(response, "text", "")
    if text:
        return text.strip()

    # Fallback for responses where .text is empty but parts are present.
    candidates = getattr(response, "candidates", []) or []
    if candidates:
        parts = getattr(candidates[0].content, "parts", [])
        joined = " ".join(getattr(part, "text", "") for part in parts if getattr(part, "text", ""))
        return joined.strip()

    return ""


def get_hf_answer(question):
    """Generate answer using HuggingFace inference API as a fallback."""
    if not HF_API_KEY:
        return "Error generating response: HF_API_KEY is missing in .env"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": HF_CHAT_MODEL,
        "messages": [
            {
                "role": "user",
                "content": _build_exam_prompt(question)
            }
        ],
        "max_tokens": 220,
        "temperature": 0.3
    }

    hf_url = _resolve_hf_url()

    try:
        response = requests.post(hf_url, headers=headers, json=payload, timeout=60)
        raw_text = (response.text or "").strip()

        # Successful responses are JSON in OpenAI-compatible format.
        if response.status_code == 200:
            if not raw_text:
                return "Error generating response: HuggingFace returned an empty response"

            try:
                data = response.json()
            except ValueError:
                # Some gateways may return plain text; treat it as usable output.
                return raw_text

            # OpenAI-style format: {"choices": [{"message": {"content": "..."}}]}
            if isinstance(data, dict):
                choices = data.get("choices") or []
                if choices and isinstance(choices[0], dict):
                    message = choices[0].get("message") or {}
                    generated = str(message.get("content", "")).strip()
                else:
                    generated = ""
                if generated:
                    return generated

            return "Error generating response: HuggingFace returned an empty response"

        # Non-200 errors: parse JSON if possible, else include body snippet.
        error_message = "No response body"
        if raw_text:
            try:
                data = response.json()
                if isinstance(data, dict):
                    error_message = data.get("error") or str(data)
                else:
                    error_message = str(data)
            except ValueError:
                error_message = raw_text[:300]

        return f"Error generating response: HuggingFace API failed ({response.status_code}): {error_message}"
    except requests.RequestException as req_err:
        return f"Error generating response: HuggingFace request error: {req_err}"


def get_ai_answer(question, api_key=None):
    """
    Generate an exam-oriented answer for a user question using an external AI API.

    Args:
        question (str): User question from the frontend.
        api_key (str | None): API key loaded from environment.

    Returns:
        str: Clean answer text suitable for exam preparation.
    """
    if api_key:
        # Keep compatibility with existing caller signature.
        genai.configure(api_key=api_key)

    prompt = _build_exam_prompt(question)

    try:
        print("Using Gemini...")
        print(f"Using model: {MODEL_NAME}")
        response = model.generate_content(prompt)
        answer = _extract_text_from_response(response)
        time.sleep(2)  # Prevent rate limiting by spacing calls.
        return answer or "Error generating response: Empty response from Gemini API"
    except Exception as e:
        err = str(e)
        print(f"Gemini failed: {err}")

        if "429" in err or "quota" in err.lower():
            print("Switching to HuggingFace...")
            return get_hf_answer(question)

        return f"Error generating response: {err}"














