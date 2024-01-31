from django.contrib import admin
from course import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'price', 'discount']
    list_editable = ['status']
    inlines = [CommentInline]


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', ]


@admin.register(models.UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']


@admin.register(models.UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson']


# @admin.register(models.UserLesson1)
# class UserLesson1Admin(admin.ModelAdmin):
#     list_display = ['user', 'lesson']


# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'rating']


