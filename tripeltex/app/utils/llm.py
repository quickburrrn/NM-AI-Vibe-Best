# app/utils/llm.py
import openai
import json

async def call_llm(prompt: str, task: str) -> dict:
    """
    Call LLM for parsing or planning tasks.
    Returns a JSON dict.
    """
    system_prompt = ""
    if task == "parse_task":
        system_prompt = "Parse user prompt into structured JSON (see schema)."
    elif task == "plan_task":
        system_prompt = "Convert structured task JSON into execution steps."

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    # Ensure JSON parsing
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: try eval, but ideally handle properly
        return eval(content)