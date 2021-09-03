run-db:
	docker run --name google_book_postgres -p 5432:5432 -e POSTGRES_PASSWORD=password \
	-e POSTGRES_DB=google_book_api -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres

run-test-db:
	docker run --name test_google_book_postgres -p 5432:5432 -e POSTGRES_PASSWORD=password \
	-e POSTGRES_DB=test_google_book_api -v ${PWD}/tests/db_data:/var/lib/postgresql/data -d postgres