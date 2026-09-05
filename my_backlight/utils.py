import sys

DEBUG = False


def debug(msg: str) -> None:
    if DEBUG:
        print(f"[debug] {msg}")


def die(msg: str, exit_code=1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(exit_code)


def clamp(n: int, lo: int, hi: int):
    return max(lo, min(hi, n))


def percent_to_intensity(p):
    p = clamp(int(p), 0, 100)
    return round(p * 255 / 100)


def hex_to_rgb(hexstr):
    hexstr = hexstr.strip().lower().replace("#", "")
    if len(hexstr) != 6:
        die("Color must be RRGGBB")

    try:
        r = int(hexstr[0:2], 16)
        g = int(hexstr[2:4], 16)
        b = int(hexstr[4:6], 16)
    except ValueError:
        die("Invalid hex color")

    return r, g, b
