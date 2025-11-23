# Contributing to FinTerm

First off, thank you for considering contributing to FinTerm! It's people like you that make FinTerm such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, terminal emulator)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (PEP 8)
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Setup

1. **Fork and clone the repo**
   ```bash
   git clone https://github.com/your-username/finterm.git
   cd finterm
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Style Guidelines

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use 4 spaces for indentation (not tabs)
* Maximum line length is 100 characters
* Use descriptive variable names
* Add docstrings to all functions and classes

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add candlestick chart widget

- Implement candlestick rendering using plotext
- Add support for multiple timeframes
- Update dashboard to include chart widget

Fixes #123
```

### Documentation Style Guide

* Use [Markdown](https://guides.github.com/features/mastering-markdown/)
* Reference function/class names in backticks: `ClassName`
* Include code examples where appropriate

## Project Structure

```
finterm/
├── src/
│   ├── app.py              # Main application entry point
│   ├── widgets/            # Widget components
│   ├── data/               # Data fetching modules
│   └── utils/              # Utility functions
├── tests/                  # Test files (coming soon)
├── docs/                   # Documentation (coming soon)
└── examples/               # Example configurations (coming soon)
```

## Adding a New Widget

To add a new widget to FinTerm:

1. **Create the widget file** in `src/widgets/your_widget.py`

2. **Extend BaseWidget**
   ```python
   from .base import BaseWidget
   from rich.console import RenderableType

   class YourWidget(BaseWidget):
       async def fetch_data(self):
           # Fetch your data
           pass

       def render_content(self) -> RenderableType:
           # Render your widget
           pass
   ```

3. **Add to widgets/__init__.py**
   ```python
   from .your_widget import YourWidget

   __all__ = [..., "YourWidget"]
   ```

4. **Update the app** to include your widget in the dashboard

5. **Add tests** for your widget

6. **Update documentation**

## Testing

We use pytest for testing. Run tests with:

```bash
pytest
```

For coverage:
```bash
pytest --cov=src tests/
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
