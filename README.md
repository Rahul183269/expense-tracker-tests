# Expense Tracker API Tests

A small expense tracker REST API built with FastAPI, with an automated test suite written in pytest.

I built this project to practice the core QA/SDET loop: understand the feature, write the test, run it, read the failure, fix it, commit.

## Tech used

- Python
- FastAPI (the API)
- pytest (the tests)
- Git and GitHub

## How to run

Create and activate a virtual environment, then install the tools:

```
python -m venv venv
venv\Scripts\activate
python -m pip install fastapi uvicorn pytest httpx
```

Start the API:

```
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints in the browser.

Run the tests:

```
python -m pytest -v
```

## API endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | /health | Checks the app is alive |
| POST | /expenses | Creates an expense |
| GET | /expenses | Lists all expenses |
| GET | /expenses/{id} | Gets one expense (404 if missing) |
| PUT | /expenses/{id} | Updates an expense (404 if missing) |
| DELETE | /expenses/{id} | Deletes an expense (404 if missing) |
| DELETE | /reset | Clears all data (used by tests only) |

## What I tested

- Health check
- Create, read, update and delete (CRUD)
- Not-found cases (404) for get, update and delete
- Invalid input (422), using one parametrized test with 8 bad payloads:
  empty title, negative amount, zero amount, empty category, wrong type for category,
  missing title, missing amount, text instead of a number
- ID uniqueness after a delete
- Clean test data for every test, using a pytest fixture

## Bug log

### Bug 1: Invalid data was accepted

- **What happened:** the API accepted an empty title, an empty category, and zero or negative amounts, and returned 201.
- **How I found it:** I wrote tests for bad input first and watched them fail.
- **Fix:** added validation rules in the `ExpenseIn` model (`min_length=1` for text, `gt=0` for amount).

### Bug 2: Duplicate IDs after a delete

- **What happened:** I created two expenses (ids 1 and 2), deleted the first, then created a third. The third also got id 2, because the id was calculated as `len(expenses) + 1`.
- **How I found it:** a test that follows the sequence create, create, delete, create (`test_ids_are_unique_after_delete`). It failed with `assert 2 == 3`.
- **Fix:** replaced the length-based id with a counter (`next_id`) that only goes up, and made `/reset` restart the counter.

## What I learned

- **Fixtures:** a fixture in `conftest.py` gives every test a clean start. Without it, tests share data and can fail depending on the order they run in.
- **Parametrize:** one test function can run many inputs, so adding a new bad-input case is one new line.
- **Test first:** writing a test and seeing it fail proves the test can catch the bug.
- **Reading failures:** the line after `>` shows where it crashed, and the last `E` line names the error.

## Next steps

- Replace the in-memory list with a SQLite database
- Add tests that check the data directly in the database
- Add Selenium and Playwright UI tests (Project 2)
- Add Docker and a GitHub Actions pipeline