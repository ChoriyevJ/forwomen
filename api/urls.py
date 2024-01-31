from django.urls import path
from course import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view()),

    path('courses/', views.CourseListView.as_view()),
    path('courses/<int:pk>/category', views.CourseListView.as_view()),

    path('course/<int:pk>/detail/', views.CourseDetailView.as_view()),

]
