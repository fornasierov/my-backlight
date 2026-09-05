## Repository

https://github.com/vrgb-dev/my-backlight

## Get started

For a fresh system, run the following in order:

```fish
# 1) Install the project prerequisites
make install-poetry
make create-env

# 2) Activate the project environment
conda activate my-backlight

# 3) Install the Python package and create the user config
make setup

# 4) Install the udev rule and device group
make install-system

# 5) Open a new shell with the device group active
make activate-group
# inside the new shell
conda activate my-backlight

# 6) Verify the device access and project setup
make doctor

# 7) Run the app
make run ARGS="brightness 30"
```

`make create-env` creates the `my-backlight` Conda environment with Python 3.12.
`make install-poetry` installs Poetry if it is missing. `make setup` assumes the
`my-backlight` Conda environment is already active and installs the project with
Poetry and creates the user configuration without overwriting an existing file.
`make install-system` requires `sudo` because it installs the udev rule and
creates the device-access group. The `activate-group` target opens a subshell
with that group active immediately; use `exit` to return to the original shell.
Logging out and back in applies the group permanently to new shells.

## Run arguments

Use `make run ARGS="..."` to pass a command to the CLI. The project accepts the
following patterns:

```fish
# brightness and power states
make run ARGS="brightness 30"
make run ARGS="brightness 80"
make run ARGS="off"
make run ARGS="restore"

# color by name
make run ARGS="set red"
make run ARGS="set orange"
make run ARGS="set yellow"
make run ARGS="set green"
make run ARGS="set blue"
make run ARGS="set purple"
make run ARGS="set pink"
make run ARGS="set brown"
make run ARGS="set black"
make run ARGS="set grey"
make run ARGS="set white"

# color by hex value
make run ARGS="set ff8800"
make run ARGS="set 00ff88"

# brightness with a color
make run ARGS="set red 45"
make run ARGS="set blue 80"
```

Common form:

- `brightness <percent>` sets the backlight level
- `set <color> [percent]` applies a named or hex color and optional brightness
- `off` turns the backlight off
- `restore` restores the last saved state

Supported named colors are: `red`, `orange`, `yellow`, `green`, `blue`,
`purple`, `pink`, `brown`, `black`, `grey`, and `white`. Existing `RRGGBB`
values remain supported.

To troubleshoot an existing installation:

```fish
make audit-udev
make check-access
make doctor
```

To initialize only the user configuration:

```fish
make config-init
```

The default color accepts these names: `red`, `orange`, `yellow`, `green`,
`blue`, `purple`, `pink`, `brown`, `black`, `grey`, and `white`. Existing
`RRGGBB` values remain supported.

Development checks:

```fish
make test
make lint
```

To preview or remove all installed my-backlight artifacts:

```fish
DRY_RUN=1 make purge
make purge
```

The purge command requires typing `REMOVE` and does not delete this source
repository or the Conda environment.
