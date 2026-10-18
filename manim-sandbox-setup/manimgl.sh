#!/usr/bin/env bash
# Install ONLY ManimGL + runtime/build dependencies + shared fonts. No LaTeX.
# Based on sandbox/manimgl/manimgl-e2b-sandbox.md in the supplied repository.
set -Eeuo pipefail
trap 'printf "[manimgl] Failed at line %s. Fix the error above and rerun.\n" "$LINENO" >&2' ERR

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
WORKSPACE="${MANIM_WORKSPACE:-$SCRIPT_DIR}"
MANIMGL_VERSION="${MANIMGL_VERSION:-1.7.2}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help)
            cat <<'HELP'
Usage: bash manimgl.sh [--dry-run]
Install ManimGL only, in its own virtual environment, with CMU Serif and
Noto Serif Bengali. Does NOT install ManimCE or LaTeX.

Optional extensions: bash latex_slim.sh  OR  bash latex_full.sh
Run this as your normal user with passwordless sudo (Debian/Ubuntu).
Python 3.11+ is required. No shell startup files or system Python are modified.

Environment overrides:
  MANIM_WORKSPACE  Absolute destination; default: this script's directory.
  MANIMGL_VERSION PyPI version; default: 1.7.2 (stable OpenGL release).
  PYTHON_BIN      Interpreter; default: python3.

Use <workspace>/bin/manimgl scene.py SceneName -w -l -c '#000000'
The wrapper starts Xvfb when no display exists and uses software OpenGL by
default. Set LIBGL_ALWAYS_SOFTWARE=0 to allow hardware acceleration.
Always use -w in a sandbox; no interactive preview window is available.
HELP
            exit 0 ;;
        *) printf 'Unknown option: %s\n' "$arg" >&2; exit 2 ;;
    esac
done
[[ "$WORKSPACE" = /* ]] || { echo 'MANIM_WORKSPACE must be an absolute path.' >&2; exit 2; }
WORKSPACE="$(realpath -m -- "$WORKSPACE")"
VENV="$WORKSPACE/.venv/manimgl"
[[ -r "$SCRIPT_DIR/font.sh" ]] || { echo 'Required helper font.sh must be beside manimgl.sh.' >&2; exit 1; }
PACKAGES=(
    python3 python3-dev python3-venv build-essential pkg-config
    libcairo2-dev libpango1.0-dev ffmpeg
    libgl1 libegl1 libgl1-mesa-dri libglx-mesa0 xvfb xauth
    ca-certificates curl fontconfig unzip xz-utils
)
# audioop was removed from Python 3.13; pydub in ManimGL still needs it.
# Keep IPython 8.21.0 for compatibility with the repository's environment.
# ManimGL 1.7.2 imports pkg_resources, removed in newer setuptools releases.
REQUIREMENTS=("manimgl==$MANIMGL_VERSION" 'ipython==8.21.0' 'setuptools==80.9.0'
    'audioop-lts>=0.2.1; python_version >= "3.13"')

if (( DRY_RUN )); then
    printf '[manimgl] Missing apt packages only: %s\n' "${PACKAGES[*]}"
    printf '[manimgl] Create/reuse virtual environment: %s\n' "$VENV"
    printf '[manimgl] pip install: %s\n' "${REQUIREMENTS[*]}"
    MANIM_WORKSPACE="$WORKSPACE" bash "$SCRIPT_DIR/font.sh" --dry-run
    printf '[manimgl] Write headless wrapper: %s/bin/manimgl\n' "$WORKSPACE"
    echo '[manimgl] Verify imports and CLI. No ManimCE or LaTeX will be installed.'
    exit 0
fi
command -v apt-get >/dev/null 2>&1 || { echo 'This installer supports Debian/Ubuntu with apt-get.' >&2; exit 1; }
MISSING=()
for package in "${PACKAGES[@]}"; do
    if [[ "$(dpkg-query -W -f='${db:Status-Status}' "$package" 2>/dev/null || true)" != installed ]]; then MISSING+=("$package"); fi
done
if (( ${#MISSING[@]} )); then
    SUDO=()
    if (( EUID != 0 )); then
        if ! command -v sudo >/dev/null 2>&1 || ! sudo -n true; then
            echo 'Missing packages require root or passwordless sudo.' >&2
            exit 1
        fi
        SUDO=(sudo -n)
    fi
    "${SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 update
    "${SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 install -y --no-install-recommends "${MISSING[@]}"
fi
"$PYTHON_BIN" -c 'import sys; sys.exit("Python 3.11+ is required.") if sys.version_info < (3, 11) else None'
mkdir -p -- "$WORKSPACE/bin" "$WORKSPACE/.venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$PYTHON_BIN" -m venv "$VENV"; fi
"$VENV/bin/python" -m pip --disable-pip-version-check install --no-cache-dir "${REQUIREMENTS[@]}"
MANIM_WORKSPACE="$WORKSPACE" bash "$SCRIPT_DIR/font.sh"

# Use a wrapper rather than editing ManimGL source to force an EGL backend.
# The stable OpenGL release creates an X11 standalone context by default.
cat > "$WORKSPACE/bin/manimgl" <<'WRAPPER'
#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
ENGINE="$ROOT/.venv/manimgl/bin/manimgl"
if [[ ! -x "$ENGINE" ]]; then
    echo 'ManimGL runtime is missing. Rerun manimgl.sh after a sandbox reset.' >&2
    exit 1
fi
# The optional LaTeX installers write this profile. An explicit user config wins.
PROFILE="$ROOT/configs/manimgl-tex.yml"
EXTRA=()
CUSTOM_CONFIG=0
for arg in "$@"; do
    case "$arg" in --config_file|--config_file=*) CUSTOM_CONFIG=1 ;; esac
done
if [[ -f "$PROFILE" ]] && (( ! CUSTOM_CONFIG )); then EXTRA=(--config_file "$PROFILE"); fi
if [[ -z "${DISPLAY:-}" ]]; then
    command -v xvfb-run >/dev/null 2>&1 || { echo 'Xvfb is missing. Rerun manimgl.sh.' >&2; exit 1; }
    export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
    exec xvfb-run -a -s '-screen 0 1280x720x24' "$ENGINE" "${EXTRA[@]}" "$@"
fi
exec "$ENGINE" "${EXTRA[@]}" "$@"
WRAPPER
chmod +x "$WORKSPACE/bin/manimgl"
"$WORKSPACE/bin/manimgl" --version
"$VENV/bin/python" -m pip check
ffmpeg -version | sed -n '1p'
printf '\n[manimgl] Ready (LaTeX not installed by this script).\n'
printf 'Render: "%s/bin/manimgl" scene.py SceneName -w -l -c "#000000"\n' "$WORKSPACE"
printf 'Python environment: %s\n' "$VENV"
printf 'For math, run latex_slim.sh or latex_full.sh in the same workspace.\n'
