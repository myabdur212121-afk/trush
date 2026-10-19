# Validation record

Publication record: **2026-10-08 (Asia/Dhaka)**. Checks are local sandbox results,
not a claim of a GitHub Actions run or support for every Linux/Python combination.

## Environment

- Debian GNU/Linux 13 (trixie), x86-64.
- Python 3.13.16.
- ManimGL 1.7.2 in its own venv; IPython 8.21.0 and setuptools 80.9.0.
- Manim Community 0.21.0 in a separate venv; IPython 8.21.0.
- FFmpeg 7.1.5; dvisvgm 3.4.4; distro TeX Live reported as 2025/dev/Debian.
- No physical GPU was needed. GL renders used the Xvfb/software OpenGL path.

The original installer preparation included fresh engine installations followed
by the slim TeX installation. Repository publication checks additionally exercise
repeat setup against the existing workspace. These are different kinds of tests:
a successful repeat setup alone is not proof of a clean-system installation.

## Installer preparation results

| Check | Result |
|---|---|
| Fresh GL and CE installations in separate environments | Passed |
| Neither engine installer installs the other engine or LaTeX | Confirmed before the separate TeX installation |
| CLI/import checks and `python -m pip check` | Passed for both engines |
| English/Bengali `FontsOnly` videos without LaTeX | Passed for both engines |
| Actual slim TeX installation and formula-to-SVG check | Passed |
| `FontsAndMath` video with slim TeX | Passed for both engines |
| Bengali/CMU Serif XeLaTeX PDF without missing-character warnings | Passed |
| Font helper repeat run skips downloading | Passed |
| Fresh Fontconfig registration with download commands blocked | Passed; all 13 TTF contents and mtimes unchanged |
| Copied cache under a path with spaces, XML special characters and Bengali | Passed without downloading |
| Corrupt cached family rejected and scheduled for repair | Passed |
| `texlive-full` and `texlive-fonts-extra` absent after slim setup | Confirmed |

## Publication checks

| Check | Result |
|---|---|
| 16 offline script/repository tests | Passed |
| Bash syntax and ShellCheck on all five installers | Passed |
| ShellCheck on the generated GL/CE wrappers | Passed |
| Repeated GL, CE and slim installation using the existing `MANIM_WORKSPACE` | Passed; saved fonts reused |
| Four fresh final videos: GL/CE × `FontsOnly`/`FontsAndMath` | Passed; non-empty MP4s readable by ffprobe |
| Fresh GL cache for the math render | Passed; did not depend on the previous TeX SVG cache |
| Included `examples/bengali.tex` compiled with XeLaTeX | Passed; PDF produced, no missing-character warnings |
| Fresh font registration and repeat run with network/install commands blocked | Passed; all 13 saved TTFs retained their contents and modification times |
| Full TeX APT dependency simulation | Passed; full TeX and fonts-extra remained uninstalled |
| Git ignore rules and local Markdown links | Passed |
| GitHub issue-template YAML parse | Passed |

The measured headless renderer was:

```text
llvmpipe (LLVM 19.1.7, 256 bits)
```

This is **software rendering**, not a hardware-GPU claim. The four verification
videos, PDF, logs and runtime dependencies are intentionally not repository assets.

## Deliberate limits

- **Full LaTeX was not installed or render-tested.** Its Bash syntax, ShellCheck,
  dry-run and APT dependency resolution were checked only. Full installation
  remains a large, separately requested operation.
- Ubuntu, other CPU architectures, other Python versions, real hardware-GPU
  acceleration and alternate engine versions were not separately verified.
- The font restore test simulated missing per-user Fontconfig registration;
  it was not a complete provider-triggered sandbox reboot.
- Engine versions and selected compatibility dependencies are pinned, but this
  is not a complete lockfile for every transitive pip or distro package.
- There is no GitHub Actions workflow in this initial publication. Run the
  offline tests and lint commands below or in your own approved CI environment.

## Repeat the offline checks

```bash
python3 -m unittest discover -s tests -v
shellcheck *.sh
```

For integration checks, follow the [sandbox guide](sandbox-guide.md). Keep render
outputs, font downloads, logs and runtime environments out of Git. Update this
record with the actual environment and outcomes when validating future changes.
