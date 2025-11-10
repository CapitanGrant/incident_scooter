import pytest

INCIDENT_CASES = [
    {"description": "вышел из строя аккумулятор", "source": "operator"},
    {"description": "поставили на стоянку", "source": "monitoring"},
    {"description": "пригласили друга", "source": "partner"},
    {"description": "ошибка 302", "source": "system"},
]


@pytest.mark.parametrize("payload", INCIDENT_CASES)
def test_create_incident(client, payload):
    response = client.post("/incidents/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == payload["description"]
    assert data["source"] == payload["source"]


@pytest.mark.parametrize("status",
                         ["in_progress", "resolved", "closed", "rejected"])
def test_update_incident(client, create_param_incident, status):
    incident = create_param_incident
    incident_id = incident["id"]
    response = client.patch(f'/incidents/{incident_id}', json={"status": status})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident["id"]
    assert data["status"] == status


def test_get_incidents(client, create_param_incident):
    """"Тест на получение всех инцидентов"""
    incident = create_param_incident
    response = client.get('/incidents/all_records')
    assert response.status_code == 200


@pytest.mark.parametrize("status",
                         ["new", "in_progress", "resolved", "resolved", "rejected"])
def test_get_incidents_by_status(client, create_param_incident, status):
    """"Тест на получение инцидентов по фильтрам"""
    incident = create_param_incident
    response = client.get(f'/incidents/all_records/?status={status}')
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == status for item in data)


def test_create_incident_invalid_data(client):
    response = client.post("/incidents/create", json={"source": "operator"})
    assert response.status_code == 422
