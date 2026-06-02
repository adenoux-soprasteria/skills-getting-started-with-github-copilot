import pytest


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_after = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_after[activity_name]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_requires_email_query_param(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


@pytest.mark.strict_contract
@pytest.mark.xfail(reason="Backend currently does not validate email format")
def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


@pytest.mark.strict_contract
@pytest.mark.xfail(reason="Backend currently allows blank or whitespace emails")
def test_signup_rejects_blank_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "   "

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


@pytest.mark.strict_contract
@pytest.mark.xfail(reason="Backend currently does not enforce max_participants")
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"

    # Fill capacity: starts at 2 participants, max is 12.
    for i in range(10):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"capacity-{i}@mergington.edu"},
        )

    # Act
    overflow_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    # Assert
    assert overflow_response.status_code == 409
