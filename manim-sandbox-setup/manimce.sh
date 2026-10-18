#!/usr/bin/env bash
# Install ONLY Manim Community + runtime/build dependencies + shared fonts.
# Based on sandbox/manimce/setup_manim.sh; LaTeX is now a separate extension.
set -Eeuo pipefail
trap 'printf "[manimce] Failed at line %s. Fix the error above and rerun.\n" "$LINENO" >&2' ERR

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
WORKSPACE="${MANIM_WORKSPACE:-$SCRIPT_DIR}"
MANIMCE_VERSION="${MANIMCE_VERSION:-0.21.0}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help)
            cat <<'HELP'
Usage: bash manimce.sh [--dry-run]
Install Manim Community (Cairo renderer) in its own virtual environment, with
CMU Serif and Noto Serif Bengali. Does NOT install ManimGL or LaTeX.

Optional extensions: bash latex_slim.sh  OR  bash latex_full.sh
Run as your normal user with passwordless sudo (Debian/Ubuntu).
Python 3.11+ is required. No shell startup files or system Python are modified.

Environment overrides:
  MANIM_WORKSPACE  Absolute destination; default: this script's directory.
  MANIMCE_VERSION PyPI version; default: 0.21.0.
  PYTHON_BIN      Interpreter; default: python3.

Use <workspace>/bin/manim -ql scene.py SceneName
<workspace>/bin/manimce is an alias for the same command.
HELP
            exit 0 ;;
        *) printf 'Unknown option: %s\n' "$arg" >&2; exit 2 ;;
    esac
done
[[ "$WORKSPACE" = /* ]] || { echo 'MANIM_WORKSPACE must be an absolute path.' >&2; exit 2; }
WORKSPACE="$(realpath -m -- "$WORKSPACE")"
VENV="$WORKSPACE/.venv/manimce"
[[ -r "$SCRIPT_DIR/font.sh" ]] || { echo 'Required helper font.sh must be beside manimce.sh.' >&2; exit 1; }
PACKAGES=(
    python3 python3-dev python3-venv build-essential pkg-config
    libcairo2-dev libpango1.0-dev ffmpeg
    ca-certificates curl fontconfig unzip xz-utils
)
REQUIREMENTS=("manim==$MANIMCE_VERSION" 'ipython==8.21.0')

if (( DRY_RUN )); then
    printf '[manimce] Missing apt packages only: %s\n' "${PACKAGES[*]}"
    printf '[manimce] Create/reuse virtual environment: %s\n' "$VENV"
    printf '[manimce] pip install: %s\n' "${REQUIREMENTS[*]}"
    MANIM_WORKSPACE="$WORKSPACE" bash "$SCRIPT_DIR/font.sh" --dry-run
    printf '[manimce] Write CLI wrappers: %s/bin/manim and bin/manimce\n' "$WORKSPACE"
    echo '[manimce] Verify imports and CLI. No ManimGL or LaTeX will be installed.'
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

cat > "$WORKSPACE/bin/manim" <<'WRAPPER'
#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
ENGINE="$ROOT/.venv/manimce/bin/manim"
if [[ ! -x "$ENGINE" ]]; then
    echo 'ManimCE runtime is missing. Rerun manimce.sh after a sandbox reset.' >&2
    exit 1
fi
exec "$ENGINE" "$@"
WRAPPER
chmod +x "$WORKSPACE/bin/manim"
ln -sfn manim "$WORKSPACE/bin/manimce"
"$WORKSPACE/bin/manim" --version
"$VENV/bin/python" -c 'import manim, IPython; print("Imports OK:", manim.__version__, "| IPython", IPython.__version__)'
"$VENV/bin/python" -m pip check
ffmpeg -version | sed -n '1p'
printf '\n[manimce] Ready (LaTeX not installed by this script).\n'
printf 'Render: "%s/bin/manim" -ql scene.py SceneName\n' "$WORKSPACE"
printf 'Python environment: %s\n' "$VENV"
printf 'For MathTex/Tex, run latex_slim.sh or latex_full.sh separately.\n'
