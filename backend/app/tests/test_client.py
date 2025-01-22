import asyncio
import os
import sys

import pytest
from typing import List
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from main import app
from models import Base



DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test"


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
async def test_db():
    async with async_session_maker.begin(async_session_maker) as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_session_maker

    async with async_session_maker.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@pytest.mark.asyncio
async def test_create_client(test_db, client):
    client_data = {
        "name": "test_name",
        "sur_name": "test_surname",
        "middle_name": "test_middle_name",
        "contacts": {
            "phone_number": "9997775500",
            "email": "test@mail.ru",
            "facebook": "test_face",
            "vk": "test_vk"
            }
            }
    response = client.post("/clients", json=client_data)
    assert response.status_code == 201
    assert response.json()["name"] == client_data["name"]
    assert response.json()["sur_name"] == client_data["last_name"]
    assert response.json()["email"] == client_data["email"]

@pytest.mark.asyncio
async def test_fetch_all_clients(test_db, client):
    client_data = {
        "name": "test_name",
        "sur_name": "test_surname",
        "middle_name": "test_middle_name",
        "contacts": {
            "phone_number": "9997775500",
            "email": "test@mail.ru",
            "facebook": "test_face",
            "vk": "test_vk"
            }
            
    }
    client.post("/clients", json=client_data)

    response = client.get("/clients")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == client_data["email"]

@pytest.mark.asyncio
async def test_update_client(test_db, client):
    client_data = {
        "name": "test_name",
        "sur_name": "test_surname",
        "middle_name": "test_middle_name",
        "contacts": {
            "phone_number": "9997775500",
            "email": "test@mail.ru",
            "facebook": "test_face",
            "vk": "test_vk"
            }
            
    }
    response = client.post("/clients", json=client_data)
    client_id = response.json()["id"]
    update_data = {
        "first_name": "Updated",
        "last_name": "Client",
        "contacts": {"phone_number": "+79991234568"},
    }
    response = client.put(f"/clients/{client_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == update_data["first_name"]
    assert response.json()["contacts"]["phone_number"] == update_data["contacts"]["phone_number"]

@pytest.mark.asyncio
async def test_delete_client(test_db, client):
     client_data = {
        "name": "test_name",
        "sur_name": "test_surname",
        "middle_name": "test_middle_name",
        "contacts": {
            "phone_number": "9997775500",
            "email": "test@mail.ru",
            "facebook": "test_face",
            "vk": "test_vk"
            }
            
    }
     response = client.post("/clients", json=client_data)
     client_id = response.json()["id"]

     response = client.delete(f"/clients/{client_id}")
     assert response.status_code == 204
     response = client.put(f"/clients/{client_id}", json={"first_name": "Updated"})
     assert response.status_code == 404
