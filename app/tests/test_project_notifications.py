"""
Project notification integration tests.

This module verifies that project events
create the expected notifications.
"""

import uuid

from app.models.notification import Notification
from app.models.user import User


def verify_user_email(client, token):
    """
    Verify a user's email before login.
    """

    response = client.get(
        f"/auth/verify-email/{token}"
    )

    assert response.status_code == 200


def create_and_login_user(
    client,
    db_session,
    prefix: str,
):
    """
    Create, verify and login a test user.
    """

    email = (
        f"{prefix}_{uuid.uuid4().hex}"
        "@capgemini.com"
    )

    register_response = client.post(
        "/auth/register",
        json={
            "first_name": "Project",
            "last_name": "Test",
            "email": email,
            "password": "Password123!",
        },
    )

    assert register_response.status_code == 201

    user = (
        db_session.query(User)
        .filter(User.email == email)
        .first()
    )

    assert user is not None
    assert user.verification_token is not None

    verify_user_email(
        client,
        user.verification_token,
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Password123!",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    return user, {
        "Authorization": f"Bearer {access_token}"
    }


def test_project_notifications(
    client,
    db_session,
):
    """
    Test all project notification events:

    1. Project creation
    2. Member addition
    3. Member role update
    4. Project update
    5. Member removal
    6. Project deletion
    """

    # ==========================================================
    # CREATE USERS
    # ==========================================================

    owner, owner_headers = create_and_login_user(
        client,
        db_session,
        "project_owner",
    )

    member, member_headers = create_and_login_user(
        client,
        db_session,
        "project_member",
    )

    # ==========================================================
    # 1. CREATE PROJECT
    # ==========================================================

    create_response = client.post(
        "/projects",
        headers=owner_headers,
        json={
            "name": "Notification Test Project",
            "description": (
                "Project used to test project notifications."
            ),
        },
    )

    assert create_response.status_code == 201

    project = create_response.json()

    project_id = project["id"]

    owner_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == owner.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert owner_notification is not None
    assert owner_notification.level == "SUCCESS"
    assert owner_notification.is_read is False

    # ==========================================================
    # 2. ADD MEMBER
    # ==========================================================

    add_member_response = client.post(
        f"/projects/{project_id}/members",
        headers=owner_headers,
        json={
            "email": member.email,
            "role": "COLLABORATOR",
        },
    )

    assert add_member_response.status_code == 201

    member_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == member.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert member_notification is not None
    assert member_notification.level == "INFO"
    assert member_notification.is_read is False

    # ==========================================================
    # 3. UPDATE MEMBER ROLE
    # ==========================================================

    update_role_response = client.put(
        f"/projects/{project_id}/members/{member.id}",
        headers=owner_headers,
        json={
            "role": "READER",
        },
    )

    assert update_role_response.status_code == 200

    role_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == member.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert role_notification is not None
    assert role_notification.level == "INFO"
    assert "Rôle" in role_notification.title

    # ==========================================================
    # 4. UPDATE PROJECT
    # ==========================================================

    update_project_response = client.put(
        f"/projects/{project_id}",
        headers=owner_headers,
        json={
            "name": "Updated Notification Project",
        },
    )

    assert update_project_response.status_code == 200

    owner_update_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == owner.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert owner_update_notification is not None
    assert owner_update_notification.level == "INFO"
    assert owner_update_notification.title == "Projet modifié"

    member_update_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == member.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert member_update_notification is not None
    assert member_update_notification.level == "INFO"
    assert member_update_notification.title == "Projet modifié"

    # ==========================================================
    # 5. REMOVE MEMBER
    # ==========================================================

    remove_member_response = client.delete(
        f"/projects/{project_id}/members/{member.id}",
        headers=owner_headers,
    )

    assert remove_member_response.status_code == 204

    removed_member_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == member.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert removed_member_notification is not None
    assert removed_member_notification.level == "INFO"
    assert removed_member_notification.title == "Removed from Project"

    # ==========================================================
    # 6. DELETE PROJECT
    # ==========================================================

    delete_response = client.delete(
        f"/projects/{project_id}",
        headers=owner_headers,
    )

    assert delete_response.status_code == 204

    deleted_project_notification = (
        db_session.query(Notification)
        .filter(
            Notification.user_id == owner.id,
            Notification.type == "PROJECT",
            Notification.entity_type == "project",
            Notification.entity_id == project_id,
        )
        .order_by(Notification.id.desc())
        .first()
    )

    assert deleted_project_notification is not None
    assert deleted_project_notification.level == "WARNING"
    assert deleted_project_notification.title == "Projet supprimé"