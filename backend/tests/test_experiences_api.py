def test_create_experience_api(client):
    """Test POST /api/v1/experiences creates a personal experience."""
    response = client.post(
        "/api/v1/experiences",
        json={
            "title": "Moving to France for College",
            "description": "Navigated visa process, language barrier, and university setup.",
            "takeaway": "Discomfort is the fastest catalyst for rapid growth.",
            "category": "Personal"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Moving to France for College"
    assert data["takeaway"] == "Discomfort is the fastest catalyst for rapid growth."
    assert data["category"] == "Personal"
    assert data["id"] is not None


def test_create_experience_validation_error(client):
    """Test experience creation rejects empty title."""
    response = client.post(
        "/api/v1/experiences",
        json={"title": "   "}
    )
    assert response.status_code == 400


def test_list_experiences_and_category_filter_api(client):
    """Test GET /api/v1/experiences filters by category."""
    client.post("/api/v1/experiences", json={"title": "Hackathon Win", "category": "Technical"})
    client.post("/api/v1/experiences", json={"title": "Building KnowFin", "category": "Technical"})
    client.post("/api/v1/experiences", json={"title": "College Choice", "category": "Personal"})

    response = client.get("/api/v1/experiences?category=Technical")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    titles = [item["title"] for item in data["items"]]
    assert "Hackathon Win" in titles
    assert "Building KnowFin" in titles


def test_update_experience_api(client):
    """Test PATCH /api/v1/experiences/{exp_id} updates experience details."""
    create_res = client.post(
        "/api/v1/experiences",
        json={"title": "Early Freelancing Lessons", "category": "Career"}
    )
    exp_id = create_res.json()["id"]

    update_res = client.patch(
        f"/api/v1/experiences/{exp_id}",
        json={"takeaway": "Never underprice high-impact technical work."}
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["takeaway"] == "Never underprice high-impact technical work."


def test_delete_experience_api(client):
    """Test DELETE /api/v1/experiences/{exp_id} removes experience."""
    create_res = client.post("/api/v1/experiences", json={"title": "Temporary mistake"})
    exp_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/experiences/{exp_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/v1/experiences/{exp_id}")
    assert get_res.status_code == 404
