.DEFAULT_GOAL := help

PREFIX ?= /usr/local
LIBEXECDIR ?= $(PREFIX)/libexec
CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2

.PHONY: help build install install-udev uninstall doctor activate-group test run

help:
	@echo "mkb commands:"
	@echo "  make build          Build the HID helper"
	@echo "  make install        Install mkb and the udev rule"
	@echo "  make activate-group Use the device group in a new shell now"
	@echo "  make doctor         Check local setup and device access"
	@echo "  make run ARGS=...   Run mkb"
	@echo "  make test           Run checks"
	@echo "  make uninstall      Remove installed artifacts (destructive)"

build:
	@mkdir -p build
	$(CC) $(CFLAGS) src/mkb-hid.c -o build/mkb-hid

install: build
	sudo install -Dm755 bin/mkb $(PREFIX)/bin/mkb
	sudo install -Dm755 build/mkb-hid $(LIBEXECDIR)/mkb-hid
	$(MAKE) install-udev
	@echo "Installed mkb and mkb-hid."

install-udev:
	./scripts/install-udev.sh

uninstall:
	./scripts/purge-my-backlight.sh

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
