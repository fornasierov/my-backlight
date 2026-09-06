# mkb

`mkb` controls the keyboard backlight color and brightness on the supported
ASUS HID device. It uses a Bash command and a small native HID helper; Python,
Poetry, and Conda are not required.

## Install

```fish
make build
make install
make activate-group
```

The install step builds and installs `mkb`, installs the HID helper, and
installs the udev rule. Start a new login session, or use `make activate-group`,
after the udev installation so the device group is active.

Check the setup with:

```fish
make doctor
```

## Use

```fish
mkb set purple
mkb set ff8800 45
mkb brightness 30
mkb off
mkb restore
mkb status
```

Named colors include `red`, `orange`, `yellow`, `green`, `blue`, `purple`,
`pink`, `brown`, `black`, `grey`, and `white`. Six-digit `RRGGBB` values are
also accepted.

The current color and brightness are stored in `~/.config/mkb/state`.

## Development

```fish
make build
make test
make run ARGS="set blue 80"
```

Use `make doctor` when diagnosing the installation or device permissions.

To remove installed files and the udev setup:

```fish
DRY_RUN=1 make uninstall
make uninstall
```
