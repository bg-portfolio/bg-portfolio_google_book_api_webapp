import json


def test_book_create_record(client):
    isbn_13 = 123
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": None, "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}

    response = client.post("/api/create-record", json.dumps(data))
    print(response.json())
    assert response.status_code == 200 or 202
    assert response.json()["success"] == True
    assert response.json()["created_id"] == isbn_13


def test_book_get_record_1(client):
    isbn_13 = 123
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": None, "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}
    response = client.post("/api/create-record", json.dumps(data))

    response = client.get(f"/api/get-record-by-isbn/{isbn_13}")
    print(response.json())
    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "test_title"
    assert response.json()["author"] == None
