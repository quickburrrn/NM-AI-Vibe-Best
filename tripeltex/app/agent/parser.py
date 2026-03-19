# app/agent/parser.py
import asyncio
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.solve import ParsedTask
from app.utils.ocr import extract_text_from_file
from app.utils.llm import call_llm  # your wrapper around OpenAI or other LLM

async def parse_prompt(prompt: str, files: Optional[List] = None) -> ParsedTask:
    """
    Parse the raw prompt (any language) and optional files
    into structured JSON (ParsedTask Pydantic model)
    """
    text = prompt

    # Extract text from files (PDFs/images)
    if files:
        for f in files:
            extracted_text = await extract_text_from_file(f)
            text += "\n" + extracted_text

    # LLM parsing
    # call_llm should implement your parsing prompt + JSON output
    response_json = await call_llm(
        prompt=text,
        task="parse_task"  # internally selects the parsing prompt template
    )

    # Validate and return structured Pydantic model
    parsed_task = ParsedTask.model_validate_json(response_json)
    return parsed_task