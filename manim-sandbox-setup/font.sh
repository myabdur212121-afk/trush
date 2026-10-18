#!/usr/bin/env bash
# CMU Serif (Computer Modern Unicode) + Noto Serif Bengali.
# Extracted fonts, licenses and checksums persist in <workspace>/fonts/.
# Do not put the saved fonts in .cache, .local or .venv: Arena excludes those.
set -Eeuo pipefail
trap 'printf "[fonts] Failed at line %s. Fix the error above and rerun.\n" "$LINENO" >&2' ERR

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
WORKSPACE="${MANIM_WORKSPACE:-$SCRIPT_DIR}"
DRY_RUN=0
CHECK_ONLY=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --check) CHECK_ONLY=1 ;;
        -h|--help)
            cat <<'HELP'
Usage: bash font.sh [--dry-run | --check]
Download CMU Serif and Noto Serif Bengali once, then reuse the workspace copies.
Both Manim installers call this helper automatically. No LaTeX is installed.

  --dry-run  Show the plan without network access or filesystem changes.
  --check    Quiet, offline check; exit 0 only if saved fonts are intact and active.

MANIM_WORKSPACE defaults to this script's directory; use an absolute path.
Fonts are registered for the current user via Fontconfig. Run as your normal
user; passwordless sudo is needed only if download/font tools are missing.
HELP
            exit 0 ;;
        *) printf 'Unknown option: %s\n' "$arg" >&2; exit 2 ;;
    esac
done
[[ "$WORKSPACE" = /* ]] || { echo 'MANIM_WORKSPACE must be an absolute path.' >&2; exit 2; }
WORKSPACE="$(realpath -m -- "$WORKSPACE")"
FONT_ROOT="$WORKSPACE/fonts"
CMU_DIR="$FONT_ROOT/cmu-serif"
NOTO_DIR="$FONT_ROOT/noto-serif-bengali"
CMU_FILES=(cmunrm.ttf cmunbx.ttf cmunti.ttf cmunbi.ttf)
NOTO_WEIGHTS=(Thin ExtraLight Light Regular Medium SemiBold Bold ExtraBold Black)
CMU_URL='https://downloads.sourceforge.net/project/cm-unicode/cm-unicode/0.7.0/cm-unicode-0.7.0-ttf.tar.xz'
CMU_SHA256='2609c14450f42d0bcd40203900afcb1d693521a9b24a18c65e14b6b0585ff150'
NOTO_URL='https://github.com/notofonts/bengali/releases/download/NotoSerifBengali-v3.000/NotoSerifBengali-v3.000.zip'
NOTO_SHA256='3ee7ed1a48f115298ec7fd42d3d72c51fcdca6e7adceae65a0fa4f652b164795'

cmu_cached() {
    local file
    [[ -s "$CMU_DIR/SHA256SUMS" && -s "$CMU_DIR/OFL.txt" ]] || return 1
    for file in "${CMU_FILES[@]}"; do [[ -s "$CMU_DIR/$file" ]] || return 1; done
    (cd -- "$CMU_DIR" && sha256sum --status -c SHA256SUMS) 2>/dev/null
}
noto_cached() {
    local weight
    [[ -s "$NOTO_DIR/SHA256SUMS" && -s "$NOTO_DIR/OFL.txt" ]] || return 1
    for weight in "${NOTO_WEIGHTS[@]}"; do
        [[ -s "$NOTO_DIR/NotoSerifBengali-$weight.ttf" ]] || return 1
    done
    (cd -- "$NOTO_DIR" && sha256sum --status -c SHA256SUMS) 2>/dev/null
}
fonts_active() {
    command -v fc-list >/dev/null 2>&1 || return 1
    local cmu noto
    # Check that OUR saved fonts are registered. Do not require them to win
    # fc-match over a user's existing fonts or duplicates from texlive-full.
    cmu="$(fc-list -f '%{file}\n' 'CMU Serif' 2>/dev/null)" || return 1
    noto="$(fc-list -f '%{file}\n' 'Noto Serif Bengali' 2>/dev/null)" || return 1
    grep -Fx -- "$CMU_DIR/cmunrm.ttf" <<< "$cmu" >/dev/null &&
        grep -Fx -- "$NOTO_DIR/NotoSerifBengali-Regular.ttf" <<< "$noto" >/dev/null
}

if (( CHECK_ONLY )); then
    if cmu_cached && noto_cached && fonts_active; then exit 0; else exit 1; fi
fi
if (( DRY_RUN )); then
    printf '[fonts] Persistent destination: %s\n' "$FONT_ROOT"
    if cmu_cached; then echo '[fonts] Reuse saved CMU Serif (no download).'
    else printf '[fonts] Download, verify SHA-256 and extract four CMU Serif faces: %s\n' "$CMU_URL"; fi
    if noto_cached; then echo '[fonts] Reuse saved Noto Serif Bengali (no download).'
    else printf '[fonts] Download, verify SHA-256 and extract nine normal-width Noto weights: %s\n' "$NOTO_URL"; fi
    echo '[fonts] Install missing download/Fontconfig tools only; register fonts if needed.'
    exit 0
fi
# Fast path: no apt, curl, configuration rewrite or cache refresh on a repeat run.
if cmu_cached && noto_cached && fonts_active; then
    echo '[fonts] Already saved and registered. Nothing to download or reinstall.'
    exit 0
fi

# Install tools only when actually needed. A saved font can be restored offline
# as long as Fontconfig is present, even if curl/unzip are not installed.
packages=()
for tool in fc-cache fc-match fc-list fc-scan; do
    if ! command -v "$tool" >/dev/null 2>&1; then packages+=(fontconfig); break; fi
done
if ! cmu_cached || ! noto_cached; then
    command -v curl >/dev/null 2>&1 || packages+=(curl)
    [[ -s /etc/ssl/certs/ca-certificates.crt ]] || packages+=(ca-certificates)
fi
if ! cmu_cached; then command -v xz >/dev/null 2>&1 || packages+=(xz-utils); fi
if ! noto_cached; then command -v unzip >/dev/null 2>&1 || packages+=(unzip); fi
if (( ${#packages[@]} )); then
    command -v apt-get >/dev/null 2>&1 || { echo 'Install curl, xz, unzip and Fontconfig first (Debian/Ubuntu supported).' >&2; exit 1; }
    SUDO=()
    if (( EUID != 0 )); then
        if ! command -v sudo >/dev/null 2>&1 || ! sudo -n true; then
            echo 'Missing tools require root or passwordless sudo.' >&2
            exit 1
        fi
        SUDO=(sudo -n)
    fi
    "${SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 update
    "${SUDO[@]}" env DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 install -y --no-install-recommends "${packages[@]}"
fi

mkdir -p -- "$FONT_ROOT" "$WORKSPACE/.cache"
# A second engine can share this helper without racing the first font download.
if command -v flock >/dev/null 2>&1; then exec 9>"$FONT_ROOT/.install.lock"; flock 9; fi
TMP_DIR="$(mktemp -d "$WORKSPACE/.cache/font-install.XXXXXX")"
trap 'rm -rf -- "$TMP_DIR"' EXIT

download() {
    curl --proto '=https' --tlsv1.2 --fail --location --silent --show-error \
        --retry 3 --connect-timeout 20 --max-time 300 "$1" -o "$2"
    printf '%s  %s\n' "$3" "$2" | sha256sum --check --status
}

if ! cmu_cached; then
    echo '[fonts] Downloading CMU Serif 0.7.0...'
    download "$CMU_URL" "$TMP_DIR/cmu.tar.xz" "$CMU_SHA256"
    mkdir -p -- "$TMP_DIR/cmu"
    for file in "${CMU_FILES[@]}" OFL.txt; do
        tar -xJOf "$TMP_DIR/cmu.tar.xz" "cm-unicode-0.7.0/$file" > "$TMP_DIR/cmu/$file"
    done
    for file in "$TMP_DIR/cmu/"*.ttf; do fc-scan "$file" >/dev/null; done
    (cd -- "$TMP_DIR/cmu" && sha256sum ./*.ttf OFL.txt > SHA256SUMS)
    mkdir -p -- "$CMU_DIR"
    install -m 0644 "$TMP_DIR/cmu/"*.ttf "$TMP_DIR/cmu/OFL.txt" "$CMU_DIR/"
    install -m 0644 "$TMP_DIR/cmu/SHA256SUMS" "$CMU_DIR/SHA256SUMS"
else
    echo '[fonts] Reusing saved CMU Serif.'
fi

if ! noto_cached; then
    echo '[fonts] Downloading Noto Serif Bengali 3.000...'
    download "$NOTO_URL" "$TMP_DIR/noto.zip" "$NOTO_SHA256"
    mkdir -p -- "$TMP_DIR/noto"
    for weight in "${NOTO_WEIGHTS[@]}"; do
        file="NotoSerifBengali-$weight.ttf"
        unzip -p "$TMP_DIR/noto.zip" "NotoSerifBengali/full/ttf/$file" > "$TMP_DIR/noto/$file"
    done
    unzip -p "$TMP_DIR/noto.zip" OFL.txt > "$TMP_DIR/noto/OFL.txt"
    for file in "$TMP_DIR/noto/"*.ttf; do fc-scan "$file" >/dev/null; done
    (cd -- "$TMP_DIR/noto" && sha256sum ./*.ttf OFL.txt > SHA256SUMS)
    mkdir -p -- "$NOTO_DIR"
    install -m 0644 "$TMP_DIR/noto/"*.ttf "$TMP_DIR/noto/OFL.txt" "$NOTO_DIR/"
    install -m 0644 "$TMP_DIR/noto/SHA256SUMS" "$NOTO_DIR/SHA256SUMS"
else
    echo '[fonts] Reusing saved Noto Serif Bengali.'
fi

# Register the persistent directory directly, rather than saving the only copies
# under .local/share/fonts (which is not persisted by Arena).
if ! fonts_active; then
    CONF_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/fontconfig/conf.d"
    mkdir -p -- "$CONF_DIR"
    XML_PATH="$(printf '%s' "$FONT_ROOT" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' -e 's/"/\&quot;/g')"
    cat > "$TMP_DIR/fontconfig.conf" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>$XML_PATH</dir>
</fontconfig>
EOF
    install -m 0644 "$TMP_DIR/fontconfig.conf" "$CONF_DIR/50-manim-workspace-fonts.conf"
fi
fc-cache -f "$FONT_ROOT"
if ! cmu_cached || ! noto_cached || ! fonts_active; then
    echo '[fonts] Font verification failed; check Fontconfig configuration.' >&2
    exit 1
fi
printf '[fonts] Ready. Saved files: %s\n' "$FONT_ROOT"
fc-match -f '  %{family}: %{file}\n' 'CMU Serif:style=Roman'
fc-match -f '  %{family}: %{file}\n' 'Noto Serif Bengali:style=Regular'
