"""Example test file, placeholder for incoming code"""

from fastapi.testclient import TestClient
import pytest
from llm_generation.app.server import app

client = TestClient(app)


def test_server_startup():
    """
    Test if the FastAPI server starts correctly and responds to /docs endpoint.
    """
    with client:
        response = client.get("/docs")
        assert response.status_code == 200


def test_generate_answer():
    """
    Test the "/generate_answer" endpoint with plain text input returns not null response
    """
    # todo
    pass
