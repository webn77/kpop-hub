# DD.md — Database Design

## 데이터베이스: SQLite (Django ORM)

## 모델 관계도

```
User (accounts)
 ├── Post (posts) — 1:N
 ├── Comment (posts) — 1:N
 ├── Like (posts) — M:N (through)
 ├── Notice (notices) — 1:N (관리자만)
 ├── Event (events) — 1:N
 └── PollVote (polls) — 1:N

Post (posts)
 └── Comment (posts) — 1:N (부모/자식 — django-mptt)

Poll (polls)
 └── PollChoice (polls) — 1:N
      └── PollVote (polls) — 1:N
```

## 모델 상세 설계

### accounts.User (CustomUser)
```python
class User(AbstractUser):
    nickname    = CharField(max_length=50, unique=True)
    profile_img = ImageField(upload_to='profiles/', blank=True)
    role        = CharField(choices=[('USER','일반'), ('ADMIN','관리자')], default='USER')
    created_at  = DateTimeField(auto_now_add=True)
```

### notices.Notice
```python
class Notice(Model):
    author      = ForeignKey(User, on_delete=CASCADE)
    title       = CharField(max_length=200)
    content     = TextField()
    is_pinned   = BooleanField(default=False)   # 상단 고정
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
```

### posts.Post
```python
class Post(Model):
    author      = ForeignKey(User, on_delete=CASCADE)
    title       = CharField(max_length=200)
    content     = TextField()
    image       = ImageField(upload_to='posts/', blank=True)
    view_count  = PositiveIntegerField(default=0)
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
```

### posts.Comment (django-mptt 계층 구조)
```python
class Comment(MPTTModel):
    post        = ForeignKey(Post, on_delete=CASCADE)
    author      = ForeignKey(User, on_delete=CASCADE)
    parent      = TreeForeignKey('self', null=True, blank=True, on_delete=CASCADE)
    content     = TextField()
    created_at  = DateTimeField(auto_now_add=True)
```

### posts.Like
```python
class Like(Model):
    user        = ForeignKey(User, on_delete=CASCADE)
    post        = ForeignKey(Post, on_delete=CASCADE)
    created_at  = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 중복 좋아요 방지
```

### events.Event
```python
class Event(Model):
    title       = CharField(max_length=200)
    description = TextField(blank=True)
    event_date  = DateField()
    event_type  = CharField(choices=[('comeback','컴백'), ('concert','콘서트'), ('other','기타')])
    created_by  = ForeignKey(User, on_delete=CASCADE)
    created_at  = DateTimeField(auto_now_add=True)
```

### polls.Poll + PollChoice + PollVote
```python
class Poll(Model):
    title       = CharField(max_length=200)
    created_by  = ForeignKey(User, on_delete=CASCADE)
    end_date    = DateTimeField()
    created_at  = DateTimeField(auto_now_add=True)

class PollChoice(Model):
    poll        = ForeignKey(Poll, on_delete=CASCADE)
    text        = CharField(max_length=200)

class PollVote(Model):
    user        = ForeignKey(User, on_delete=CASCADE)
    choice      = ForeignKey(PollChoice, on_delete=CASCADE)
    created_at  = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')  # 중복 투표 방지
```

## 인덱스 설계

| 테이블 | 인덱스 컬럼 | 이유 |
|---|---|---|
| Post | created_at | 최신순 정렬 |
| Comment | post_id | 게시글별 댓글 조회 |
| Like | (user_id, post_id) | 중복 체크 |
| Event | event_date | 날짜별 조회 |
| PollVote | (user_id, choice_id) | 중복 투표 방지 |
