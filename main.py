"""Copy the front-page image to the output directory.

This program is the entrypoint for the make.fun news-image-20261121
bounty. It takes the pre-rendered newspaper front page (entry.png, in the
same directory as this script) and writes an exact copy to
<output>/entry.png, where <output> is the MAKEFUN_OUTPUT_DIR environment
variable when set, or /output otherwise.

The copy is byte-for-byte and deterministic: the same input always
produces the same output, so repeated runs write identical files.

Standard library only; no network access.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def source_path() -> Path:
    """Return the path of the image shipped beside this script."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def destination_path() -> Path:
    """Return the output path, honouring MAKEFUN_OUTPUT_DIR."""
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return output_dir / IMAGE_NAME


def sha256_of(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_image(source: Path, destination: Path) -> None:
    """Copy the image byte-for-byte and verify the copy matches."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

    if sha256_of(source) != sha256_of(destination):
        raise ValueError("copy mismatch: output differs from source")


def main() -> int:
    source = source_path()
    destination = destination_path()

    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 1

    try:
        copy_image(source, destination)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"wrote {destination} ({destination.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
