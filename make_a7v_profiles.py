#!/usr/bin/env python3
"""
make_a7v_profiles.py
====================
Generates Sony A7V (ILCE-7M5) Camera Matching DCP profiles by transplanting
the correct colour matrices from the A7V's Adobe Standard profile into each of
the 11 Sony RX1R III (DSC-RX1RM3) Camera Matching profiles.

Profiles are written to ./output/Sony ILCE-7M5/ relative to this script so
that no elevated (sudo) permissions are needed.  After inspection, copy them
to the system CameraRaw folder with the command printed at the end.

Profile naming
--------------
Files and internal ProfileName tags get " (A7V)" appended, e.g.:
  "Sony ILCE-7M5 Camera ST (A7V).dcp"   ProfileName = "Camera ST (A7V)"

This means they appear as *separate* entries in Lightroom's Profile Browser
(under Camera Matching) alongside any future native Sony / Adobe profiles for
the A7V — they do NOT override anything.

No third-party libraries required — stdlib only (struct, pathlib).

macOS paths used
-----------------
  Donor profiles : /Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony DSC-RX1RM3/
  Colour source  : /Library/Application Support/Adobe/CameraRaw/CameraProfiles/Adobe Standard/Sony ILCE-7M5 Adobe Standard.dcp
  System output  : /Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5/
  Local output   : <script_dir>/output/Sony ILCE-7M5/   (written by default)

DCP / TIFF tag reference
-------------------------
  ProfileName           0x4746  (18246)  ASCII
  UniqueCameraModel     0xC614  (50708)  ASCII
  LocalizedCameraModel  0xC615  (50709)  ASCII (optional)
  ColorMatrix1          0xC621  (50721)  SRATIONAL
  ColorMatrix2          0xC622  (50722)  SRATIONAL
  ForwardMatrix1        0xC714  (51988)  SRATIONAL
  ForwardMatrix2        0xC715  (51989)  SRATIONAL
  LookTable             0xC725  (52005)  FLOAT  – left untouched
  ToneCurve             0xC6FC  (50940)  FLOAT  – left untouched

SRATIONAL = (int32 numerator, int32 denominator), 8 bytes per element.
A 3x3 matrix is 9 consecutive SRATIONAL values = 72 bytes in the data block.
"""

import struct
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()

BASE = Path("/Library/Application Support/Adobe/CameraRaw/CameraProfiles")
DONOR_DIR  = BASE / "Camera" / "Sony DSC-RX1RM3"
ADOBE_STD  = BASE / "Adobe Standard" / "Sony ILCE-7M5 Adobe Standard.dcp"
SYSTEM_OUTPUT_DIR = BASE / "Camera" / "Sony ILCE-7M5"

# Local output – no sudo required
LOCAL_OUTPUT_DIR = SCRIPT_DIR / "output" / "Sony ILCE-7M5"

# ---------------------------------------------------------------------------
# Profile variant suffix (appended to filename stem and ProfileName tag)
# ---------------------------------------------------------------------------
VARIANT_SUFFIX = " (A7V)"

# ---------------------------------------------------------------------------
# ForwardMatrix: ProPhoto RGB -> XYZ D50  (canonical pass-through)
# ---------------------------------------------------------------------------
FORWARD_MATRIX = [
    0.7976749, 0.1351917, 0.0313534,
    0.2880402, 0.7118741, 0.0000857,
    0.0000000, 0.0000000, 0.8252100,
]

# ---------------------------------------------------------------------------
# TIFF / DCP tag IDs
# ---------------------------------------------------------------------------
TAG_UNIQUE_CAMERA_MODEL    = 0xC614
TAG_LOCALIZED_CAMERA_MODEL = 0xC615
TAG_PROFILE_NAME           = 0x4746
TAG_COLOR_MATRIX_1         = 0xC621
TAG_COLOR_MATRIX_2         = 0xC622
TAG_FORWARD_MATRIX_1       = 0xC714
TAG_FORWARD_MATRIX_2       = 0xC715

TIFF_ASCII     = 2
TIFF_SRATIONAL = 10

# ---------------------------------------------------------------------------
# TIFF helpers
# ---------------------------------------------------------------------------

def _endian(data: bytes) -> str:
    bom = data[:2]
    if bom == b"II":
        return "<"
    if bom == b"MM":
        return ">"
    raise ValueError(f"Not a TIFF file: magic={bom!r}")


def _type_size(typ: int) -> int:
    sizes = {1:1, 2:1, 3:2, 4:4, 5:8, 6:1, 7:1, 8:2, 9:4, 10:8, 11:4, 12:8}
    return sizes.get(typ, 1)


def _read_value_bytes(data: bytes, typ: int, count: int, voff: int, endian: str) -> bytes:
    total = _type_size(typ) * count
    if total <= 4:
        raw4 = struct.pack(endian + "I", voff)
        return raw4[:total]
    return data[voff: voff + total]


def _read_ascii(data: bytes, typ: int, count: int, voff: int, endian: str) -> str:
    raw = _read_value_bytes(data, typ, count, voff, endian)
    return raw.rstrip(b"\x00").decode("latin-1")


def _read_srational_matrix(data: bytes, count: int, voff: int, endian: str) -> list:
    vals = []
    for i in range(count):
        num, den = struct.unpack_from(endian + "ii", data, voff + i * 8)
        vals.append(num / den if den != 0 else 0.0)
    return vals


def _read_ifd(data: bytes, ifd_offset: int, endian: str) -> list:
    n = struct.unpack_from(endian + "H", data, ifd_offset)[0]
    entries = []
    pos = ifd_offset + 2
    for _ in range(n):
        tag, typ, count, voff = struct.unpack_from(endian + "HHII", data, pos)
        entries.append((tag, typ, count, voff, pos))
        pos += 12
    return entries


# ---------------------------------------------------------------------------
# Extract ColorMatrix1/2 from the A7V Adobe Standard DCP
# ---------------------------------------------------------------------------

def extract_color_matrices(path: Path) -> dict:
    data = path.read_bytes()
    endian = _endian(data)
    ifd_off = struct.unpack_from(endian + "I", data, 4)[0]
    entries = _read_ifd(data, ifd_off, endian)
    result = {}
    for (tag, typ, count, voff, _pos) in entries:
        if tag in (TAG_COLOR_MATRIX_1, TAG_COLOR_MATRIX_2):
            result[tag] = _read_srational_matrix(data, count, voff, endian)
    missing = {TAG_COLOR_MATRIX_1, TAG_COLOR_MATRIX_2} - result.keys()
    if missing:
        raise RuntimeError(
            f"Tags not found in A7V Adobe Standard: {[hex(t) for t in missing]}")
    return result


# ---------------------------------------------------------------------------
# Encode helpers
# ---------------------------------------------------------------------------

def _encode_srational_matrix(matrix: list, endian: str) -> bytes:
    DEN = 10_000_000
    buf = bytearray()
    for v in matrix:
        num = round(v * DEN)
        buf += struct.pack(endian + "ii", num, DEN)
    return bytes(buf)


# ---------------------------------------------------------------------------
# DCP patch engine
# ---------------------------------------------------------------------------

def patch_dcp(src: Path, dst: Path, new_model: str,
              color_matrices: dict, forward_matrix: list,
              variant_suffix: str) -> None:
    """
    Copy src -> dst with the following patches:

    ASCII tag patches:
      - UniqueCameraModel / LocalizedCameraModel:
          'DSC-RX1RM3' replaced with new_model  (no suffix)
      - ProfileName:
          'DSC-RX1RM3' replaced with new_model AND variant_suffix appended

    Matrix patches (in-place SRATIONAL replacement, same byte count):
      - ColorMatrix1 / ColorMatrix2  <- color_matrices
      - ForwardMatrix1 / ForwardMatrix2  <- forward_matrix

    Untouched: LookTable, ToneCurve, and everything else.
    """
    data = bytearray(src.read_bytes())
    endian = _endian(bytes(data))
    ifd_off = struct.unpack_from(endian + "I", data, 4)[0]
    entries = _read_ifd(bytes(data), ifd_off, endian)

    OLD = "DSC-RX1RM3"

    for (tag, typ, count, voff, pos) in entries:
        total_bytes = _type_size(typ) * count
        inline = total_bytes <= 4

        # ---- ASCII string patches ----------------------------------------
        if tag in (TAG_UNIQUE_CAMERA_MODEL,
                   TAG_LOCALIZED_CAMERA_MODEL,
                   TAG_PROFILE_NAME) and typ == TIFF_ASCII:

            old_str = _read_ascii(bytes(data), typ, count, voff, endian)

            if OLD in old_str:
                new_str = old_str.replace(OLD, new_model)
            elif tag == TAG_PROFILE_NAME:
                new_str = old_str  # will still append variant suffix below
            else:
                continue  # nothing to change

            if tag == TAG_PROFILE_NAME:
                new_str = new_str + variant_suffix

            new_bytes = new_str.encode("latin-1") + b"\x00"
            new_count = len(new_bytes)

            if new_count <= 4 and inline:
                padded = new_bytes.ljust(4, b"\x00")
                data[pos + 8: pos + 12] = padded[:4]
                struct.pack_into(endian + "I", data, pos + 4, new_count)
            else:
                new_offset = len(data)
                data += new_bytes
                struct.pack_into(endian + "I", data, pos + 4, new_count)
                struct.pack_into(endian + "I", data, pos + 8, new_offset)

        # ---- ColorMatrix patches -----------------------------------------
        elif tag in (TAG_COLOR_MATRIX_1, TAG_COLOR_MATRIX_2) and typ == TIFF_SRATIONAL:
            new_raw = _encode_srational_matrix(color_matrices[tag], endian)
            if len(new_raw) != total_bytes:
                raise RuntimeError(
                    f"ColorMatrix size mismatch for {hex(tag)}: "
                    f"expected {total_bytes}, got {len(new_raw)}")
            data[voff: voff + total_bytes] = new_raw

        # ---- ForwardMatrix patches ----------------------------------------
        elif tag in (TAG_FORWARD_MATRIX_1, TAG_FORWARD_MATRIX_2) and typ == TIFF_SRATIONAL:
            new_raw = _encode_srational_matrix(forward_matrix, endian)
            if len(new_raw) != total_bytes:
                raise RuntimeError(
                    f"ForwardMatrix size mismatch for {hex(tag)}: "
                    f"expected {total_bytes}, got {len(new_raw)}")
            data[voff: voff + total_bytes] = new_raw

    dst.write_bytes(bytes(data))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 62)
    print("Sony A7V (ILCE-7M5) DCP Profile Generator")
    print("=" * 62)

    if not DONOR_DIR.is_dir():
        sys.exit(f"\nERROR: Donor directory not found:\n  {DONOR_DIR}")
    if not ADOBE_STD.is_file():
        sys.exit(f"\nERROR: A7V Adobe Standard DCP not found:\n  {ADOBE_STD}")

    donor_files = sorted(DONOR_DIR.glob("*.dcp"))
    if not donor_files:
        sys.exit(f"\nERROR: No .dcp files found in {DONOR_DIR}")
    if len(donor_files) != 11:
        print(f"WARNING: Expected 11 donor profiles, found {len(donor_files)}")

    print(f"\nReading ColorMatrix values from:\n  {ADOBE_STD}")
    color_matrices = extract_color_matrices(ADOBE_STD)
    for tag, vals in color_matrices.items():
        label = "ColorMatrix1" if tag == TAG_COLOR_MATRIX_1 else "ColorMatrix2"
        print(f"  {label} ({hex(tag)}): [{', '.join(f'{v:.6f}' for v in vals)}]")

    print(f"\nForwardMatrix (ProPhoto RGB -> XYZ D50):")
    print(f"  [{', '.join(f'{v:.7f}' for v in FORWARD_MATRIX)}]")
    print(f"\nVariant suffix appended to ProfileName: '{VARIANT_SUFFIX}'")

    LOCAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nLocal output directory:\n  {LOCAL_OUTPUT_DIR}\n")

    success = 0
    for src in donor_files:
        # Filename: DSC-RX1RM3 -> ILCE-7M5, append variant suffix before .dcp
        stem = src.stem.replace("DSC-RX1RM3", "ILCE-7M5")
        new_name = stem + VARIANT_SUFFIX + ".dcp"
        dst = LOCAL_OUTPUT_DIR / new_name
        try:
            patch_dcp(src, dst, "ILCE-7M5", color_matrices, FORWARD_MATRIX,
                      VARIANT_SUFFIX)
            print(f"  OK  {src.name}")
            print(f"   -> {new_name}")
            success += 1
        except Exception as e:
            print(f"  FAIL {src.name}: {e}")

    print(f"\n{'=' * 62}")
    print(f"Done: {success}/{len(donor_files)} profiles written to:")
    print(f"  {LOCAL_OUTPUT_DIR}")

    print(f"\n--- To install system-wide (requires your password) ---")
    print(f"Run in Terminal:\n")
    print(f'  sudo mkdir -p "{SYSTEM_OUTPUT_DIR}"')
    print(f'  sudo cp "{LOCAL_OUTPUT_DIR}"/*.dcp "{SYSTEM_OUTPUT_DIR}/"')
    print(f'  sudo chown root:wheel "{SYSTEM_OUTPUT_DIR}"/*.dcp')
    print(f'  sudo chmod 644 "{SYSTEM_OUTPUT_DIR}"/*.dcp')

    print(f"\n--- Lightroom Classic import ---")
    print(f"  1. Open an ILCE-7M5 raw file in Develop.")
    print(f"  2. Click the Profile box (top of Basic panel) -> Browse...")
    print(f"  3. Hamburger menu (=) -> Import Profiles.")
    print(f"  4. Navigate to:\n       {LOCAL_OUTPUT_DIR}")
    print(f"  5. Select all 11 .dcp files -> Import.")
    print(f"  6. Profiles appear under Camera Matching as e.g. 'Camera ST (A7V)'.")
    print(f"{'=' * 62}")


if __name__ == "__main__":
    main()
