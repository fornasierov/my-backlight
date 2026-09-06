.DEFAULT_GOAL := help

PREFIX ?= /usr/local
LIBEXECDIR ?= $(PREFIX)/libexec
CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2

.PHONY: help build install install-system install-udev uninstall uninstall-udev \
	audit-udev check-access doctor activate-group test run purge

help:
	@echo "mkb commands:"
	@echo "  make build          Build the HID helper"
	@echo "  make install        Install mkb and the udev rule"
	@echo "  make install-system Install only the udev rule and device group"
	@echo "  make activate-group Use the device group in a new shell now"
	@echo "  make doctor         Check local setup and device access"
	@echo "  make run ARGS=...   Run mkb"
	@echo "  make test           Run checks"
	@echo "  make purge          Remove installed artifacts (destructive)"

build:
	@mkdir -p build
	$(CC) $(CFLAGS) src/mkb-hid.c -o build/mkb-hid

install: build
	sudo install -Dm755 bin/mkb $(PREFIX)/bin/mkb
	sudo install -Dm755 build/mkb-hid $(LIBEXECDIR)/mkb-hid
	$(MAKE) install-udev
	@echo "Installed mkb and mkb-hid."

uninstall:
	sudo rm -f $(PREFIX)/bin/mkb $(LIBEXECDIR)/mkb-hid
	$(MAKE) uninstall-udev

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
	@echo "Run 'exit' to return to the original shell."
	newgrp my-backlight

test: build
	bash -n bin/mkb scripts/*.sh
	build/mkb-hid >/dev/null 2>&1; test $$? -eq 1

run:
	@if test -z "$(ARGS)"; then echo "Usage: make run ARGS=\"brightness 30\""; exit 2; fi
	bin/mkb $(ARGS)

purge:
	./scripts/purge-my-backlight.sh