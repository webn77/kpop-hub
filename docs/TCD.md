# TCD.md — Technical Context Document

## 코딩 철학

### Django Way 원칙
- **Convention over Configuration** — Django 기본 규칙을 따른다. 임의 구조 금지
- **DRY (Don't Repeat Yourself)** — 반복 로직은 반드시 추상화
- **Fat Model, Thin View** — 비즈니스 로직은 Model에, View는 요청/응답만 처리
- **Django ORM 우선** — Raw SQL 사용 최소화

### 바이브 코딩 원칙
- 한 번에 하나의 기능만 구현
- 동작 확인 후 다음 단계 진행
- 에러 발생 시 원인 분석 후 수정 요청

## 기술 스택 선택 근거

### 왜 Django인가
1. Python 기반 → AI 코드 생성 정확도 최고
2. 인증·세션·CSRF·XSS 방어 기본 탑재
3. Django Admin → 관리자 대시보드 즉시 사용 가능
4. django-allauth → 소셜 로그인까지 확장 가능

### 왜 HTMX인가
- React/Vue 없이 SPA 수준의 인터랙션 구현
- `hx-post="/like/"` 속성 하나로 페이지 새로고침 없이 좋아요 동작
- Django Templates와 자연스럽게 통합

### 왜 SQLite인가
- 개발 단계에서 별도 DB 서버 불필요
- WAL 모드 활성화로 동시성 문제 해결
- 추후 PostgreSQL 마이그레이션 1줄 변경으로 가능

## 보안 패턴

| 위협 | 방어 방법 |
|---|---|
| XSS | Django Templates 자동 이스케이프 |
| CSRF | Django CSRF 미들웨어 기본 활성화 |
| SQL Injection | Django ORM 사용 (Raw SQL 금지) |
| 비밀번호 | bcrypt 해시 (Django 기본) |
| Rate Limiting | django-ratelimit 적용 |

## SQLite 성능 최적화 설정

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'init_command': (
                'PRAGMA journal_mode=WAL;'
                'PRAGMA synchronous=NORMAL;'
                'PRAGMA foreign_keys=ON;'
            ),
        },
    }
}
```

## 앱 구조 패턴

각 Django 앱은 아래 구조를 따른다:

```
앱명/
├── models.py      # 데이터 모델 + 비즈니스 로직
├── views.py       # 요청/응답 처리
├── urls.py        # URL 라우팅
├── forms.py       # Form 클래스
├── admin.py       # Admin 등록
└── templates/앱명/  # 템플릿
```
