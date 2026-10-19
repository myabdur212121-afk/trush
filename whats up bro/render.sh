#!/usr/bin/env bash
# উদ্দেশ্য: দৃশ্য রেন্ডার করে চূড়ান্ত ভিডিও videos ফোল্ডারে রাখা,
# আর সব সাময়িক ফাইল (আংশিক ভিডিও, টেক্স, নথি) cache ফোল্ডারে রাখা।
# ব্যবহার: ./render.sh <দৃশ্যের-ফাইল.py> <দৃশ্যের-নাম> [মানের পতাকা, যেমন -ql]
# উদাহরণ: ./render.sh test_workspace.py WorkspaceTest
set -Eeuo pipefail

WORKSPACE_ROOT="/home/user"
SCENES_DIR="$WORKSPACE_ROOT/scenes"
VIDEOS_DIR="$WORKSPACE_ROOT/videos"
CACHE_DIR="$WORKSPACE_ROOT/cache"
MANIM="$WORKSPACE_ROOT/manim-sandbox-setup/bin/manim"

if [[ $# -lt 2 ]]; then
    echo "ব্যবহার: ./render.sh <দৃশ্যের-ফাইল.py> <দৃশ্যের-নাম> [মানের পতাকা]" >&2
    echo "উদাহরণ: ./render.sh test_workspace.py WorkspaceTest -ql" >&2
    exit 2
fi

SCENE_FILE="$1"
SCENE_NAME="$2"
QUALITY="${3:--ql}"

# দৃশ্যের ফাইল খোঁজা: পুরো পথ দেওয়া থাকলে সেটাই, না হলে scenes ফোল্ডারে
if [[ -f "$SCENE_FILE" ]]; then
    SCENE_PATH="$SCENE_FILE"
elif [[ -f "$SCENES_DIR/$SCENE_FILE" ]]; then
    SCENE_PATH="$SCENES_DIR/$SCENE_FILE"
else
    echo "দৃশ্যের ফাইল পাওয়া যায়নি: $SCENE_FILE" >&2
    exit 1
fi

mkdir -p -- "$VIDEOS_DIR" "$SCENES_DIR" "$CACHE_DIR/logs" "$CACHE_DIR/manim"
export PYTHONDONTWRITEBYTECODE=1
# নিজস্ব অ্যানিমেশন যাতে দৃশ্যের লেখা থেকে সরাসরি আনা যায়
export PYTHONPATH="$WORKSPACE_ROOT${PYTHONPATH:+:$PYTHONPATH}"

LOG_FILE="$CACHE_DIR/logs/${SCENE_NAME}-$(date +%Y%m%d-%H%M%S).log"
echo "রেন্ডার শুরু: $SCENE_PATH -> $SCENE_NAME ($QUALITY)"
echo "নথি: $LOG_FILE"

"$MANIM" "$QUALITY" --media_dir "$CACHE_DIR/manim" "$SCENE_PATH" "$SCENE_NAME" 2>&1 | tee "$LOG_FILE"

# চূড়ান্ত ভিডিও খোঁজা (আংশিক ফোল্ডার বাদে সবচেয়ে নতুনটি)
FINAL="$(find "$CACHE_DIR/manim" -type f -name "${SCENE_NAME}.mp4" ! -path '*/partial_movie_files/*' -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)"

if [[ -z "${FINAL:-}" || ! -s "$FINAL" ]]; then
    echo "চূড়ান্ত ভিডিও পাওয়া যায়নি। নথি দেখো: $LOG_FILE" >&2
    exit 1
fi

mv -f -- "$FINAL" "$VIDEOS_DIR/${SCENE_NAME}.mp4"
# দৃশ্যের ফোল্ডারে যাতে শুধু লেখাই থাকে
rm -rf -- "$SCENES_DIR/__pycache__"

echo "তৈরি: $VIDEOS_DIR/${SCENE_NAME}.mp4"
ls -lh "$VIDEOS_DIR/${SCENE_NAME}.mp4"
