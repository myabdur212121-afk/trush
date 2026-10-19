#!/usr/bin/env bash
# ==============================================================================
# font.sh - Download, Install & Configure CMU Serif and Noto Serif Bengali
# ==============================================================================
set -euo pipefail

echo "==> [1/4] Preparing font directories..."
INSTALL_DIR_CMU="/usr/local/share/fonts/truetype/cmu-serif"
INSTALL_DIR_NOTO="/usr/local/share/fonts/truetype/noto-serif-bengali"
USER_FONTS_DIR="$HOME/fonts"

sudo mkdir -p "$INSTALL_DIR_CMU" "$INSTALL_DIR_NOTO"
mkdir -p "$USER_FONTS_DIR/cmu-serif" "$USER_FONTS_DIR/noto-serif-bengali"

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "==> [2/4] Installing CMU Serif fonts..."
# Option A: Check if Debian package fonts-cmu is available
if sudo apt-get install -y --no-install-recommends fonts-cmu >/dev/null 2>&1; then
    echo "    -> Installed fonts-cmu via package manager."
    sudo cp /usr/share/fonts/truetype/cmu/cmun*.ttf "$INSTALL_DIR_CMU/"
    cp /usr/share/fonts/truetype/cmu/cmun*.ttf "$USER_FONTS_DIR/cmu-serif/"
else
    echo "    -> Downloading CMU Serif fonts from SourceForge..."
    curl -fsSL "https://downloads.sourceforge.net/project/cm-unicode/cm-unicode/0.7.0/cm-unicode-0.7.0-ttf.tar.xz" -o "$TMP_DIR/cmu.tar.xz"
    tar -xf "$TMP_DIR/cmu.tar.xz" -C "$TMP_DIR"
    sudo cp "$TMP_DIR"/cm-unicode-*/cmun*.ttf "$INSTALL_DIR_CMU/"
    cp "$TMP_DIR"/cm-unicode-*/cmun*.ttf "$USER_FONTS_DIR/cmu-serif/"
fi

echo "==> [3/4] Downloading & Installing Noto Serif Bengali from Google/notofonts..."
NOTO_URL="https://github.com/notofonts/bengali/releases/download/NotoSerifBengali-v3.000/NotoSerifBengali-v3.000.zip"
curl -fsSL "$NOTO_URL" -o "$TMP_DIR/NotoSerifBengali.zip"
unzip -q -o "$TMP_DIR/NotoSerifBengali.zip" -d "$TMP_DIR/noto_extracted"

# Copy full TTF variants
sudo cp "$TMP_DIR"/noto_extracted/NotoSerifBengali/full/ttf/*.ttf "$INSTALL_DIR_NOTO/"
cp "$TMP_DIR"/noto_extracted/NotoSerifBengali/full/ttf/*.ttf "$USER_FONTS_DIR/noto-serif-bengali/"

echo "==> [4/4] Refreshing font cache..."
sudo fc-cache -fv /usr/local/share/fonts >/dev/null 2>&1
fc-cache -fv "$HOME/.local/share/fonts" >/dev/null 2>&1 || true

echo ""
echo "=== Verification ==="
echo "CMU Serif font faces:"
fc-list : family | grep -i "cmu serif" | sort -u || true

echo ""
echo "Noto Serif Bengali font faces:"
fc-list : family | grep -i "noto serif bengali" | head -n 5 || true

echo ""
echo "Successfully installed CMU Serif and Noto Serif Bengali!"
