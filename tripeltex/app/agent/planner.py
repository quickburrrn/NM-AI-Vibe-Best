# app/agent/planner.py
from typing import List
from app.schemas.solve import ParsedTask, PlanStep
from app.utils.llm import call_llm  # LLM planning prompt

async def create_plan(parsed_task: ParsedTask) -> List[PlanStep]:
    """
    Convert parsed structured task into a deterministic execution plan
    """
    # Option 1: rule-based simple plan (fast & safe)
    plan = []

    if parsed_task.task_type == "create_customer" and parsed_task.customer.name:
        plan.append(PlanStep(
            action="get_or_create_customer",
            args={"name": parsed_task.customer.name, "email": parsed_task.customer.email}
        ))

    if parsed_task.task_type == "create_invoice" and parsed_task.invoice.amount:
        if parsed_task.customer.name:
            plan.append(PlanStep(
                action="get_or_create_customer",
                args={"name": parsed_task.customer.name, "email": parsed_task.customer.email}
            ))
        plan.append(PlanStep(
            action="create_invoice",
            args={"amount": parsed_task.invoice.amount, "currency": parsed_task.invoice.currency, "due_date": parsed_task.invoice.due_date}
        ))

    # Option 2: LLM-assisted planning for more complex workflows
    # plan_json = await call_llm(parsed_task.json(), task="plan_task")
    # plan = [PlanStep(**step) for step in plan_json]

    return plan