# 02 · UI/UX — 영어 빙고 (Lovable 디자인 적용)

> ui-ux-pro-max/SKILL.md + design-md/lovable/DESIGN.md 적용.

## 브랜드 선택
- **Lovable** — 따뜻한 cream (#f7f4ed) 배경, 거의 검정에 가까운 charcoal (#1c1c1c) 텍스트.
  교실용 도구에 맞는 접근가능하고 인쇄 친화적 톤. 채도 없는 팔레트는 인쇄 시 잉크 절약.

## 색·타이포
- `--bg: #f7f4ed` (cream paper)
- `--ink: #1c1c1c` (charcoal)
- `--muted: #5f5f5d`
- `--line: #eceae4` (warm divider)
- `--strong-line: rgba(28,28,28,0.4)`
- `--soft: rgba(28,28,28,0.04)` (hover)
- `--ring: rgba(59,130,246,0.5)` (focus)
- `--accent: #c6532b` (BINGO 라인 강조 — Lovable 톤에 어울리는 따뜻한 적갈색, AA 통과)
- 폰트: system-ui, "Helvetica Neue", Arial — 외부 폰트 의존 0. Camera Plain Variable는 라이선스 이슈로 system fallback 사용 (Lovable 가이드도 fallback 명시).

## 타이포 스케일
| 역할 | 크기 | 두께 | LH | 자간 |
|---|---|---|---|---|
| Hero | 40px | 600 | 1.10 | -1.0px |
| Section | 24px | 600 | 1.20 | -0.5px |
| Body | 16px | 400 | 1.50 | normal |
| Caption | 13px | 400 | 1.50 | normal |
| Bingo cell (4x4) | 28px | 600 | 1.10 | -0.4px |
| Bingo cell (5x5) | 22px | 600 | 1.10 | -0.3px |
| Caller word | 96px | 600 | 1.00 | -2px (메인 호명) |

## 화면 구조
```
┌──────────────────────────────────────────────────────────┐
│  Header: 로고/제목 (좌) · 보드 토글 4x4/5x5 (우)         │
├──────────────────────────────────────────────────────────┤
│  ┌─ Settings (좌, ~360px) ─┐  ┌─ Caller Panel (우) ──┐ │
│  │ • 단어 풀 textarea       │  │ ┌─ Big Word Card ─┐  │ │
│  │ • 단어 개수 카운트       │  │ │  apple          │  │ │
│  │ • [샘플 단어 불러오기]   │  │ │  사과 (toggle)  │  │ │
│  │ • [한글 의미] textarea   │  │ └──────────────────┘ │ │
│  │ • TTS rate slider        │  │  ◉ 다음 단어 (Space)  │ │
│  │ • TTS voice select       │  │  ↺ 다시 듣기          │ │
│  │ • [인쇄 미리보기]        │  │  ↶ 처음으로           │ │
│  └──────────────────────────┘  └───────────────────────┘ │
│                                                          │
│  ┌─ Student Board Preview ───────────────────────────┐  │
│  │  [Bingo 5x5 grid, 각 칸 클릭 토글]               │  │
│  │  ╔════╦════╦════╦════╦════╗                       │  │
│  │  ║apple║book║...                                  │  │
│  │  ║       ...                                       │  │
│  │  ╚════╩════╩════╩════╩════╝                       │  │
│  │  빙고 라인: 0  ·  [다른 판]                       │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 주요 컴포넌트

### 1. Big Word Card (Caller)
- 배경: cream
- 보더: 1px solid var(--line)
- radius: 16px
- padding: 56px 32px
- 영어 단어: 96px, weight 600, 자간 -2px, charcoal
- 한글 뜻: 28px, weight 400, muted gray, 토글 버튼으로 숨김
- TTS 발화 중 미세한 인셋 그림자 깜빡임 (active state)

### 2. Button — Primary Dark (호명/다음 단어)
- bg: #1c1c1c, color: #fcfbf8
- padding: 10px 18px, radius: 6px
- 인셋 shadow: `rgba(255,255,255,0.2) 0 .5px 0 0 inset, rgba(0,0,0,0.2) 0 0 0 .5px inset, rgba(0,0,0,0.05) 0 1px 2px 0`
- :hover opacity 0.9, :active 0.8

### 3. Button — Ghost (인쇄, 다른 판)
- bg: transparent, border: 1px solid var(--strong-line)
- radius: 6px

### 4. Bingo Cell
- 정사각형 (aspect-ratio: 1)
- 기본: bg cream, border 1px solid var(--line)
- :hover: bg var(--soft)
- :active/:focus: outline 2px var(--ring)
- 마크된 상태(`.marked`): 배경 cream 유지, 단어 위에 대각 X 또는 두꺼운 underline + opacity 0.45
  → 단어를 가리지 않고 표시
- 라인 완성 칸: 색 var(--accent) 두꺼운 outline (3px), opacity 0.85

### 5. 사이드 패널 (Settings)
- bg cream, padding 24px, border 1px solid var(--line), radius 12px
- textarea: bg cream, border 1px solid var(--line), radius 6px, padding 12px, monospace 14px

## 접근성
- 모든 인터랙티브 요소 키보드 도달 (Tab/Shift+Tab)
- 호명 버튼: `Space` 단축키. 다시 듣기: `R`. 처음으로: `Esc`(확인 후).
- aria-label: 빙고 칸 → `aria-label="apple, marked"` / `aria-pressed`로 토글 상태
- 호명 단어 변경 시 `aria-live="polite"`로 스크린 리더에 알림
- 대비: charcoal(#1c1c1c) on cream(#f7f4ed) ≈ 16.7:1 (AAA)
- focus state: `box-shadow: 0 0 0 2px var(--ring)` (sharp outline은 Lovable 권고는 soft지만 인쇄·교실 환경에선 명확함 우선)

## 인쇄 (`@media print`)
- settings, caller panel, header 숨김
- 보드만 표시, 페이지 가운데 정렬
- 배경 cream → 흰색으로 (잉크 절약)
- 칸 border 진하게 (#000)
- "옵션: 한 페이지에 2판" 토글 시 grid-template-columns: 1fr 1fr; 페이지 분할 처리

## design.md ↔ ui-ux-pro-max 충돌 해소
- Lovable의 "no sharp focus outlines" → 교실용 도구이므로 명확성 우선, 디자인 → 가이드 우선 원칙 따라 sharp outline 유지.
- 외 모든 색·타이포·radius는 Lovable 가이드 그대로.
