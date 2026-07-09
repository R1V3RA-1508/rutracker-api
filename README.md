# Rutracker API

Unofficial Rutracker API based on parsing

----

### Stack: 
- fastapi
- pydantic
- httpx
- bs4

---

### TODO:
  - [x] Topic fetching

  - [ ] Search

  - [ ] Login


----

### Dev launching:
```bash
uv sync
uv run uvicorn api.app:app --port 8000 --reload
```

----

### Login model:
  1. Sending POST rutracker.org/forum/login.php
  2. Fetching bb_session cookie from response
  3. Fetching captcha if needed


