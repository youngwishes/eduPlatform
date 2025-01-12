from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Assignment, Enrollment, Submission, User
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.core.exceptions import PermissionDenied


def home(request):
    courses = Course.objects.all()
    if request.user.is_authenticated and request.user.role == User.TEACHER:
        return redirect('teacher_dashboard')
    return render(request, 'core/home.html', {'courses': courses})


def role_required(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@login_required(login_url='/login/')
@role_required('student', 'teacher')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'core/course_detail.html', {'course': course, 'enrolled': enrolled})


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    return render(request, 'core/assignment_detail.html', {'assignment': assignment})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Войти автоматически после регистрации
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    """Обработка выхода пользователя с перенаправлением."""
    logout(request)
    return redirect('home')  # Перенаправляем на главную страницу после выхода


@login_required(login_url="/login")
@role_required('student')
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
@role_required('student')
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()

    # Если запрос POST и задание ещё не было сдано
    if request.method == 'POST' and not submission:
        file = request.FILES.get('file')
        Submission.objects.create(assignment=assignment, student=request.user, file=file)
        return redirect('assignment_detail', assignment_id=assignment.id)

    return render(request, 'core/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
    })


@login_required
@role_required('teacher')
def course_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    progress_data = course.get_student_progress()
    return render(request, 'core/course_progress.html', {
        'course': course,
        'progress_data': progress_data,
    })

@login_required
@role_required('teacher')
def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, assignment__course__teacher=request.user)
    if request.method == 'POST':
        grade = request.POST.get('grade')
        submission.grade = grade
        submission.save()
        return redirect('course_progress', course_id=submission.assignment.course.id)
    return render(request, 'core/review_submission.html', {'submission': submission})

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    # Получение всех курсов, созданных текущим преподавателем
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/teacher_dashboard.html', {'courses': courses})

@login_required
@role_required('teacher')
def submissions_list(request, assignment_id):
    # Получение всех сданных заданий для конкретного задания
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = assignment.submissions.all()
    return render(request, 'core/submissions_list.html', {
        'assignment': assignment,
        'submissions': submissions
    })

@login_required
@role_required('teacher')
def grade_submission(request, submission_id):
    # Проверка конкретной работы студента
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == 'POST':
        grade = request.POST.get('grade')
        submission.grade = grade
        submission.save()
        return redirect('submissions_list', assignment_id=submission.assignment.id)
    return render(request, 'core/grade_submission.html', {'submission': submission})



@login_required
@role_required('teacher')
def teacher_courses(request):
    """Список курсов, созданных преподавателем."""
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/teacher_courses.html', {'courses': courses})
