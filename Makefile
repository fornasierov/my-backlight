.DEFAULT_GOAL := help

.PHONY: help setup config-init install-dev-suite install-system install-udev \
	uninstall-udev audit-udev check-access doctor activate-group test lint run purge

help:
	@echo "my-backlight commands:"
	@echo "  make setup          Install Python dependencies and initialize config"
	@echo "  make install-system Install the udev rule and device group"
	@echo "  make activate-group Use the device group in a new shell now"
	@echo "  make doctor         Check local setup and device access"
	@echo "  make run ARGS=...   Run my-backlight"
	@echo "  make test           Run tests"
	@echo "  make lint           Run Ruff checks"
	@echo "  make purge          Remove installed artifacts (destructive)"

setup:
	@command -v poetry >/dev/null || { echo "Error: Poetry is not installed." >&2; exit 1; }
	poetry install --with dev
	$(MAKE) config-init
	@echo "Setup complete. Run 'make install-system' for device access."

config-init:
	./scripts/init-config.sh

install-dev-suite:
	@echo "Installing Poetry 2.4.1..."
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.4.1 python3 -
	@echo "Poetry 2.4.1 installed successfully!"
	@echo "Installing project and development dependencies..."
	poetry install --with dev
	@echo "Development dependencies installed successfully!"

install-system: install-udev

install-udev:
	./scripts/install-udev.sh

uninstall-udev:
	./scripts/uninstall-udev.sh

audit-udev:
	./scripts/audit-udev.sh

check-access:
	./scripts/check-access.sh

doctor:
	./scripts/doctor.sh

activate-group:
	@echo "Starting a shell with the 'my-backlight' group active."
	@echo "After it starts, run 'conda activate my-backlight'."
	@echo "Run 'exit' to return to the original shell."
	newgrp my-backlight

test:
	poetry run pytest

lint:
	poetry run ruff check .

run:
	@if test -z "$(ARGS)"; then echo "Usage: make run ARGS=\"brightness 30\""; exit 2; fi
	@if test -n "$${CONDA_DEFAULT_ENV:-}" && test "$${CONDA_DEFAULT_ENV}" != "my-backlight"; then \
		echo "Error: the active Conda environment is '$${CONDA_DEFAULT_ENV}'." >&2; \
		echo "Run 'conda activate my-backlight' and try again." >&2; \
		exit 1; \
	fi
	@if test ! -f "$${MY_BACKLIGHT_CONFIG_DIR:-$$HOME/.config/my-backlight}/config.yaml"; then \
		echo "Error: user configuration is missing." >&2; \
		echo "Run 'make config-init' first." >&2; \
		exit 1; \
	fi
	poetry run my-backlight $(ARGS)

purge:
	./scripts/purge-my-backlight.sh