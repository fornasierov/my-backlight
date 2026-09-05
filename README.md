## Repository

https://github.com/vrgb-dev/my-backlight

## Usage

For a fresh checkout:

```fish
conda activate my-backlight
make setup
make install-system
make activate-group
# inside the new shell
conda activate my-backlight
make doctor
make run ARGS="brightness 30"
```

`make setup` installs the Poetry environment and creates the user configuration
without overwriting an existing file. `make install-system` requires `sudo`
because it installs the udev rule and creates the device-access group. The
`activate-group` target opens a subshell with that group active immediately;
use `exit` to return to the original shell. Logging out and back in applies the
group permanently to new shells.

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
