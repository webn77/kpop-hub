# CBP.md — Coding Best Practices

## 개발 표준

### 네이밍 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 모델 클래스 | PascalCase | `Post`, `Comment`, `UserProfile` |
| 변수/함수 | snake_case | `get_post_list`, `user_profile` |
| URL name | kebab-case | `post-detail`, `comment-create` |
| 템플릿 | snake_case.html | `post_detail.html` |
| CSS 클래스 | Tailwind 유틸리티 | `bg-violet-600 text-white` |

### 금지 사항
- Raw SQL 사용 금지 → Django ORM 사용
- `print()` 디버깅 금지 → `logging` 모듈 사용
- 하드코딩된 URL 금지 → `{% url 'name' %}` 사용
- 기존 코드 삭제 금지
- 중복 코드 작성 금지

## 바이브 코딩 워크플로우

```
1. 기능 요청 작성
       ↓
2. Claude Code에 전달
       ↓
3. 코드 생성 확인
       ↓
4. 서버 재시작 (python manage.py runserver)
       ↓
5. 브라우저에서 동작 확인
       ↓
6. 에러 발생 시 에러 메시지 복사 → Claude Code에 전달
       ↓
7. 다음 기능으로 이동
```

## 커밋 규칙

```
feat: 공지사항 CRUD 구현
fix: 댓글 삭제 권한 오류 수정
style: 게시판 카드 UI 개선
docs: PRD 업데이트
```

## 작업 완료 후 필수 문서화

작업이 끝나면 반드시 `logs/` 폴더에 기록:

```
logs/
├── YYYYMMDD_tasks.md   # 업무 보고서
└── YYYYMMDD_logs.md    # 업무 일기
```

### tasks.md 템플릿
```markdown
## [날짜] - [작업 제목]
- 담당자: [이름/AI]
- 소요시간: [예상 vs 실제]
- 구현 기능: [상세 설명]
- 테스트 결과: [통과한 테스트 수/전체]
- 배운 점: [새로 알게 된 것]
- 어려웠던 점: [막혔던 부분과 해결 과정]
- 다음 작업: [후속 작업]
```

## 막혔을 때 대응 순서

1. 에러 메시지 전체 복사
2. Claude Code에 "이 에러 수정해줘" + 에러 메시지 전달
3. `docs/troubleshooting.md`에 문제/해결 기록
4. 기존 유사 구현 패턴 참고
