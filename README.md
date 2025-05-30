# Yell

**Yell** is a stylized developer console logger that gives you expressive, themed, and introspective output—perfect for complex projects where clarity and traceability matter.

Yell captures where a message came from, how many times a function has fired, and wraps output in a customizable color and formatting theme. It’s built to be modular, extensible, and fun to use.

---

## 🔧 Installation

Clone or install via pip (packaging support coming soon):

```bash
pip install yell-dev-console  # once packaged
```

Or drop it directly into your project:

```bash
project/
  └── yell/
        ├── Yell.py
        ├── YellCaller.py
        ├── ColorText.py
        ├── AnsiColors.py
        ├── Theme.py
        └── ColorTools.py
```

---

## 🚀 Quick Start

```python
from yell import yell

def my_func():
    yell("This is a message")
    yell.success("Operation succeeded")
    yell.error("Something went wrong")

my_func()
```

Output is formatted with styled borders, stack trace info, and theming.

---

## 🪄 Features

* Colorful, labeled log messages (`info`, `debug`, `success`, `error`, etc.)
* Output includes:

  * File name and function
  * Call count
  * Indented trace path
* Custom class-color mapping (see config)
* Configurable quiet mode, width, theme toggle
* Smart wrapping that preserves ANSI formatting

---

## ⚙️ Configuration

Yell will look for a file named `yell_config.py` in your working directory. Here’s an example:

```python
config = {
    "use_theme": True,
    "all_quiet": False,
    "width": 120,
    "custom_class_a": MyType,
    "custom_color_a": "bright_magenta",
    "modules": {
        "my_script": {"lvl": 3, "on": True},
        "utils": {"lvl": 2, "on": True},
    }
}
```

This will automatically register module-level YellCallers with levels and switches.

---

## 🧪 Testing

Yell is designed for testability. Core components separate formatting from side effects. To test output, redirect `stdout` or use `StringIO` mocks.

---

## 📦 Packaging Notes

This package is nearly PyPI-ready. Remaining steps:

* Add a `pyproject.toml` or `setup.py`
* Add `__version__` to `__init__.py`
* Include this `README.md`, a `LICENSE`, and optionally examples/tests

---

## 🧠 Philosophy

Yell emerged organically while working on a Notion-backed memory engine, and it reflects a desire for transparent debugging without sacrificing style or flow. The stack awareness and visual traceability turn logging into a narrative tool, not just a diagnostic one.

---

## 🔗 License

MIT (or your choice)
