from src.models import BookEntry, GoogleBookRequest
import httpx


async def get_google_books(google_query: GoogleBookRequest) -> list:
    get_string = "+".join([f"{key}:{query}" for key,
                           query in google_query.__dict__.items() if query != ""])  # this populates get_string with data from pydantic model
    # replaces spaces, getting rid of 'req' the searching phrase attr from pydantic model
    get_string = get_string[4:].replace(" ", "%20")
    url = f'https://www.googleapis.com/books/v1/volumes?q={get_string}'

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.get(url)
        resp.raise_for_status()

        data = resp.json()
        book_list = []

        if data["totalItems"] == 0:
            return []

        for item in data["items"]:
            # check for proper isbn/there are different standards, not always isbn_13 is available, but the var name remain
            try:
                isbn_13 = item["volumeInfo"]["industryIdentifiers"][1]["identifier"]
            except:
                isbn_13 = item["volumeInfo"]["industryIdentifiers"][0]["identifier"]
            if not isbn_13.isnumeric():
                isbn_13 = "".join(
                    letter for letter in isbn_13 if letter.isnumeric())

            try:
                book = BookEntry(
                    isbn_13=isbn_13,
                    title=item["volumeInfo"]["title"],
                    publish_date=item["volumeInfo"]["publishedDate"],
                    author=item["volumeInfo"]["authors"],
                    page_count=item["volumeInfo"]["pageCount"],
                    thumbnail_url=item["volumeInfo"]["imageLinks"]["thumbnail"],
                    language=item["volumeInfo"]["language"]
                )
                book_list.append(book)
            except (ValueError, KeyError) as e:
                print(e)
        return book_list
