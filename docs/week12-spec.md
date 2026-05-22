# Week 12 구현 스펙
<!-- v1.1 | 2026-05-22 | 코드 검증 + Advisor 리뷰 반영 -->

## 현황 요약

| 앱 | 상태 | 코드 검증 결과 |
|----|------|--------------|
| notices | ✅ 구현 완료 | 브라우저 테스트 필요 |
| posts | ✅ 구현 완료 | 버그 2건 수정 필요 |
| events | ✅ 구현 완료 | 브라우저 테스트 필요 |
| polls | ✅ 구현 완료 | 브라우저 테스트 필요 |
| accounts (프로필) | ✅ 본인 편집 구현 | 타인 프로필 조회 미구현 |
| surveys | ❌ 미구현 | 전체 신규 구현 |
| search | ❌ 미구현 | 전체 신규 구현 |

---

## Group 1 — 공지사항 + 소통공간

### 1-A. 공지사항 (notices)

**인수 조건:**
- [ ] `/notices/` 목록 — 핀 고정 상단, 최신순, 페이지네이션 10개
- [ ] `/notices/<id>/` 상세 — 제목/내용/작성일 표시
- [ ] `/notices/new/` — staff/ADMIN만 접근, 비허가 시 403
- [ ] 수정/삭제 버튼 — 관리자에게만 노출
- [ ] 중요 공지 빨간 배지 표시

---

### 1-B. 소통공간 — 자유게시판 (posts)

**코드 검증 결과 (posts/views.py):**
| 기능 | 코드 존재 | 이슈 |
|------|----------|------|
| HTMX 댓글 작성 | ✅ | - |
| 대댓글 parent 처리 | ✅ | - |
| 비로그인 차단 LoginRequired | ✅ | - |
| 댓글 삭제 본인만 | ⚠️ | **silent fail — 403 미반환, 수정 필요** |
| 게시글 목록 페이지네이션 | ⚠️ | **paginate_by=10, 스펙은 15 — 수정 필요** |

**수정 태스크:**
- [ ] `CommentDeleteView`: 본인 아닌 경우 `HttpResponseForbidden(403)` 반환
- [ ] `PostListView.paginate_by`: 10 → 15

**인수 조건:**
- [ ] 게시글 목록 — 제목/작성자/좋아요수/댓글수/조회수/작성일, 15개씩
- [ ] 게시글 상세 — 조회수 자동 증가 (매 요청마다 +1)
- [ ] 좋아요 — HTMX 실시간 토글, 중복 방지, 취소 가능
- [ ] 댓글 작성 — 로그인 필수, HTMX 새로고침 없이 트리에 즉시 추가
- [ ] 대댓글 — "답글" 클릭 시 parent 폼 노출, 들여쓰기 표시
- [ ] 본인 댓글에만 [삭제] 버튼 노출
- [ ] 타인 댓글 삭제 POST 시 403 반환
- [ ] 비로그인 사용자에게 댓글 폼 미노출

---

## Group 2 — 설문조사 + 검색 + 프로필

### 2-A. 설문조사 (surveys) — 신규 구현

**모델:**
```python
Survey(title, description, is_anonymous, expires_at, created_by)
Question(survey, text, question_type, required, options)
  # question_type: TEXT / TEXTAREA / CHOICE / MULTIPLE / SCALE(1-5)
Response(survey, respondent, submitted_at)
Answer(response, question, answer_text)
```

**인수 조건:**
- [ ] `/surveys/` 목록 — 진행중/완료 구분, 제목/질문수/응답자수
- [ ] `/surveys/<id>/respond/` — 질문 타입별 폼, 필수 질문 체크, 로그인 필수
- [ ] `/surveys/new/` — 관리자만, 동적 질문 추가/삭제 (JS)
- [ ] `/surveys/<id>/results/` — 관리자만, 질문별 통계
  - 객관식: 선택지별 비율 + CSS 막대 그래프
  - 주관식: 답변 목록
  - 척도: 평균 점수
- [ ] `/surveys/<id>/results/<response_id>/` — **개인별 응답 상세** (구글 설문지 스타일)
- [ ] 중복 응답 방지 (1인 1회)

**생성 파일:**
- `surveys/models.py` — 4개 모델
- `surveys/views.py` — 5개 뷰
- `surveys/forms.py`
- `surveys/urls.py`
- `templates/surveys/list.html`
- `templates/surveys/respond.html`
- `templates/surveys/create.html`
- `templates/surveys/results.html`
- `templates/surveys/response_detail.html`

---

### 2-B. 검색 (search) — 신규 구현

**범위 확정:** 키워드 검색만 (필터링 제외 — 수업 범위 밖)

**인수 조건:**
- [ ] `/search/` — 검색창 + 버튼 UI
- [ ] 키워드로 공지사항(title, content) + 게시글(title, content) 동시 검색
- [ ] 결과 리스트 — 각 항목 해당 페이지 링크
- [ ] 검색어 없이 제출 시 빈 결과 표시

**생성 파일:**
- `config/urls.py` — search path 추가
- `posts/views.py` — SearchView 추가
- `templates/search/search.html`

---

### 2-C. 사용자 프로필 (accounts)

**현황:** `/accounts/profile/` 본인 조회+편집 구현됨. 타인 프로필 조회 미구현.

**인수 조건:**
- [ ] `/accounts/profile/` — 로그인 사용자 본인 프로필 + 수정 폼
- [ ] 아바타/닉네임 변경 저장

> 타인 프로필 조회(`/profile/<nickname>/`)는 PDF 10페이지 요구사항이나, 기말 제출 우선순위상 선택 구현.

---

## TDD 계획

각 Group은 **테스트 작성 → 구현 → 테스트 통과** 순서로 진행.

### Group 1 테스트 케이스
```
test_comment_delete_by_other_user_returns_403
test_comment_delete_by_owner_succeeds
test_post_list_paginate_by_15
test_like_toggle
test_notice_create_by_staff_only
```

### Group 2 테스트 케이스
```
test_survey_respond_once_per_user
test_survey_results_admin_only
test_search_returns_matching_posts
test_search_returns_matching_notices
test_search_empty_query_returns_empty
```

---

## 완료 기준

- [ ] Group 1 수정 2건 반영 + 인수 조건 전체 통과
- [ ] Group 2 설문조사 응답/결과/개인별 결과 동작
- [ ] Group 2 검색 키워드 결과 정상 노출
- [ ] 테스트 전체 PASS
- [ ] git push 완료
