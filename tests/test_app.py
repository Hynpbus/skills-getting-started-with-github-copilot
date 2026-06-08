from urllib.parse import quote

from src import app as app_module


def test_get_activities(client):
    # Arrange
    expected_keys = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for key in expected_keys:
        assert key in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module.activities[activity]["participants"]


def test_signup_duplicate_student(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_missing_activity(client):
    # Arrange
    encoded_activity = quote("Nonexistent Club", safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in app_module.activities[activity]["participants"]


def test_remove_missing_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
