"""환경변수 기반 superuser 생성/갱신 (멱등적).

Render 무료 플랜은 Shell 탭이 없어 대화형 createsuperuser를 쓸 수 없으므로,
배포 빌드 단계에서 환경변수로 관리자 계정을 보장한다.

필요 환경변수:
  DJANGO_SUPERUSER_USERNAME (필수)
  DJANGO_SUPERUSER_PASSWORD (필수)
  DJANGO_SUPERUSER_EMAIL    (선택)
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "환경변수로 superuser를 생성하거나 비밀번호를 갱신한다 (멱등적)"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME/PASSWORD 미설정 → superuser 단계 건너뜀"
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "nickname": username},
        )
        user.is_staff = True
        user.is_superuser = True
        if email:
            user.email = email
        user.set_password(password)
        user.save()

        action = "생성" if created else "비밀번호 갱신"
        self.stdout.write(self.style.SUCCESS(f"superuser {action} 완료: {username}"))
