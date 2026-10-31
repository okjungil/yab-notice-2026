#!/bin/bash
# 새 GitHub PAT를 받아 모든 설정에 적용하는 스크립트
# 사용법: bash scripts/apply_new_token.sh <새_PAT>
set -e

NEW_PAT="$1"
REPO="okjungil/yab-notice-2026"

if [ -z "$NEW_PAT" ]; then
  echo "사용법: bash scripts/apply_new_token.sh <GitHub_PAT>"
  exit 1
fi

echo "1) git remote URL 업데이트..."
git remote set-url origin "https://okjungil:${NEW_PAT}@github.com/${REPO}.git"

echo "2) 토큰 유효성 확인..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token ${NEW_PAT}" "https://api.github.com/user")
if [ "$STATUS" != "200" ]; then
  echo "❌ 토큰 유효하지 않음 (HTTP $STATUS)"
  exit 1
fi
echo "✅ 토큰 유효"

echo "3) docs/index.html 재빌드..."
PW_HASH="b85c65c827d834bb6e24fad6dde064ca12f2134f7334bdec269500619dd5ab08" \
GH_TOKEN="${NEW_PAT}" \
GH_REPO="${REPO}" \
python3 scripts/inject_gate.py

echo "4) GitHub Secrets 업데이트..."
# 공개키 가져오기
PUB_KEY_RESP=$(curl -s -H "Authorization: token ${NEW_PAT}" "https://api.github.com/repos/${REPO}/actions/secrets/public-key")
KEY_ID=$(echo "$PUB_KEY_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['key_id'])")
PUB_KEY=$(echo "$PUB_KEY_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['key'])")

# 시크릿 암호화 및 등록
ENCRYPTED=$(python3 -c "
import base64
from nacl import encoding, public
pk = public.PublicKey('${PUB_KEY}'.encode(), encoding.Base64Encoder())
box = public.SealedBox(pk)
enc = box.encrypt('${NEW_PAT}'.encode())
print(base64.b64encode(enc).decode())
")
curl -s -X PUT -H "Authorization: token ${NEW_PAT}" -H "Content-Type: application/json" \
  "https://api.github.com/repos/${REPO}/actions/secrets/GH_DATA_TOKEN" \
  -d "{\"encrypted_value\":\"${ENCRYPTED}\",\"key_id\":\"${KEY_ID}\"}" > /dev/null
echo "✅ GH_DATA_TOKEN 시크릿 등록됨"

echo "5) 커밋 및 push..."
git add docs/index.html
git diff --staged --quiet || git commit -m "fix: apply new PAT for GitHub sync"
git push origin feat/infant-dept-worship-notice-generator

echo "6) main에 merge..."
curl -s -X POST -H "Authorization: token ${NEW_PAT}" -H "Content-Type: application/json" \
  "https://api.github.com/repos/${REPO}/merges" \
  -d '{"base":"main","head":"feat/infant-dept-worship-notice-generator","commit_message":"fix: apply new PAT for GitHub sync"}' | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('Merge SHA:', d.get('sha','ERROR')[:12] if 'sha' in d else d)"

echo ""
echo "✅ 완료! GitHub Actions가 자동 배포합니다."
echo "배포 URL: https://okjungil.github.io/yab-notice-2026/"
