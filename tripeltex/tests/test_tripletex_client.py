import asyncio
import json

import httpx

from app.services.tripletex_client import TripletexClient


async def _make_client(handler):
    transport = httpx.MockTransport(handler)
    client = TripletexClient({"token": "Bearer token", "proxy_url": "https://api.example.com"})
    await client.client.aclose()
    client.client = httpx.AsyncClient(
        base_url=client.base_url,
        headers={"Authorization": client.token},
        transport=transport,
    )
    return client


def test_search_customer_returns_first_value():
    async def scenario():
        async def handler(request: httpx.Request):
            assert request.method == "GET"
            assert request.url.path == "/customer"
            assert request.url.params["filter"] == "Acme"
            return httpx.Response(200, json={"values": [{"id": 42, "name": "Acme"}]})

        client = await _make_client(handler)
        try:
            result = await client.search_customer("Acme")
        finally:
            await client.client.aclose()

        assert result == {"id": 42, "name": "Acme"}

    asyncio.run(scenario())


def test_create_invoice_posts_expected_payload():
    async def scenario():
        async def handler(request: httpx.Request):
            assert request.method == "POST"
            assert request.url.path == "/invoice"
            assert json.loads(request.content) == {
                "customerId": 7,
                "amount": 199.5,
                "currency": "NOK",
                "dueDate": "2026-03-31",
            }
            return httpx.Response(200, json={"id": 1001})

        client = await _make_client(handler)
        try:
            result = await client.create_invoice(7, 199.5, due_date="2026-03-31")
        finally:
            await client.client.aclose()

        assert result == {"id": 1001}

    asyncio.run(scenario())
