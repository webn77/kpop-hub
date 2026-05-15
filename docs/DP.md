# DP.md — Design Principles

## UI/UX 철학

### 핵심 원칙 3가지
1. **모바일 퍼스트** — 모든 UI는 375px 기준으로 먼저 설계
2. **미니멀리즘** — 불필요한 요소 제거, 콘텐츠 중심
3. **터치 최적화** — 버튼 최소 44px, 탭 영역 충분히 확보

## 색상 시스템

| 용도 | 색상 | Tailwind 클래스 |
|---|---|---|
| 브랜드 메인 | 보라 #7C3AED | `bg-violet-600` |
| 브랜드 보조 | 핑크 #EC4899 | `bg-pink-500` |
| 배경 | 흰색 #FFFFFF | `bg-white` |
| 텍스트 기본 | 회색 #111827 | `text-gray-900` |
| 텍스트 보조 | 회색 #6B7280 | `text-gray-500` |
| 경계선 | 회색 #E5E7EB | `border-gray-200` |
| 좋아요 | 빨강 #EF4444 | `text-red-500` |

## 컴포넌트 가이드

### 버튼

```html
<!-- 기본 버튼 -->
<button class="bg-violet-600 text-white px-4 py-2 rounded-lg hover:bg-violet-700">
  제출
</button>

<!-- 보조 버튼 -->
<button class="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg">
  취소
</button>
```

### 카드 (게시글)

```html
<div class="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
  <!-- 게시글 내용 -->
</div>
```

### 네비게이션 바

```html
<nav class="fixed top-0 w-full bg-white border-b border-gray-200 z-50">
  <!-- 로고 + 메뉴 + 로그인/로그아웃 -->
</nav>
```

## 레이아웃 규칙

- 최대 너비: `max-w-2xl mx-auto` (모바일 중심)
- 여백: `px-4 py-6` 기본
- 카드 간격: `space-y-4`
- 반응형 그리드: `grid grid-cols-1 md:grid-cols-2`

## HTMX 인터랙션 패턴

```html
<!-- 좋아요 버튼 (페이지 새로고침 없이 동작) -->
<button hx-post="/posts/1/like/"
        hx-target="#like-count"
        hx-swap="outerHTML"
        class="text-gray-400 hover:text-red-500">
  ❤ <span id="like-count">12</span>
</button>
```

## 제약사항

- JavaScript 라이브러리 추가 최소화 (HTMX만 사용)
- 이미지 업로드 최대 5MB
- 댓글 최대 2depth (댓글 + 대댓글)
- 모바일에서 사이드바 없음 (하단 네비게이션)
