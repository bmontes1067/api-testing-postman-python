# 🔌 API Testing — Postman & Python

![API Tests](https://github.com/bmontes1067/api-testing-postman-python/actions/workflows/api-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?logo=pytest&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?logo=postman&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

API test suite for the [JSONPlaceholder](https://jsonplaceholder.typicode.com) REST API using two complementary approaches: **Python + pytest** for code-based automation and **Postman** for exploratory and contract testing. Both run in CI via GitHub Actions.

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Test Coverage](#-test-coverage)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Design Decisions](#-design-decisions)
- [What I Learned](#-what-i-learned)

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [Python 3.11+](https://python.org) | Test language |
| [pytest](https://pytest.org) | Test runner & assertions |
| [requests](https://requests.readthedocs.io) | HTTP client |
| [Pydantic v2](https://docs.pydantic.dev) | Schema / contract validation |
| [pytest-html](https://pytest-html.readthedocs.io) | HTML test reports |
| [Postman](https://postman.com) | Collection-based API testing |
| [Newman](https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/) | Postman CLI runner for CI |

---

## 📁 Project Structure

```
api-testing-postman-python/
├── .github/
│   └── workflows/
│       └── api-tests.yml      # CI: pytest (py3.11+3.12) + Newman
├── postman/
│   └── jsonplaceholder_collection.json   # Exportable Postman collection
├── schemas/
│   └── post_schema.py         # Pydantic models for contract validation
├── tests/
│   ├── test_posts.py          # GET, POST, PUT, PATCH, DELETE + negatives
│   ├── test_users.py          # Users + nested resources
│   ├── test_comments.py       # Comments + headers + response time
│   └── test_todos.py          # Todos + filtering + parametrize
├── conftest.py                # Shared fixtures (session, base_url, payloads)
├── pytest.ini                 # pytest config + HTML report
├── requirements.txt
└── .env                       # BASE_URL and thresholds (not committed)
```

---

## ✅ Test Coverage

| Endpoint | Tests | Methods | Schema | Negative |
|----------|-------|---------|--------|----------|
| `/posts` | 18 | GET, POST, PUT, PATCH, DELETE | ✅ | ✅ |
| `/users` | 7 | GET | ✅ | ✅ |
| `/comments` | 8 | GET, POST | ✅ | ✅ |
| `/todos` | 7 | GET | ✅ | — |
| **Total** | **40** | | | |

Every test suite validates:
- ✅ Status codes
- ✅ Response time under threshold
- ✅ JSON schema / contract via Pydantic
- ✅ Content-Type headers
- ✅ Negative cases (404, invalid IDs)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ (only to run the Postman collection with Newman)

### Installation

```bash
git clone https://github.com/bmontes1067/api-testing-postman-python.git
cd api-testing-postman-python
```

**Create and activate a virtual environment** (recommended, especially on Mac with Homebrew):

```bash
python3 -m venv venv
source venv/bin/activate    # Mac / Linux
# venv\Scripts\activate     # Windows
```

You will see `(venv)` at the beginning of the prompt — this indicates that it is active.

```bash
pip install -r requirements.txt
```

To deactivate the virtual environment when you are finished:

```bash
deactivate
```

> The next time you open a terminal, remember to activate the environment before running tests:
> ```bash
> source venv/bin/activate
> ```

### Environment variables

The project includes a `.env` with default values ready to use:

```env
BASE_URL=https://jsonplaceholder.typicode.com
RESPONSE_TIME_THRESHOLD_MS=2000
```

---

## ▶️ Running Tests

### Python / pytest

```bash
# Run all tests
pytest

# Run a specific file
pytest tests/test_posts.py

# Run with verbose output
pytest -v

# Run only negative cases
pytest -m negative
```

The HTML report is generated automatically at `reports/report.html`.

### Postman / Newman

Import `postman/jsonplaceholder_collection.json` directly into Postman, or run via CLI:

```bash
# Install Newman
npm install -g newman

# Run the collection
newman run postman/jsonplaceholder_collection.json \
  --env-var "base_url=https://jsonplaceholder.typicode.com"

# Run with HTML report
npm install -g newman-reporter-htmlextra
newman run postman/jsonplaceholder_collection.json \
  --env-var "base_url=https://jsonplaceholder.typicode.com" \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/newman-report.html
```

---

## ⚙️ CI/CD Pipeline

Two parallel jobs run on every push and PR:

```
push / PR / nightly cron
        ↓
┌──────────────────┐   ┌──────────────────┐
│  pytest          │   │  Newman          │
│  Python 3.11     │   │  Postman         │
│  Python 3.12     │   │  collection      │
└────────┬─────────┘   └────────┬─────────┘
         ↓                      ↓
   HTML report             HTML report
   (artifact)              (artifact)
```

---

## 🧠 Design Decisions

**Why both pytest and Postman?**
They serve different purposes. Postman excels at exploratory testing, quick contract checks, and sharing with non-developers. pytest is better for data-driven tests, reusable fixtures, CI integration and complex assertions. Having both shows versatility.

**Why Pydantic for schema validation?**
Pydantic v2 gives typed, readable schema definitions. If the API contract changes, the test fails clearly pointing to the field that broke — much cleaner than raw `assert "field" in response`.

**Why a shared `requests.Session` fixture?**
Sessions reuse TCP connections and share headers, making the suite faster and avoiding repeated header setup. The `scope="session"` fixture ensures one session for the entire test run.

**Why `pytest.mark.parametrize` on some tests?**
Parametrized tests run the same logic against multiple inputs with minimal code. It's the right tool for boundary testing and equivalent partition cases.

---

## 📚 What I Learned

- How to design a layered API test suite separating fixtures, schemas and tests
- The difference between contract testing (Pydantic) and functional testing (assertions)
- How to measure and assert response time thresholds programmatically
- Running Postman collections headlessly with Newman in CI
- The complementary value of code-based and collection-based API testing

---

## 📄 License

MIT © [Belén Montes](https://github.com/bmontes1067)
