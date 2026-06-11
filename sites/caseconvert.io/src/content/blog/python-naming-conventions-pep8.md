---
title: "Python Naming Conventions: The Complete PEP 8 Guide"
description: "Full PEP 8 naming guide: snake_case for variables and functions, CapWords for classes, UPPER_SNAKE for constants, and the underscore conventions for private members."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["python", "pep8", "naming conventions", "snake case", "programming style"]
draft: false
heroImage: "/images/blog/python-naming-conventions-pep8-hero.png"
---

Python's naming conventions are defined by [PEP 8](https://peps.python.org/pep-0008/), the official Python style guide authored by Guido van Rossum and maintained by the Python core team. Following PEP 8 is not enforced by the Python interpreter — your code will run either way — but it is the universal community standard, expected in open-source projects, code reviews, and professional Python teams.

This guide covers every naming rule in PEP 8 with practical code examples for each.

## Variables and functions: snake_case

Variables and function names use **snake_case**: all lowercase, words separated by underscores.

```python
# Variables
user_id = 42
first_name = "Alice"
is_authenticated = False
max_retry_count = 3
account_balance = 1500.00

# Functions
def get_user_by_id(user_id: int):
    pass

def send_welcome_email(email_address: str, user_name: str) -> bool:
    pass

def calculate_monthly_interest(principal: float, rate: float) -> float:
    return principal * rate / 12
```

For more context on snake_case and why Python chose it, see [*What Is snake_case?*](/blog/what-is-snake-case).

Function names should be verb phrases: `get_`, `create_`, `update_`, `delete_`, `validate_`, `calculate_`, `send_`. Avoid vague names like `data()` or `process()`.

## Classes: CapWords (PascalCase)

Class names use **CapWords**, also called **PascalCase**: the first letter of each word is capitalized, with no separators.

```python
# Classes
class UserAccount:
    pass

class DatabaseConnection:
    pass

class HttpRequestHandler:
    pass

class ShoppingCartItem:
    pass

# Exception classes follow the same convention
# and conventionally end in "Error" or "Exception"
class ValidationError(Exception):
    pass

class DatabaseConnectionError(RuntimeError):
    pass

class InsufficientFundsError(ValueError):
    pass
```

PEP 8 notes that if a callable (a class used as a factory function) is documented primarily as a function, the function naming convention (lowercase) may be used instead. The `collections.namedtuple` factory is a well-known example of this deliberate exception.

## Constants: UPPER_SNAKE_CASE

Module-level constants use **UPPER_SNAKE_CASE**: all uppercase letters with underscores between words.

```python
# Constants — defined at module level
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com/v1"
DATABASE_URL = "postgresql://localhost/mydb"
SECRET_KEY = "change-me-in-production"

# Configuration-style constants
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DEBUG = False
LOG_LEVEL = "INFO"
```

Python's UPPER_SNAKE convention is a signal, not a technical guarantee. Unlike JavaScript's `const`, Python doesn't prevent reassignment of an uppercase name. By convention, other developers know not to reassign it.

## Modules and packages: short lowercase

Module (`.py` file) names should be **short, all-lowercase**, and avoid underscores where possible. When a module name needs word separation, underscores are acceptable but not preferred.

```
# Good module names
utils.py
models.py
views.py
auth.py
db.py

# Acceptable (underscores when needed for clarity)
user_utils.py
email_helpers.py

# Avoid
UserUtils.py        # Don't use CamelCase for modules
emailHelpers.py     # Don't use camelCase for modules
```

Package (directory) names follow the same rule: short and lowercase. Underscores are explicitly discouraged in package names (though the interpreter allows them).

```
# Good package names
mypackage/
utils/
auth/

# Avoid
my_package/         # underscores discouraged
MyPackage/          # no CamelCase
```

## Private and internal naming conventions

Python uses underscore prefixes as visibility conventions, since there are no access modifiers like `private` or `protected`.

### Single leading underscore: `_internal`

A single leading underscore signals that the name is intended for internal use. It's a hint to other developers, not a technical restriction.

```python
class UserService:
    def get_user(self, user_id: int):
        return self._fetch_from_db(user_id)

    def _fetch_from_db(self, user_id: int):
        # Internal implementation detail — not part of the public API
        pass

# Module-level: won't be exported by "from module import *"
_internal_cache = {}

def _normalize_email(email: str) -> str:
    return email.strip().lower()
```

When you do `from mymodule import *`, names with a leading underscore are excluded from the import. This makes `_` a lightweight encapsulation tool.

### Double leading underscore: `__name_mangling`

A double leading underscore on a class attribute triggers **name mangling**: Python renames `__attr` to `_ClassName__attr` at the bytecode level. This prevents accidental override in subclasses.

```python
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance    # stored as _BankAccount__balance

    def deposit(self, amount: float):
        self.__balance += amount

    def get_balance(self) -> float:
        return self.__balance

class SavingsAccount(BankAccount):
    def __init__(self, balance: float, interest_rate: float):
        super().__init__(balance)
        self.__balance = 0   # stored as _SavingsAccount__balance — does NOT override parent

# Name mangling in action
account = BankAccount(100.0)
# account.__balance → AttributeError
# account._BankAccount__balance → 100.0 (accessible but discouraged)
```

Use `__double_leading` sparingly — only when you genuinely need to protect against subclass name clashes.

### Dunder (magic) methods: `__name__`

Names surrounded by double underscores on both sides are **dunder** methods (short for "double underscore"). These are Python's special method protocol:

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
```

**Never invent your own `__dunder__` names.** The double-underscore namespace is reserved for Python's future use. If you need a custom magic-like protocol, use `_single_underscore` instead.

### Single trailing underscore: `name_`

When a name you want to use conflicts with a Python keyword, add a trailing underscore:

```python
# 'class', 'type', 'lambda', 'id', 'list' are keywords or built-ins
class UserForm:
    def __init__(self, class_: str, type_: str, id_: int):
        self.class_ = class_
        self.type_ = type_
        self.id_ = id_
```

## Type variable names

Type variable names in generic type hints use **CapWords** (PascalCase), typically kept short:

```python
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
UserT = TypeVar("UserT")
ResponseT = TypeVar("ResponseT")

def first_item(items: list[T]) -> T:
    return items[0]

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

Covariant type variables conventionally end in `_co`; contravariant ones end in `_contra`:

```python
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
```

## Avoid ambiguous single-letter names

PEP 8 explicitly forbids these single-letter variable names in certain contexts because they are visually ambiguous in some fonts:

- `l` (lowercase L) — looks like `1` (digit one)
- `O` (uppercase O) — looks like `0` (digit zero)
- `I` (uppercase I) — looks like `l` (lowercase L) or `1`

```python
# These names are forbidden by PEP 8 in ambiguous contexts
l = 1      # Is this 1 (one) or l (ell)?
O = 0      # Is this 0 (zero) or O (oh)?
I = 1      # Is this 1 (one) or I (eye)?

# Use descriptive names or unambiguous alternatives
line_count = 1
offset = 0
index = 1
```

For loop variables that truly are throwaway, `i`, `j`, `k` are acceptable. The rule targets variable *definitions* where the name persists and needs to be read back.

## Complete PEP 8 naming summary

| Identifier type | Convention | Example |
|----------------|------------|---------|
| Variable | snake_case | `user_id`, `is_active` |
| Function | snake_case | `get_user_by_id()` |
| Method | snake_case | `self.calculate_total()` |
| Class | CapWords (PascalCase) | `UserAccount` |
| Exception | CapWords + Error/Exception | `ValidationError` |
| Module | short lowercase | `utils.py`, `models.py` |
| Package | short lowercase | `auth/`, `db/` |
| Constant | UPPER_SNAKE_CASE | `MAX_CONNECTIONS` |
| Internal/private | `_single_leading` | `_fetch_from_db()` |
| Name-mangled | `__double_leading` | `__balance` |
| Dunder/magic | `__name__` | `__init__`, `__repr__` |
| Keyword conflict | `trailing_` | `class_`, `type_` |
| Type variable | CapWords (short) | `T`, `UserT` |

## Enforcing PEP 8 automatically

Manual compliance is error-prone. The standard toolchain for PEP 8 enforcement:

- **flake8** — linter that checks style violations including naming
- **pylint** — more comprehensive linter with naming convention checks
- **black** — opinionated auto-formatter (doesn't rename identifiers, but formats everything else)
- **ruff** — fast Rust-based linter/formatter that replaces flake8 + isort + many plugins

A typical project setup in `pyproject.toml`:

```toml
[tool.ruff]
select = ["E", "F", "N"]  # pycodestyle, pyflakes, naming conventions
line-length = 88

[tool.black]
line-length = 88
target-version = ["py311"]
```

## Convert Python identifiers between styles

If you're working on a project that interfaces with a JavaScript frontend or a REST API that uses camelCase keys, you'll need to convert between snake_case and camelCase. The [caseconvert.io](/) converter handles all major naming conventions — paste a block of Python identifiers and get the camelCase equivalents instantly.
