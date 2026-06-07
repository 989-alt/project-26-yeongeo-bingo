# 03 · Tester Cycle 1 — Bug Report

> webapp-testing/SKILL.md 적용. Playwright headless chromium.

## 시나리오
1. 페이지 로드 → 보드 25칸 (5x5)
2. 4x4 전환 → 16칸
3. 5x5 복귀 → 0행 5칸 마킹 → 빙고 라인 = 1
4. 다음 단어 클릭 → 호명 카운터 1, 단어 카드 표시
5. 다시 듣기 → 같은 단어 유지
6. 3회 추가 호명 → 카운터 4
7. 처음으로 → 카운터 0, 빈 카드 표시
8. 인쇄 → 2판 빌드, window.print() 호출
9. console error / pageerror 0

## 결과
- **모든 15개 검증 통과**.
- console error 0, pageerror 0.
- TTS 호출은 헤드리스 환경에서 silent (정상 — speakWord 내 try/catch).

## 종료 조건
- P0·P1 버그 0건
- e2e 1개 (tests/e2e.py) 0 fail
→ Ralph loop 1사이클로 종료, 배포 진행.

스크린샷: `tests/artifacts/` (01_home, 02_4x4, 03_bingo, 04_caller, final_5x5, final_4x4 PNG)
