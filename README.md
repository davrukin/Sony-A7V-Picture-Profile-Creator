# Sony A7V Camera Matching DCP Profiles

[![License: MIT (script only)](https://img.shields.io/badge/License-MIT_(script_only)-blue.svg)](LICENSE)

Camera Matching colour profiles for the **Sony A7V (ILCE-7M5)** in Adobe
Lightroom Classic, derived from the Sony RX1R III (DSC-RX1RM3) donor profiles.

## Licence

The **Python script and documentation** in this repository are released under
the [MIT Licence](LICENSE).

> [!IMPORTANT]
> The MIT Licence covers **only the original source code** (`make_a7v_profiles.py`
> and associated documentation). It does **not** extend to the generated `.dcp`
> files, which are derived from Adobe-distributed profile data. See the
> [⚠️ Legal Disclaimer](#️-legal-disclaimer) below for usage restrictions on
> those files.

---

## Attribution

This project is based on the community workaround described in:

> **["A guide to making your own A7V Camera Matching profiles for Lightroom"](https://www.reddit.com/r/SonyAlpha/comments/1tk5uag/a_guide_to_making_your_own_a7v_camera_matching/)**
> — u/cequl on r/SonyAlpha (May 2026)

That post itself builds on an earlier technique shared by u/Reptiles_SHH.
All credit for the underlying methodology goes to those community members.

---

## ⚠️ Legal Disclaimer

> [!CAUTION]
> **Read before using or distributing these files.**

The generated `.dcp` files are derived, in part, from DCP profile files that
are distributed by Adobe Systems as part of Adobe Camera Raw and Lightroom
Classic. Adobe has not explicitly granted permission to redistribute modified
versions of these files. The author of the original Reddit guide noted caution
on this point, and that caution is echoed here.

**By using this script and the profiles it generates, you acknowledge:**

1. **Personal use only.** The generated profiles are intended solely for your
   own personal, non-commercial use on cameras you own.
2. **No redistribution.** Do not share, upload, or otherwise redistribute the
   generated `.dcp` files. Point others to this script instead so they generate
   their own copies from their own locally-installed Adobe software.
3. **No warranty.** The profiles are provided as-is. They may produce
   inaccurate colour results and are not a substitute for an official Adobe
   profile for the A7V.
4. **Licence compliance.** Your use of the script is subject to the licence
   terms of your Adobe software. Review the [Adobe General Terms of Use](https://www.adobe.com/legal/terms.html)
   and the Camera Raw / Lightroom licence if in doubt.
5. **This is not legal advice.** If you have specific concerns about IP or
   copyright, consult a qualified legal professional.

---

## What's here

| Path | Description |
|------|-------------|
| `make_a7v_profiles.py` | Generator script (stdlib-only, no pip required) |
| `output/Sony ILCE-7M5/` | 11 ready-to-import `.dcp` files |
| `README.md` | This document |
| `LICENSE` | MIT licence (applies to the script source only — see below) |

### Profiles generated

| Filename | Creative Look | Abbreviation |
|----------|---------------|:---:|
| `Sony ILCE-7M5 Camera BW (A7V).dcp` | Black & White | BW |
| `Sony ILCE-7M5 Camera FL (A7V).dcp` | Film | FL |
| `Sony ILCE-7M5 Camera FL2 (A7V).dcp` | Film 2 | FL2 |
| `Sony ILCE-7M5 Camera FL3 (A7V).dcp` | Film 3 | FL3 |
| `Sony ILCE-7M5 Camera IN (A7V).dcp` | Instant | IN |
| `Sony ILCE-7M5 Camera NT (A7V).dcp` | Neutral | NT |
| `Sony ILCE-7M5 Camera PT (A7V).dcp` | Portrait | PT |
| `Sony ILCE-7M5 Camera SH (A7V).dcp` | Soft Highkey | SH |
| `Sony ILCE-7M5 Camera ST (A7V).dcp` | Standard | ST |
| `Sony ILCE-7M5 Camera VV (A7V).dcp` | Vivid | VV |
| `Sony ILCE-7M5 Camera VV2 (A7V).dcp` | Vivid 2 | VV2 |

The `(A7V)` suffix means these profiles coexist with any future native Adobe
profiles for the A7V — they do **not** override anything.

---

## How to run the script

> **Requirements**: Python 3.8+ (pre-installed on macOS; available from
> [python.org](https://python.org) on Windows). No third-party packages.

**macOS / Linux**

```bash
cd /path/to/PhotoProfiles
python3 make_a7v_profiles.py
```

**Windows**

```powershell
cd C:\path\to\PhotoProfiles
python make_a7v_profiles.py
```

> The script auto-detects the OS and uses the correct system paths (see
> [Paths reference](#paths-reference) below). Profiles are written to
> `./output/Sony ILCE-7M5/` relative to the script.

---

## How to install (system-wide)

### macOS

Open Terminal and run:

```bash
sudo mkdir -p "/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5"

sudo cp "./output/Sony ILCE-7M5"/*.dcp \
        "/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5/"

sudo chown root:wheel \
        "/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5"/*.dcp

sudo chmod 644 \
        "/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5"/*.dcp
```

Alternatively, copy them via Finder (requires Finder authentication).

### Windows

Open **PowerShell as Administrator** and run:

```powershell
$dest = "C:\ProgramData\Adobe\CameraRaw\CameraProfiles\Camera\Sony ILCE-7M5"
New-Item -ItemType Directory -Force -Path $dest
Copy-Item ".\output\Sony ILCE-7M5\*.dcp" -Destination $dest
```

Or copy the files with File Explorer — navigate to
`C:\ProgramData\Adobe\CameraRaw\CameraProfiles\Camera\`, create a
`Sony ILCE-7M5` folder, and paste the `.dcp` files in (administrator
confirmation required).

---

## How to import into Lightroom Classic

You can install via the **system folder** (above) or the **Lightroom import
dialog** — choose one.

**Import dialog method (no admin rights needed):**

1. Open Lightroom Classic with an **ILCE-7M5** raw file selected.
2. Switch to the **Develop** module.
3. In the **Basic** panel, click the **Profile** box → **Browse…**
4. In the Profile Browser, click the hamburger menu **(☰)** → **Import Profiles…**
5. Navigate to the `output/Sony ILCE-7M5/` folder inside this project.
6. Select all 11 `.dcp` files → **Review** → **Import**.
7. The profiles appear under **Camera Matching** as e.g. `Camera ST (A7V)`.

> **Note**: You must have an ILCE-7M5 raw file open; Lightroom only shows
> profiles that match the `UniqueCameraModel` tag of the current image.

---

## Paths reference

### macOS (Lightroom Classic system-wide)

| Role | Path |
|------|------|
| Donor profiles (RX1R III) | `/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony DSC-RX1RM3/` |
| Colour source (A7V Adobe Standard) | `/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Adobe Standard/Sony ILCE-7M5 Adobe Standard.dcp` |
| System install target | `/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Camera/Sony ILCE-7M5/` |
| Local output | `<script_dir>/output/Sony ILCE-7M5/` |

### Windows (Lightroom Classic system-wide)

| Role | Path |
|------|------|
| Donor profiles (RX1R III) | `C:\ProgramData\Adobe\CameraRaw\CameraProfiles\Camera\Sony DSC-RX1RM3\` |
| Colour source (A7V Adobe Standard) | `C:\ProgramData\Adobe\CameraRaw\CameraProfiles\Adobe Standard\Sony ILCE-7M5 Adobe Standard.dcp` |
| System install target | `C:\ProgramData\Adobe\CameraRaw\CameraProfiles\Camera\Sony ILCE-7M5\` |
| Local output | `<script_dir>\output\Sony ILCE-7M5\` |

> **Per-user location (Windows):** If `C:\ProgramData\Adobe\...` does not
> exist, check `%APPDATA%\Adobe\CameraRaw\CameraProfiles\` instead
> (`C:\Users\<username>\AppData\Roaming\Adobe\CameraRaw\CameraProfiles\`).

---

## Technical details

### What a DCP file is

A **DCP (DNG Camera Profile)** is a TIFF-family binary file. Its IFD
(Image File Directory) entries store colour transformation data as private
Adobe tags. The file is typically < 500 KB; the dominant payload is the
LookTable (a 3D colour LUT) and optional ToneCurve.

### Patch pipeline

The script reads the donor DCP as raw bytes, walks its IFD, and patches
values in-place where possible:

| Operation | Strategy |
|-----------|----------|
| ASCII model strings | Append new string at end of file, update IFD offset + count |
| SRATIONAL matrices (9 × 8 bytes = 72 bytes) | Overwrite existing slot — same size, no pointer change needed |
| Everything else | Untouched (byte-for-byte copy) |

### Colour matrix sources

| Tag | Hex | Source |
|-----|-----|--------|
| `ColorMatrix1` | `0xC621` | `Sony ILCE-7M5 Adobe Standard.dcp` |
| `ColorMatrix2` | `0xC622` | `Sony ILCE-7M5 Adobe Standard.dcp` |
| `ForwardMatrix1` | `0xC714` | ProPhoto RGB → XYZ D50 (see below) |
| `ForwardMatrix2` | `0xC715` | ProPhoto RGB → XYZ D50 (see below) |

**ColorMatrix** values extracted from the A7V's own Adobe Standard profile
(illuminant D65 for CM2, standard illuminant A for CM1). This gives the A7V
correct sensor characterisation for white-balance computation.

### ColorMatrix values (from A7V Adobe Standard)

```
ColorMatrix1 (illuminant A ≈ 2856 K):
  [ 1.1168, -0.6826,  0.0991,
   -0.3276,  1.0617,  0.3080,
   -0.0050,  0.0460,  0.7113 ]

ColorMatrix2 (illuminant D65 ≈ 6504 K):
  [ 0.9089, -0.3577, -0.0787,
   -0.3563,  1.1326,  0.2557,
   -0.0114,  0.0928,  0.5904 ]
```

### ForwardMatrix: ProPhoto RGB → XYZ D50

```
ForwardMatrix1 = ForwardMatrix2 =
  [ 0.7976749,  0.1351917,  0.0313534,
    0.2880402,  0.7118741,  0.0000857,
    0.0000000,  0.0000000,  0.8252100 ]
```

This is the **canonical identity forward matrix** for Camera Matching profiles.
It is the exact ProPhoto RGB primaries expressed in XYZ D50, which tells
Lightroom "delegate all creative colour work to the LookTable — do not apply
any additional chromatic adaptation." This is the same matrix Adobe uses in
every other Camera Matching DCP.

### Why ColorMatrix and ForwardMatrix are not independent

The two represent the same transform via:

```
F × D = CAT(WP → D50) × C⁻¹
```

where:
- **C** = ColorMatrix (sensor raw → XYZ)
- **F** = ForwardMatrix (ProPhoto RGB → XYZ D50)
- **D** = diagonal white-balance multiplier matrix
- **CAT** = Bradford chromatic adaptation transform

When no ForwardMatrix is present, Lightroom inverts C and adapts chromatically.
In Camera Matching profiles, F is always the ProPhoto pass-through above, so
Lightroom uses C only for white balance and lets the LookTable handle the
creative colour rendition.

### LookTable and ToneCurve

These are taken **byte-for-byte** from the RX1R III donor profiles. The
LookTable encodes Sony's Picture Profile rendering (e.g. Vivid saturation boost,
Black & White desaturation). The ToneCurve encodes the S-curve contrast. Both
are sensor-response-independent and transfer cleanly to the A7V.

---

## Troubleshooting

**Profiles don't appear in Lightroom**
- Ensure the open image is an ILCE-7M5 raw file (ARW).
- Restart Lightroom after installing to the system folder.
- Try the Import dialog method instead of the system folder.

**Lightroom crashes immediately after importing the profiles**
- This is a known first-launch quirk. When Lightroom encounters a new batch
  of DCP files for the first time it rebuilds its profile index, which can
  cause a crash on some systems.
- **Workaround**: Simply relaunch Lightroom. On the second launch the index
  is already built and the profiles load and work correctly. No further
  crashes should occur.

**"Permission denied" when running the script**
- The script writes to `./output/` (no elevated permissions needed). If you
  see permission errors, check that the `output/` subfolder is writable.
- For system-wide install, `sudo` (macOS) or **Run as Administrator** (Windows)
  is required only for the copy step, not for running the script itself.

**Profile looks wrong / colours are off**
- Verify the A7V Adobe Standard DCP is present at the path listed in the
  [Paths reference](#paths-reference) above.
- Re-run the script; it prints the ColorMatrix values it extracted so you can
  cross-check them.

**Windows: `C:\ProgramData` is not visible in File Explorer**
- Enable **Show hidden items** in File Explorer's View menu, or type the path
  directly into the address bar.

---

## FAQ

### Why do these profiles work, but the ones bundled in Lightroom look wrong for the A7V?

As of mid-2026, Adobe has not yet released official Camera Matching profiles
for the ILCE-7M5. The profiles that Lightroom *does* show for the A7V are a
fallback — either the generic **Adobe Color / Adobe Standard** profiles (which
are built from Adobe's own perceptual model and make no attempt to replicate
Sony's in-camera Picture Profiles), or profiles from a closely-related camera
that Lightroom maps as a proxy.

Here is why these generated profiles look better at matching in-camera JPEGs:

| What | Bundled Adobe profiles | These profiles |
|------|------------------------|----------------|
| **ColorMatrix** | From the A7V sensor calibration ✓ | Also from the A7V sensor calibration ✓ |
| **ForwardMatrix** | Adobe's perceptual creative matrix | ProPhoto RGB pass-through (neutral) |
| **LookTable** | Adobe Color look, or none | Sony's own Picture Profile LUT (from the RX1R III) |
| **ToneCurve** | Adobe's curve | Sony's S-curve (from the RX1R III) |

The critical element is the **LookTable**. Sony's Camera Matching Look Tables
encode the specific hue, saturation, and luminance shifts that reproduce each
Picture Profile (Standard, Vivid, Neutral, etc.) — the same rendering the
camera applies when generating in-camera JPEGs. Adobe's built-in profiles for
the A7V don't have these LUTs because Adobe has not yet characterised the
camera for them.

The RX1R III is a closely related Sony camera whose sensor pipeline produces
very similar colour science to the A7V. Its Picture Profile LUTs transfer
cleanly: the colour engine (ColorMatrix) is kept A7V-specific, while the
creative rendering (LookTable + ToneCurve) comes from the RX1R III. The
ForwardMatrix is set to the neutral ProPhoto pass-through so that Lightroom
applies no additional creative adaptation on top of the LUT.

The net result is that the rendered colour in Lightroom closely matches what
you see in-camera — which is precisely what Camera Matching profiles are
designed to do.
