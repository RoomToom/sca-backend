def test_create_cat_and_mission_and_freeze_notes(client):
    # створюємо кота
    cat_payload = {
        "name": "Tom",
        "years_experience": 3,
        "breed": "Abyssinian",
        "salary": 1000
    }
    r = client.post("/api/v1/cats", json=cat_payload)
    assert r.status_code == 201, r.text
    cat = r.json()
    cat_id = cat["id"]

    # створюємо місію з 1 таргетом + одразу призначаємо кота
    mission_payload = {
        "targets": [{"name": "T1", "country": "US", "notes": "hello"}],
        "assigned_cat_id": cat_id
    }
    r = client.post("/api/v1/missions", json=mission_payload)
    assert r.status_code == 201, r.text
    mission = r.json()
    assert mission["assigned_cat_id"] == cat_id
    assert len(mission["targets"]) == 1
    target_id = mission["targets"][0]["id"]
    mission_id = mission["id"]

    # оновлюємо нотатки ДО complete (має бути 200)
    r = client.patch(f"/api/v1/targets/{target_id}/notes", json={"notes": "updated"})
    assert r.status_code == 200, r.text

    # завершуємо таргет
    r = client.patch(f"/api/v1/targets/{target_id}/complete")
    assert r.status_code == 200, r.text

    # перевіряємо що місія стала complete
    r = client.get(f"/api/v1/missions/{mission_id}")
    assert r.status_code == 200, r.text
    assert r.json()["is_complete"] is True

    # пробуємо ще раз оновити нотатки — тепер має бути 400 (заморожені)
    r = client.patch(f"/api/v1/targets/{target_id}/notes", json={"notes": "should fail"})
    assert r.status_code == 400, r.text


def test_cannot_delete_assigned_mission(client):
    # кіт
    r = client.post("/api/v1/cats", json={
        "name": "Jerry",
        "years_experience": 2,
        "breed": "Abyssinian",
        "salary": 800
    })
    assert r.status_code == 201
    cat_id = r.json()["id"]

    # місія, одразу з таргетом і асайном
    r = client.post("/api/v1/missions", json={
        "targets": [{"name": "T2", "country": "DE"}],
        "assigned_cat_id": cat_id
    })
    assert r.status_code == 201
    mission_id = r.json()["id"]

    # пробуємо видалити — має дати 400
    r = client.delete(f"/api/v1/missions/{mission_id}")
    assert r.status_code == 400, r.text
