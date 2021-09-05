What could have been better?:

- frontend?
- use of databases package for asyncpg -> async postgres database
- not lazy sql schema
- forgotten about HTTP status codes
- publish_date is a string with different date formats/filtering by date, from-to, doesn't work properly...
- add more json validation for google book api, thumbnail especially. (for ex. harry potter)
- filtering db queries do not provide a way of distinguishing between small and big letters
- could use settings.py for all env vars like db etc.
- not every book uses isbn, 13, precisely as an identifier, there are many other formats, in fact it would be better to change into string in db and validate outside pydantic. Would need to allow all weird identifiers like stringhere:number