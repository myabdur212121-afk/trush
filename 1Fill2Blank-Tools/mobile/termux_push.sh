#!/data/data/com.termux/files/usr/bin/env bash
# Upload THIS standalone package to a NEW, EMPTY GitHub repository from Termux.
#
# Why this exists: the package owner mainly uses a phone.  This script keeps
# any GitHub credential on that phone; it never asks anyone to paste a token
# into a chat, a file, or a repository URL.
#
# First create an empty GitHub repository (no README, .gitignore or licence),
# then run from the package root:
#   bash mobile/termux_push.sh

set -Eeuo pipefail

cd -- "$(dirname -- "$0")/.."
PACKAGE_ROOT="$(pwd -P)"

if ! command -v git >/dev/null 2>&1; then
  echo "Git পাওয়া যায়নি — Termux-এ install করা হচ্ছে..."
  if command -v pkg >/dev/null 2>&1; then
    pkg update -y
    pkg install -y git
  else
    echo "দুঃখিত: এই script টি Termux-এর pkg ছাড়া Git install করতে পারবে না।" >&2
    exit 1
  fi
fi

EXISTING_ROOT=""
if EXISTING_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  if [ "$EXISTING_ROOT" != "$PACKAGE_ROOT" ]; then
    cat >&2 <<'MSG'
এই package টি এখন অন্য আরেকটি Git repository-এর ভেতরে আছে।
এখানে নতুন repository শুরু করা হবে না।
আলাদা repo হিসেবে তুলতে package টি repo-র বাইরে রেখে আবার চালাও।
MSG
    exit 4
  fi
else
  git init -b main
fi

if ! git config user.name >/dev/null 2>&1; then
  printf 'Git-এ দেখানোর নাম লিখো: '
  IFS= read -r GIT_NAME
  [ -n "$GIT_NAME" ] || { echo "নাম খালি রাখা যাবে না।" >&2; exit 2; }
  git config user.name "$GIT_NAME"
fi

if ! git config user.email >/dev/null 2>&1; then
  printf 'Git-এ ব্যবহারের email লিখো: '
  IFS= read -r GIT_EMAIL
  [ -n "$GIT_EMAIL" ] || { echo "Email খালি রাখা যাবে না।" >&2; exit 2; }
  git config user.email "$GIT_EMAIL"
fi

printf 'নতুন খালি GitHub repo-র HTTPS URL দাও (token ছাড়া পরিষ্কার URL): '
IFS= read -r REPO_URL

case "$REPO_URL" in
  *ghp_*|*github_pat_*|*x-access-token:*|https://*@github.com/*)
    echo "STOP: URL-এর ভেতরে token থাকতে পারে। শুধু https://github.com/USER/REPO.git ধরনের URL দাও।" >&2
    exit 2
    ;;
  https://github.com/*)
    ;;
  *)
    echo "শুধু https://github.com/USER/REPO.git ধরনের URL গ্রহণ করা হবে।" >&2
    exit 2
    ;;
esac

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

# A first upload should go to an empty, unrelated remote. If this folder has
# no commit yet but the remote already has one, stop instead of creating a
# confusing unrelated-history push from a phone.
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  if git ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
    cat >&2 <<'MSG'
এই remote repository খালি নয়।
প্রথম upload-এর জন্য README/.gitignore ছাড়া তৈরি করা সম্পূর্ণ খালি repo ব্যবহার করো,
অথবা বিদ্যমান repo clone করে তার ভেতরে এই folder copy করার পদ্ধতি অনুসরণ করো।
MSG
    exit 3
  fi
fi

git add .

echo
echo "--- Commit-এর আগে file তালিকা ---"
git status --short

if git diff --cached --quiet; then
  echo "নতুন কোনো পরিবর্তন নেই; commit করা হচ্ছে না।"
else
  printf 'Commit message [Add 1Fill2Blank audio-video tools]: '
  IFS= read -r COMMIT_MESSAGE
  COMMIT_MESSAGE="${COMMIT_MESSAGE:-Add 1Fill2Blank audio-video tools}"
  git commit -m "$COMMIT_MESSAGE"
fi

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  echo "বর্তমান branch বোঝা যাচ্ছে না; push থামানো হলো।" >&2
  exit 5
fi

cat <<'MSG'

এবার GitHub login চাইতে পারে।
- Username: তোমার GitHub username দাও।
- Password: account password নয়; নিজের ফোনেই একটি fine-grained token ব্যবহার করো।
- Token কখনো chat, file, screenshot বা repo URL-এ রাখবে না।
MSG
printf 'Push করতে চাও? [y/N]: '
IFS= read -r ANSWER
case "$ANSWER" in
  y|Y|yes|YES) ;;
  *) echo "Push বাতিল করা হলো। Local commit এখানেই আছে।"; exit 0 ;;
esac

git push -u origin "$BRANCH"
echo "হয়ে গেছে: $BRANCH branch GitHub-এ push করা হয়েছে।"
