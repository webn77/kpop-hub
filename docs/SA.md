# SA.md — System Architecture

## 전체 시스템 구조

```
사용자 브라우저
      │
      │ HTTP Request
      ▼
┌─────────────────────────────────────┐
│         Django 5.x (웹 서버)         │
│                                     │
│  URL Router (urls.py)               │
│       │                             │
│       ▼                             │
│  Middleware Layer                   │
│  - 인증 검사 (django-allauth)        │
│  - CSRF 방어                        │
│  - Rate Limiting                    │
│       │                             │
│       ▼                             │
│  Views (views.py)                   │
│  - accounts / notices / posts       │
│  - events / polls / admin_dashboard │
│       │                             │
│       ▼                             │
│  Models (models.py) ──── ORM ────▶ SQLite DB │
│       │                             │
│       ▼                             │
│  Templates (.html)                  │
│  - Tailwind CSS                     │
│  - HTMX (비동기 인터랙션)            │
└─────────────────────────────────────┘
      │
      │ HTTP Response (HTML)
      ▼
사용자 브라우저
```

## 데이터 플로우

### 1. 게시글 작성 플로우
```
사용자 → 글쓰기 폼 제출
       → CSRF 검증
       → 로그인 상태 확인
       → posts/views.py PostCreateView
       → Post 모델 저장 (이미지 → media/)
       → 게시글 상세 페이지로 리다이렉트
```

### 2. 좋아요 플로우 (HTMX)
```
사용자 → 좋아요 버튼 클릭
       → HTMX hx-post="/posts/1/like/"
       → PostLikeView (토글 처리)
       → 좋아요 수 HTML 조각만 반환
       → HTMX가 해당 요소만 교체 (페이지 새로고침 없음)
```

### 3. 인증 플로우
```
사용자 → /login 접속
       → django-allauth LoginView
       → 이메일/비밀번호 검증
       → 세션 생성
       → 메인 페이지 리다이렉트
```

### 4. 관리자 플로우
```
관리자 → /admin 접속
       → Django Admin 인증
       → is_staff=True 확인
       → 회원/게시글/공지사항 관리 UI
```

## URL 구조

| URL | 앱 | 설명 |
|---|---|---|
| / | posts | 메인 (게시글 목록) |
| /accounts/login/ | accounts | 로그인 |
| /accounts/signup/ | accounts | 회원가입 |
| /accounts/logout/ | accounts | 로그아웃 |
| /notices/ | notices | 공지사항 목록 |
| /posts/ | posts | 자유게시판 |
| /posts/create/ | posts | 글쓰기 |
| /posts/<id>/ | posts | 게시글 상세 |
| /posts/<id>/like/ | posts | 좋아요 (HTMX) |
| /events/ | events | 일정 캘린더 |
| /polls/ | polls | 투표 목록 |
| /admin/ | Django Admin | 관리자 |

## 배포 구조 (개발 단계)

```
로컬 개발 환경
├── python manage.py runserver  (포트 8000)
├── SQLite (db.sqlite3)
└── media/ (업로드 이미지)
```
