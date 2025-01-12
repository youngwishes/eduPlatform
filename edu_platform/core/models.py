from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def get_student_progress(self):
        """
        Возвращает прогресс студентов в виде списка:
        [{'student': <User>, 'progress': 75, 'graded_count': 3, 'total_assignments': 4}, ...]
        """
        progress_data = []
        for enrollment in self.enrollments.all():
            student = enrollment.student
            total_assignments = self.assignments.count()
            if total_assignments == 0:
                progress = 0
            else:
                graded_count = Submission.objects.filter(
                    assignment__course=self,
                    student=student,
                    grade__isnull=False
                ).count()
                progress = (graded_count / total_assignments) * 100
            progress_data.append({
                'student': student,
                'progress': progress,
                'graded_count': graded_count,
                'total_assignments': total_assignments,
            })
        return progress_data

    def __str__(self):
        return self.title


class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "материалы"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    grade = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Сданное ДЗ"
        verbose_name_plural = "Сданные ДЗ"

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"

    class Meta:
        verbose_name = verbose_name_plural ="Запись на курс"
