import json
import time
from openai import OpenAI

client = OpenAI()

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def fill_prompt(template, row):
    text = template
    for key, value in row.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text

def call_llm(prompt, model="gpt-4o-mini"):
    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    latency_ms = int((time.time() - start) * 1000)
    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except Exception:
        result = {
            "verdict": "needs_review",
            "confidence": 0.0,
            "reason": "Model returned invalid JSON",
            "suggested_value": None
        }

    return result, latency_ms