"""
Authentication API tests.

This module tests:
- user registration
- user login
- current user endpoint
"""


import uuid
from app.models.user import User



def test_register_user(client):
    """
    Test user registration.
    """


    email = f"test_{uuid.uuid4().hex}@capgemini.com"


    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": "Password123!",
        },
    )


    assert response.status_code == 201


    data = response.json()


    assert data["email"] == email
    assert data["first_name"] == "Test"

def test_login_user(client, db_session):
    """
    Test user login and JWT generation.
    """

    email = f"login_{uuid.uuid4().hex}@capgemini.com"


    # Create user first
    register_response = client.post(
        "/auth/register",
        json={
            "first_name": "Login",
            "last_name": "Test",
            "email": email,
            "password": "Password123!",
        },
    )


    assert register_response.status_code == 201


    # Get verification token from database
    user = db_session.query(User).filter(
        User.email == email
    ).first()

    assert user is not None

    verification_token = user.verification_token


    # Verify email before login
    verify_user_email(
        client,
        verification_token
    )


    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Password123!",
        },
    )


    assert login_response.status_code == 200


    token = login_response.json()


    assert "access_token" in token
    assert token["token_type"] == "bearer"



def test_get_current_user(client, db_session):
    """
    Test authenticated user endpoint.
    """


    email = f"me_{uuid.uuid4().hex}@capgemini.com"


    client.post(
        "/auth/register",
        json={
            "first_name": "Current",
            "last_name": "User",
            "email": email,
            "password": "Password123!",
        },
    )


    user = db_session.query(User).filter(
        User.email == email
    ).first()

    assert user is not None

    verification_token = user.verification_token


    verify_user_email(
        client,
        verification_token
    )

    login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "Password123!",
            },
        )


    token = login_response.json()["access_token"]



    response = client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )


    assert response.status_code == 200


    data = response.json()


    assert data["email"] == email

def verify_user_email(client, token):
    """
    Verify user email before login.
    """

    response = client.get(
        f"/auth/verify-email/{token}"
    )

    assert response.status_code == 200