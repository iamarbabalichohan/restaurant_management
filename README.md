install python deps
```
uv sync
```
migrate db
```
alembic upgrade head
```
```
uv run uvicorn app.main:app --reload
```