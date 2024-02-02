from django.contrib import admin
from course import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class UserLessonWatchedInline(admin.TabularInline):
    model = models.UserLessonWatched
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
list_display_links = ['title']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'author', 'status', 'price', 'discount']
    list_display_links = ['title']
    list_editable = ['status']
    inlines = [CommentInline]
    raw_id_fields = ['category']


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course']
    list_display_links = ['title']
    raw_id_fields = ['course']


@admin.register(models.UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course']
    list_display_links = ['user']
    raw_id_fields = ['course']


@admin.register(models.UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_course', 'lesson']
    list_display_links = ['user_course']
    raw_id_fields = ['user_course', 'lesson']
    inlines = [UserLessonWatchedInline]


# @admin.register(models.UserLesson1)
# class UserLesson1Admin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'lesson']


# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'rating']


