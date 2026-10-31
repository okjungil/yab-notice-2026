# 영아부 예배 안내 생성기 2026

2026년 영아부 주간 예배 안내문을 생성·저장하고 카카오톡으로 공유하는 단일 HTML 앱입니다.

---

## 🌐 GitHub Pages로 온라인 배포하기

### 1단계 — GitHub 저장소 만들기

```bash
# GitHub에서 비공개(private) 저장소를 먼저 만들어 두세요.
# 저장소 이름 예시: yab-notice-2026
git remote add origin https://github.com/<사용자명>/yab-notice-2026.git
git push -u origin main
```

### 2단계 — GitHub Pages 활성화

1. 저장소 → **Settings** → **Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` / **Folder**: `/docs`
4. Save

잠시 후 `https://<사용자명>.github.io/yab-notice-2026/` 로 접속 가능합니다.

### 3단계 — 비밀번호 변경 (선택)

기본 비밀번호는 **`yab2026`** 입니다.

변경하려면:
```bash
# 새 비밀번호의 SHA-256 해시 계산
echo -n "새비밀번호" | sha256sum

# scripts/inject_gate.py 상단의 PW_HASH 값을 교체 후 재실행
python3 scripts/inject_gate.py
git add docs/index.html && git commit -m "chore: rotate site password" && git push
```

또는 GitHub Actions secret `PW_HASH` 에 해시값을 저장하면 push 할 때마다 자동 적용됩니다.

---

## 📂 파일 구조

```
output/영아부_예배안내_생성기.html   ← 원본 (패스워드 게이트 없음, 로컬 편집용)
docs/index.html                      ← 배포본 (패스워드 게이트 포함, GitHub Pages 서빙)
scripts/inject_gate.py               ← 원본 → 배포본 변환 스크립트
.github/workflows/pages.yml          ← push 시 자동 배포 워크플로우
```

---

## 🔑 접근 권한 관리

| 방법 | 설명 |
|------|------|
| 비밀번호 공유 | 허용된 사람에게만 `yab2026` (또는 변경한 비밀번호) 전달 |
| 저장소를 private으로 | 소스 코드 노출 방지 (Pages는 public URL 유지) |
| 비밀번호 교체 | 인원 변경 시 위 3단계 절차로 즉시 교체 |

비밀번호는 `sessionStorage` 에만 유지되므로 브라우저 탭을 닫으면 재입력이 필요합니다.

---

## ✨ 주요 기능

- **날짜 선택** → 예배 안내문 자동 생성
- **💾 저장 이력** 탭 — 생성한 안내문을 일자별로 저장·재조회·복사
- **✏️ 일정 편집** — 월별 주차 데이터 직접 수정
- **📝 공지 양식 편집** — 항목 라벨·순서·변수 커스터마이징
- **HWP 업로드** — 새 일정표 HWP 파일로 전체 데이터 교체
- **카카오톡 복사** — 완성된 안내문 원클릭 복사
