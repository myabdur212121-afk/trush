#!/usr/bin/env bash
# ==============================================================================
# setup_manim.sh - Automated environment restore for Manim & LaTeX session
# ==============================================================================
set -e

echo "=== [1/4] Updating package repositories ==="
sudo apt-get update

echo "=== [2/4] Installing system dependencies & LaTeX suite ==="
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    dvisvgm \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa

echo "=== [3/4] Installing Manim and IPython ==="
pip install manim ipython==8.21.0

echo "=== [4/4] Verifying and configuring fonts ==="
if [ -f "/home/user/scripts/font.sh" ]; then
    bash /home/user/scripts/font.sh
fi

echo "=== System Verification ==="
manim --version
ipython --version
latex --version

echo "=========================================================="
echo "Manim & LaTeX environment successfully restored and ready!"
echo "=========================================================="
