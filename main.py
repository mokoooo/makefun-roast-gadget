"""Write a single fixed one-line roast to entry.txt.

The line is written to ``entry.txt`` inside the directory named by the
``MAKEFUN_OUTPUT_DIR`` environment variable (``/output`` by default).
The write is atomic: the content goes to a temporary sibling file first
and is then renamed into place, so readers never see a partial file.
"""

import os
import sys

LINE = "My authenticator app gives me a code that expires in 30 seconds, then takes 31 seconds to open."


def main() -> int:
    content = LINE + "\n"

    if not 1 <= len(LINE) <= 200:
        print("error: line must be 1 to 200 characters long", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("error: line must not be blank", file=sys.stderr)
        return 1

    output_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)

    target = os.path.join(output_dir, "entry.txt")
    tmp = os.path.join(output_dir, ".entry.txt.tmp.%d" % os.getpid())
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
