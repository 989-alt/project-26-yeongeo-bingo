# Day 26 · 영어 빙고 — 단어 음성

> 100-vibecoding-topics.md #026

## 토픽 요약
- **주제**: 4x4 / 5x5 빙고판을 학생이 직접 채우고, 교사가 단어를 음성으로 호명. 듣기·읽기 동시 훈련.
- **대상**: 초등 3~6학년 (영어)
- **환경**: 교실 TV (교사용 호명 화면) + 학생 1:1 또는 종이 빙고판

## 포함 기능 (원 토픽)
1. 단어 풀 입력 → 학생용 무작위 빙고판 인쇄
2. 호명 모드(TTS, 사용 단어 체크)
3. 자동 BINGO 감지 (학생 자가체크)

## 배제 기능 (원 토픽)
- 학생 결과 수집, 사진 업로드

## 기술 스택 결정
- **단일 HTML + vanilla CSS/JS** (단순 토픽, CDN 의존 최소화)
- Web Speech API (`speechSynthesis`) — 호명 TTS
- `@media print` — 종이 빙고판 인쇄
- localStorage — 단어 풀, 빙고판 보존(휘발성 OK이지만 새로고침 사고 방지)
- **Gemini 미사용** (이 토픽에 AI 호출 불필요)

## 디자인
- DESIGN.md: **Lovable** (warm cream 배경, Charcoal text, opacity 기반 그레이, 둥근 모서리)
- 보조 참조: Pinterest (gallery grid 감각만 차용)

## 비기능 요구
- 대비 4.5:1 이상
- 키보드 only 조작 가능 (호명/다음/이전)
- TTS 미지원 브라우저 대비 fallback (큰 글씨 표시)
- 인쇄: A4 1장에 빙고판 1~4개
