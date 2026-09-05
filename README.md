## Repository

https://github.com/vrgb-dev/my-backlight

## Usage

```fish
conda activate my-backlight
poetry install --with dev
make install-udev
make audit-udev
make check-access
make run ARGS="brightness 30"
```

To preview or remove all installed my-backlight artifacts:

```fish
DRY_RUN=1 make purge
make purge
```

The purge command requires typing `REMOVE` and does not delete this source
repository or the Conda environment.
