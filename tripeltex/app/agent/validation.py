# app/utils/validation.py
from app.services.tripletex_client import TripletexClient

async def validate_state(state: dict, credentials: dict):
    """
    Check that all created resources exist and match expected values.
    Raise AssertionError if validation fails.
    """
    client = TripletexClient(credentials)

    if "customer_id" in state and state["customer_id"]:
        customer = await client.get_customer(state["customer_id"])
        assert customer is not None, "Customer not found"

    if "invoice_id" in state and state["invoice_id"]:
        invoice = await client.get_invoice(state["invoice_id"])
        assert invoice is not None, "Invoice not found"
        assert invoice["amount"] > 0, "Invoice amount invalid"