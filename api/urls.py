from django.urls import path
from api import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view()),

    path('courses/', views.CourseListView.as_view()),
    path('courses/<int:pk>/category/', views.CourseListView.as_view()),
    path('course/<int:pk>/finished/', views.CourseFinishedView.as_view()),
    path('course/<int:pk>/get-cert/', views.GetCertificateView.as_view()),

    path('course/<int:pk>/', views.CourseDetailView.as_view()),
    path('course/<int:course_id>/lessons/', views.CourseLessonListView.as_view()),
    path('course/<int:course_id>/lesson/<int:pk>/', views.CourseLessonDetailView.as_view()),

    path('course/<int:pk>/payment/', views.PaymentView.as_view())
]
