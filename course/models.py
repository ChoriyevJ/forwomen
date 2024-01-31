from django.db import models
from django.db.models import IntegerField, F
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from course.utils.models import BaseModel

'''
Category, Course, Lesson, Comment

Category => (title, )
Course => (title, category, is_finished, image, price, discount, status, author, is_bought)
Lesson => (course, title, content, photo, video, is_view)
Comment => (user, content, rating, course)
'''


class Category(BaseModel):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='category/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category(pk={self.pk})'


class Course(BaseModel):
    class Status(models.TextChoices):
        RECOMMENDED = 'REC', 'Tavsiya etiladi',
        BESTSELLER = 'BES', 'Bestseller'
        __empty__ = ''

    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course/%Y/%m/%d')
    status = models.CharField(max_length=3,
                              choices=Status.choices)

    price = models.IntegerField()
    discount = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='courses')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Course(pk={self.pk}, title="{self.title}")'

    @property
    def current_price(self):
        return IntegerField()


class UserCourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='user_courses')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_courses')

    is_bought = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f'{self.user}\'s {self.course} course.'

    def __repr__(self):
        return f'UserCourse(user="{self.user}", course="{self.course}")'


class UserLesson(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_lessons')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE,
                               related_name='user_lessons')
    is_view = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson',)

    def save(self, *args, **kwargs):
        if self.user.user_courses:
            courses = self.user.user_courses.all()
            for c in courses:
                course = c.course
                if course.lessons.filter(pk=self.lesson.pk).exists():
                    continue
                else:
                    raise

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}\'s {self.lesson}'


class Lesson(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()

    photo = models.ImageField(upload_to='lessons/images/%Y/%m/%d')
    video = models.FileField(upload_to='lessons/video/%Y/%m/%d',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])])

    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='lessons')

    class Meta:
        unique_together = ('title', 'course')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Lesson(pk={self.pk}, title="{self.title}")'


class Comment(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='comments')

    content = models.CharField(max_length=400)
    rating = models.SmallIntegerField(default=0)
