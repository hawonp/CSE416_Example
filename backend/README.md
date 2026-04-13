

## Tools Used

**General Tools**
| Tools  | Package |
| ------------- | ------------- |
| Package Management  | [uv](https://docs.astral.sh/uv/)  |
| Backend  | [FastAPI](https://fastapi.tiangolo.com/#create-it)  |
| Table Management | [Alembic](https://alembic.sqlalchemy.org/en/latest/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| DTO | [Pydantic](https://pydantic.dev/docs/) |

**Python Syntax**
| Python Tools | Package |
| ------------- | ------------- |
| Type Checking | [ty](https://docs.astral.sh/ty/) |
| Linter / Formatter | [Ruff](https://docs.astral.sh/ruff/) |

## Commands
- Install uv via curl
    `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Install uv via homebrew
    `brew install uv`
- Init a new project
    `uv init`
- Auto generate virtual environment
    `uv run main.py`
- Install packages
    `uv add "fastapi[standard]" alembic SQLAlchemy`

### Using ty
- Install ty (tool)
    `uvx ty`
- Run type checking
    `uvx ty check`

### Using Ruff
- Install ruff (tool)
    `uvx ruff`
- run linting/formatting
    `uvx ruff check`

### Using alembic
- Init alembic
    `uv run alembic init alembic`

### Using pre-commit
- Init pre-commit
    `uv run precommit init`
- Create a file called `.pre-commit-config.yaml`
- Install git hooks
    `pre-commit install`