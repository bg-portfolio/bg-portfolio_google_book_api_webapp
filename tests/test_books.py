import json
import pytest

# I could have used fixtures with test data to not copy the code, I could.
# each data is valid in scope of a function


@pytest.mark.xfail
def test_fail(client):
    # this is expected to fail, testing failure
    pass


@pytest.mark.skip
def test_skip(client):
    # this is expected to skip, testing skip
    pass


def test_pass(client):
    # this is expected to pass, testing pass
    assert True


def test_connection_to_pages(client):
    response = client.get("/")
    # we are testing api routes, it's expected to not connect to pages.
    assert response.status_code == 404


def test_nonexistent_api_route(client):
    response = client.get("/not-a-route")

    assert response.status_code == 404


def test_method_not_allowed(client):
    response = client.put("/get-record-by-isbn/1")

    assert response.json()["detail"] == 'Method Not Allowed'

    response = client.put("/get-all-records")

    assert response.json()["detail"] == 'Method Not Allowed'

    response = client.post("/delete-record-by-isbn/1")

    assert response.json()["detail"] == "Method Not Allowed"

    # and so on and on


def test_book_create_record_1(client):
    # possitive
    isbn_13 = 123
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": None, "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}

    response = client.post(
        "/create-record", json.dumps(data))

    assert response.status_code == 200 or 202
    assert response.json()["success"] == True
    assert response.json()["created_id"] == isbn_13

    # duplicate record
    response = client.post(
        "/create-record", json.dumps(data))

    assert response.status_code == 200 or 202
    assert response.json()["success"] == False
    assert response.json()[
        "info"] == f"isbn {isbn_13} already exists"

    # negative
    isbn_13 = "abc"
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": None, "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}

    response = client.post(
        "/create-record", json.dumps(data))

    assert response.status_code == 200 or 202
    assert response.json()[
        "detail"][0]["msg"] == 'value is not a valid integer'


def test_book_get_record_by_isbn_1(client):
    # possitive
    isbn_13 = 124
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}
    response = client.post("/create-record", json.dumps(data))

    response = client.get(f"/get-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "test_title"
    assert response.json()["author"] == ["Bob"]

    # negative
    response = client.get(f"/get-record-by-isbn/{isbn_13}5")

    assert response.status_code == 200 or 202
    assert response.json()["success"] == False
    assert response.json()["info"] == f"isbn {isbn_13}5 do not exists"


def test_book_get_all_records_1(client):
    isbn_13 = 125
    data = [{"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
             "language": "testing_lang"}, {"isbn_13": isbn_13+1, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}, {"isbn_13": isbn_13+2, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}]
    for record in data:
        response = client.post("/create-record", json.dumps(record))

    response = client.get(f"/get-all-records")

    assert response.status_code == 200 or 202
    assert len(response.json()) == len(data)
    assert response.json()[0]["isbn_13"] == isbn_13


def test_book_update_record_1(client):
    # possitive
    isbn_13 = 126
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}
    response = client.post("/create-record", json.dumps(data))

    response = client.get(f"/get-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "test_title"
    assert response.json()["author"] == ["Bob"]

    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": ["Bob", "Another Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}

    response = client.put("/update-record", json.dumps(data))

    assert response.status_code == 200 or 202
    assert response.json()["success"] == True
    assert response.json()["created_id"] == f"{isbn_13}"

    response = client.get(f"/get-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "test_title"
    assert response.json()["author"] == ["Bob", "Another Bob"]

    # negative
    # no isbn
    data = {"title": "test_title", "publish_date": "1234",
            "author": ["Bob", "Another Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}

    response = client.put("/update-record", json.dumps(data))

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_delete_record_by_isbn_1(client):
    isbn_13 = 127
    data = {"isbn_13": isbn_13, "title": "test_title", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}
    response = client.post("/create-record", json.dumps(data))

    response = client.get(f"/get-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "test_title"
    assert response.json()["author"] == ["Bob"]

    # possitive
    response = client.delete(f"/delete-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["success"] == True
    assert response.json()["deleted_id"] == isbn_13

    # negative
    response = client.delete(f"/delete-record-by-isbn/{isbn_13}")

    assert response.json()["success"] == False
    assert response.json()["info"] == f"isbn {isbn_13} do not exists"


def test_get_all_records_by_query_params_1(client):
    isbn_13 = 128
    data = [{"isbn_13": isbn_13, "title": "book", "publish_date": "1234",
            "author": ["Bob"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
             "language": "not lang"}, {"isbn_13": isbn_13+1, "title": "test_title", "publish_date": "1234",
            "author": ["Arthur"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "testing_lang"}, {"isbn_13": isbn_13+2, "title": "not test", "publish_date": "1234",
            "author": ["Anna"], "page_count": 123, "thumbnail_url": "testing_thumbnail.com",
            "language": "eng"}]
    for record in data:
        response = client.post("/create-record", json.dumps(record))

    response = client.get(f"/get-record-by-isbn/{isbn_13}")

    assert response.status_code == 200 or 202
    assert response.json()["isbn_13"] == isbn_13
    assert response.json()["title"] == "book"
    assert response.json()["author"] == ["Bob"]

    # test title
    response = client.get(
        "/get-all-records-by-query-params?title=test_title")

    assert response.status_code == 200 or 202
    assert response.json()[0]["isbn_13"] == isbn_13+1
    assert response.json()[0]["title"] == "test_title"
    assert response.json()[0]["author"] == ["Arthur"]

    # test author
    response = client.get("/get-all-records-by-query-params?author=Bob")

    assert response.status_code == 200 or 202
    assert response.json()[0]["isbn_13"] == isbn_13
    assert response.json()[0]["title"] == "book"
    assert response.json()[0]["author"] == ["Bob"]

    # test language
    response = client.get(
        "/get-all-records-by-query-params?language=testing_lang")

    assert response.status_code == 200 or 202
    assert response.json()[0]["isbn_13"] == isbn_13+1
    assert response.json()[0]["title"] == "test_title"
    assert response.json()[0]["language"] == "testing_lang"

    # negative
    # will return all books, as there are no filters
    response = client.get(
        "/get-all-records-by-query-params")

    assert response.status_code == 200 or 202
    assert len(response.json()) == 3
