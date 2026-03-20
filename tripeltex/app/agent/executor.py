# app/tools/executor.py
from fastmcp import FastMCP
from app.services.tripletex_client import TripletexClient
from app.schemas.solve import PlanStep

mcp = FastMCP("tripeltex-agent")

# ----------------------------
# MCP tools (each calls Tripletex API)
# ----------------------------

@mcp.tool()
async def get_or_create_customer(name: str, email: str = None) -> dict:
    client = TripletexClient()
    existing = await client.search_customer(name)
    if existing:
        return {"customer_id": existing["id"]}
    created = await client.create_customer(name, email)
    return {"customer_id": created["id"]}

@mcp.tool()
async def create_invoice(customer_id: int, amount: float, currency: str = "NOK", due_date: str = None) -> dict:
    client = TripletexClient()
    invoice = await client.create_invoice(customer_id, amount, currency, due_date)
    return {"invoice_id": invoice["id"]}

# ----------------------------
# Executor engine
# ----------------------------
async def execute_step(step: PlanStep, state: dict, credentials: dict) -> dict:
    """
    Execute a single step using MCP tools and return updated state
    """
    # Map action to tool
    action_map = {
        "get_or_create_customer": get_or_create_customer,
        "create_invoice": create_invoice
        # Add other actions here
    }

    tool_func = action_map.get(step.action)
    if not tool_func:
        raise ValueError(f"Unknown action {step.action}")

    # Call tool with args (merge state if needed)
    result = await tool_func(**step.args)
    return result
