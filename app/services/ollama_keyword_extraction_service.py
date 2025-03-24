from ollama import chat
import json
import os
import ast
from dotenv import load_dotenv
from typing import List

load_dotenv()

LLAMA_KEYWORD_MODEL = os.getenv("LLAMA_KEYWORD_MODEL", "llama2:2b")
LLAMA_MODEL = os.getenv("LLAMA_MODEL")


def extract_keywords_from_prompt(prompt: str) -> List[str]:
    system_prompt = {
        "role": "system",
        "content": (
            "You are a keyword extraction assistant. Your job is to extract 2 to 5 meaningful keywords or named entities from a user's question. "
            "Only include specific terms such as people, places (United States, Russia, New York, etc), organizations, titles (e.g., President, Sir, Ma'am), holidays, or high-level concepts. "
            "Use sentiment or emotional cues to add one keyword related to the user's intent or tone (e.g., fear, protest, support, alliance, tension). "
            "Do not include general words like 'who', 'what', 'is', or 'the'. "
            "Return ONLY a valid Python list of lowercase strings with no explanation, such as: ['detroit', 'lions', 'football']."
        ),
    }

    user_prompt = {"role": "user", "content": prompt}

    try:
        response = chat(
            model=LLAMA_MODEL,
            messages=[system_prompt, user_prompt],
        )

        raw_output = response.get("message", {}).get("content", "[]")

        # Safely parse output as Python list
        keywords = ast.literal_eval(raw_output.strip())

        if not isinstance(keywords, list):
            raise ValueError("Returned value is not a list.")

        return [kw.lower().strip() for kw in keywords if isinstance(kw, str)]

    except Exception as e:
        print(f"❌ Keyword extraction failed: {e}")
        return []


def save_keywords_to_json(prompt: str, keywords: list[str]):
    log_path = "data/extracted_keywords.json"

    try:
        existing = []
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                existing = json.load(f)

        existing.append({"prompt": prompt, "keywords": keywords})

        with open(log_path, "w") as f:
            json.dump(existing, f, indent=2)

    except Exception as e:
        print(f"⚠️ Could not save keywords: {e}")
