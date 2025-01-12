from django.core.management.base import BaseCommand
from core.models import Course, User
import random

class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми курсами."

    def handle(self, *args, **kwargs):
        teachers = User.objects.filter(is_staff=True)
        if not teachers.exists():
            self.stdout.write(self.style.ERROR("Нет преподавателей для назначения курсов."))
            return

        course_titles = [
            "Основы программирования",
            "Разработка веб-приложений",
            # остальные курсы
        ]
        course_descriptions = [
            "Этот курс предоставляет основы для начинающих в программировании.",
            "Учимся создавать современные веб-приложения с Django и React.",
            # остальные описания
        ]

        for i in range(len(course_titles)):
            title = course_titles[i]
            description = course_descriptions[i]
            teacher = random.choice(teachers)
            Course.objects.create(
                title=title,
                description=description,
                teacher=teacher
            )
            self.stdout.write(f"Курс '{title}' успешно создан.")

        self.stdout.write(self.style.SUCCESS("Тестовые курсы успешно добавлены."))
