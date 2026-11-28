#!/usr/bin/env bash
# 턴 종료 처리 한 번에: 빌드 → (선택) 검증 → 커밋·푸시
# 사용: bash tools/turn_end.sh "커밋 메시지" [--verify]
set -e
cd "$(dirname "$0")/.."
python3 tools/build_org.py | tail -1
if [ "$2" = "--verify" ]; then node tools/verify_console.js 2>&1 | tail -1; fi
git add -A
git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || true
git push -q origin HEAD && echo pushed
