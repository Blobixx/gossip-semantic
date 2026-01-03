In production, the app runs with a non-superuser role linkup_user.

Database migrations and pgvector extension creation run under a separate migrator role.

For local dev, I containerized PostgreSQL with pgvector so everything works with one command.

### Requirements

This project runs on docker so first, you do not already have it, install docker on your machine.

### Create database

Execute the following commands in `backend/` folder

```
cd backend/

make build

make restore
```

NB : `make restore` should only be run once to load dump into database

### Start the api

```
cd backend/

make api
```

### Start the frontend

In another terminal, go to `frontend/` folder and create `.env` file. Add the following line to the file

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The still in `frontend/` folder, install packages

```
yarn install
```

Then start frontend and start search for articles !

```
yarn dev
```

You can then access website on `http://localhost:5173/`

### Run scrapping scripts

The scrappers script allow to retrieve articles from public.fr and vsd.fr.

It uses open source project Scrapy (https://www.scrapy.org/)

It then populaites de "articles" table from "linkup" database.

```
scrapy crawl public_sitemap
```

```
scrapy crawl vsd_sitemap
```

Then to fill the `embeddings` column, run

```
./scripts/compute_embeddings.py
```

### Run tests

```
docker compose up tests
```

### Future possible improvements

- Dataset

Currently around 4K articles with year range between 2016 and 2026. There is no particular strategy of year representation.

- Add CI

  To be production-ready, needs a CI to run tests, linters, etc.

- Frontend

  - Design

    Very basic now

  - User experience

    Add a "see more" option for long articles

    Tests

- Backend

  - Paginated output instead of fixes number of articles

  - Multiple embedding per articles => per chunk of content
