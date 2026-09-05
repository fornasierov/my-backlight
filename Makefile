.PHONY: install-dev-suite

install-dev-suite:
	@echo "Installing Poetry 2.4.1..."
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.4.1 python3 -
	@echo "Poetry 2.4.1 installed successfully!"
	@echo "Installing development dependencies (ruff 0.16.6, pytest 9.1.1)..."
	poetry add --group dev ruff==0.16.6 pytest==9.1.1
	@echo "Development dependencies installed successfully!"