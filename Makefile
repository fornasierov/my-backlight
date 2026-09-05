.PHONY: install-dev-suite install-udev uninstall-udev audit-udev check-access run purge

install-dev-suite:
	@echo "Installing Poetry 2.4.1..."
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.4.1 python3 -
	@echo "Poetry 2.4.1 installed successfully!"
	@echo "Installing development dependencies (ruff 0.16.6, pytest 9.1.1)..."
	poetry add --group dev ruff==0.16.6 pytest==9.1.1
	@echo "Development dependencies installed successfully!"

install-udev:
	./scripts/install-udev.sh

uninstall-udev:
	./scripts/uninstall-udev.sh

audit-udev:
	./scripts/audit-udev.sh

check-access:
	./scripts/check-access.sh

run:
	poetry run my-backlight $(ARGS)

purge:
	./scripts/purge-my-backlight.sh