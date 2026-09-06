#!/usr/bin/env bash
# Prepare real photographs for the site.
#
# Run this on the originals Mark sends, NOT on the placeholders already in the repo.
# It resizes, strips camera metadata, compresses, and writes matching WebP files.
#
#   ./tools/prepare-images.sh ~/Downloads/special-green-photos
#
# Needs ImageMagick and cwebp:
#   macOS:  brew install imagemagick webp
#   Ubuntu: sudo apt install imagemagick webp
set -euo pipefail

SRC="${1:?usage: prepare-images.sh <folder-of-originals>}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/assets/images"
mkdir -p "$DEST"

command -v magick >/dev/null 2>&1 && IM=magick || IM=convert
command -v "$IM" >/dev/null 2>&1 || { echo "ImageMagick not found"; exit 1; }

shopt -s nullglob nocaseglob
for f in "$SRC"/*.{jpg,jpeg,png,heic,webp}; do
  base="$(basename "${f%.*}")"
  out="$DEST/$base.jpg"

  # Longest edge 2400, sRGB, metadata stripped, quality 82.
  # -strip removes GPS coordinates, which matter: photos taken at customers'
  # homes carry their addresses unless the location data is removed.
  "$IM" "$f" -auto-orient -colorspace sRGB -resize '2400x2400>' \
        -strip -interlace Plane -quality 82 "$out"

  if command -v cwebp >/dev/null 2>&1; then
    cwebp -quiet -q 80 "$out" -o "$DEST/$base.webp"
  fi
  printf '  %-38s %s\n' "$base.jpg" "$(du -h "$out" | cut -f1)"
done

# Point the page at each real photograph now that it exists. The repo ships SVG
# placeholders so nothing is ever broken; this swaps a slot to .jpg only once a
# real file for that slot is actually on disk.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
swapped=0
for jpg in "$DEST"/*.jpg; do
  [ -e "$jpg" ] || continue
  base="$(basename "${jpg%.jpg}")"
  if grep -q "assets/images/$base.svg" "$ROOT/index.html"; then
    sed -i.bak "s|assets/images/$base\.svg|assets/images/$base.jpg|g" "$ROOT/index.html"
    rm -f "$ROOT/index.html.bak"
    rm -f "$DEST/$base.svg"
    swapped=$((swapped+1))
  fi
done

echo
echo "Done. Files are in assets/images/."
echo "$swapped slot(s) switched from placeholder to real photograph."
echo "Check the names against docs/SHOT-LIST.md, then commit and push."
echo
if ! command -v cwebp >/dev/null 2>&1; then
  echo "cwebp was not installed, so no WebP files were written."
  echo "The site works fine on JPEG alone. See tools/README.md to switch WebP on."
fi
