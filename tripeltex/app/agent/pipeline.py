# app/agent/pipeline.py

import asyncio
from typing import List, Optional
from app.agent.parser import parse_prompt  # your LLM parsing function
from app.agent.planner import create_plan   # your LLM planning function
from app.tools.executor import execute_step # deterministic MCP/Tripletex executor
from app.utils.validation import validate_state  # optional final validation

# Type hint for state
StateDict = dict

async def run_pipeline(
    prompt: str,
    credentials: dict,
    files: Optional[List] = None
) -> StateDict:
    """
    Main pipeline for Tripletex AI agent.

    Args:
        prompt: User/task prompt (any of 7 languages)
        credentials: {"token": ..., "proxy_url": ...}
        files: Optional list of PDFs/images attached to the task

    Returns:
        state: dict tracking all created resources (customer_id, invoice_id, etc.)
    """

    # ----------------------------
    # Step 1: Parse the prompt
    # ----------------------------
    parsed_task = await parse_prompt(prompt, files)

    # parsed_task is a Pydantic model or dict:
    # {
    #   "task_type": "create_invoice",
    #   "customer": {"name": "Ola Nordmann"},
    #   "invoice": {"amount": 2000}
    #   ...
    # }

    # ----------------------------
    # Step 2: Create execution plan
    # ----------------------------
    plan = await create_plan(parsed_task)

    # plan is a list of steps:
    # [
    #   {"action": "get_or_create_customer", "args": {...}},
    #   {"action": "create_invoice", "args": {...}}
    # ]

    # ----------------------------
    # Step 3: Execute plan
    # ----------------------------
    state: StateDict = {}  # Track resource IDs

    for step in plan:
        try:
            result = await execute_step(step, state, credentials)
            # Update state with result
            state.update(result)
        except Exception as e:
            # You can optionally handle per-step failures
            print(f"Error executing {step['action']}: {e}")
            raise e

    # ----------------------------
    # Step 4: Validation (optional but recommended)
    # ----------------------------
    try:
        await validate_state(state, credentials)
    except AssertionError as e:
        print(f"Validation failed: {e}")
        raise e

    return state