# app/services/tripletex_client.py
import httpx

class TripletexClient:
    def __init__(self, credentials=None):
        self.token = credentials.get("token") if credentials else ""
        self.base_url = credentials.get("proxy_url") if credentials else ""
        self.client = httpx.AsyncClient(base_url=self.base_url, headers={"Authorization": self.token})

    async def search_customer(self, name: str):
        r = await self.client.get(f"/customer?filter={name}")
        data = r.json()
        return data["values"][0] if data.get("values") else None

    async def create_customer(self, name: str, email: str = None):
        payload = {"name": name, "email": email}
        r = await self.client.post("/customer", json=payload)
        return r.json()

    async def create_invoice(self, customer_id: int, amount: float, currency: str = "NOK", due_date: str = None):
        payload = {"customerId": customer_id, "amount": amount, "currency": currency, "dueDate": due_date}
        r = await self.client.post("/invoice", json=payload)
        return r.json()

    async def get_customer(self, customer_id: int):
        r = await self.client.get(f"/customer/{customer_id}")
        return r.json()

    async def get_invoice(self, invoice_id: int):
        r = await self.client.get(f"/invoice/{invoice_id}")
        return r.json()