import sys

DEBUG = False

COLOR_MAP = {
    "red": "ff0000",
    "orange": "ff8000",
    "yellow": "ffff00",
    "green": "00ff00",
    "blue": "0000ff",
    "purple": "aa00ff",
    "pink": "ff69b4",
    "brown": "a52a2a",
    "black": "000000",
    "grey": "808080",
    "white": "ffffff",
}


def debug(msg: str) -> None:
    if DEBUG:
        print(f"[debug] {msg}")


def die(msg: str, exit_code=1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(exit_code)


def clamp(n: int, lo: int, hi: int):
    return max(lo, min(hi, n))


def resolve_color(color: str) -> str:
    normalized = color.strip().lower()
    if normalized in COLOR_MAP:
        return COLOR_MAP[normalized]

    normalized = normalized.replace("#", "")
    if len(normalized) == 6:
        try:
            int(normalized, 16)
        except ValueError:
            pass
        else:
            return normalized

    choices = ", ".join(COLOR_MAP)
    raise ValueError(f"Color must be a name ({choices}) or RRGGBB")


def percent_to_intensity(p):
    p = clamp(int(p), 0, 100)
    return round(p * 255 / 100)


def hex_to_rgb(hexstr):
    try:
        hexstr = resolve_color(hexstr)
    except ValueError as error:
        die(str(error))

    r = int(hexstr[0:2], 16)
    g = int(hexstr[2:4], 16)
    b = int(hexstr[4:6], 16)

    return r, g, b
