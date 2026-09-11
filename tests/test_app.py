from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]

    client.delete(f"/activities/{activity_name}/participants?email={email}")


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]

    # restore state for later tests
    client.post(f"/activities/{activity_name}/signup?email={email}")
