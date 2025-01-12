from django.contrib import admin
from .models import Course, Material, Assignment, Submission, User, Enrollment

# Кастомизация отображения пользователей
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)

# Кастомизация отображения курсов
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher')
    search_fields = ('title', 'teacher__username')
    list_filter = ('teacher',)
    ordering = ('title',)

# Кастомизация отображения материалов
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

# Кастомизация отображения заданий
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    ordering = ('deadline',)

# Кастомизация отображения отправленных ДЗ
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grade')
    search_fields = ('assignment__title', 'student__username')
    list_filter = ('assignment', 'grade')

# Кастомизация отображения записей
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    search_fields = ('student__username', 'course__title')
    list_filter = ('course',)

