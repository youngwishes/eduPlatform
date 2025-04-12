from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('courses/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('teacher/course/<int:course_id>/progress/', views.course_progress, name='course_progress'),
    path('teacher/submission/<int:submission_id>/review/', views.review_submission, name='review_submission'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assignments/<int:assignment_id>/submissions/', views.submissions_list, name='submissions_list'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('faq/', views.faq, name='faq'),
    path('my-courses/', views.my_courses, name='my_courses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
