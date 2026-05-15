# KPOP HUB — K-POP 팬 커뮤니티

## 프로젝트 비전

K-POP 팬들이 정보를 잃지 않고, 가볍고 빠르게 소통할 수 있는 커뮤니티 플랫폼.
카카오톡처럼 즉각적이고, 네이버 카페보다 단순하며, 스레드보다 오래 남는 공간.

## 기술 스택

| 영역 | 기술 | 이유 |
|---|---|---|
| 백엔드 | Django 5.2.4 (LTS) | 보안·인증·관리자 내장, AI 코드 생성 정확도 최고 |
| 데이터베이스 | SQLite → PostgreSQL 이전 가능 | 가볍게 시작 |
| 프론트엔드 | Django Templates | 서버 렌더링, 상태관리 불필요 |
| 스타일 | Tailwind CSS | 모바일 우선 반응형 |
| 인터랙션 | HTMX | React 없이 좋아요·댓글 비동기 |
| 관리자 | Django Admin | 대시보드 80% 자동 완성 |
| 인증 | django-allauth | 세션·JWT·소셜 로그인 통합 |

## 프로젝트 구조

```
kpop_hub/
├── manage.py
├── requirements.txt
├── config/                  # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # 인증
├── notices/                 # 공지사항
├── posts/                   # 소통공간/자유게시판
├── events/                  # 주요일정
├── polls/                   # 투표
├── surveys/                 # 설문조사
├── admin_dashboard/         # 관리자 대시보드
├── templates/               # 공용 템플릿
├── static/                  # 정적 파일
├── media/                   # 업로드 이미지
├── docs/                    # 기획 문서
└── logs/                    # 작업 로그
```

## 개발 로드맵

| 단계 | 내용 | 상태 |
|---|---|---|
| Phase 1 | 프로젝트 세팅 + 기본 구조 | 예정 |
| Phase 2 | 회원가입/로그인 (accounts) | 예정 |
| Phase 3 | 공지사항 + 소통공간 (notices, posts) | 예정 |
| Phase 4 | 일정 + 투표 (events, polls) | 예정 |
| Phase 5 | 관리자 대시보드 완성 | 예정 |

## 빠른 시작

```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

접속: http://127.0.0.1:8000
