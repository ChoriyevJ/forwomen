from django.db import models
from django.db.models import Q
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from course.utils.models import BaseModel


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


class UserCourse(BaseModel):
    class PaymentType(models.TextChoices):
        PAYME = 'PM', 'Payme',
        APELSIN = 'AP', 'Apelsin'
        CLICK = 'CL', 'Click',
        VISA = 'VS', 'Visa'
        __empty__ = None

    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='user_courses')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_courses')
    payment_type = models.CharField(max_length=2, choices=PaymentType.choices,
                                    default=PaymentType.__empty__)
    is_bought = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'user')

    def finished(self):
        if len(self.user_lessons.filter(Q(status__in=['NW', 'PR']))) == 0:
            self.is_finished = True
            self.save()

    def __str__(self):
        return f'{self.user}\'s {self.course} course.'

    def __repr__(self):
        return f'UserCourse(user="{self.user}", course="{self.course}")'


class UserLesson(BaseModel):

    class Status(models.TextChoices):
        FINISHED = 'FI', 'Ko\'rilgan'
        IN_PROGRESS = 'PR', 'Jarayonda'
        NO_WATCH = 'NW', 'Ko\'rilmagan'

    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE,
                                    related_name='user_lessons')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE,
                               related_name='user_lessons')
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.NO_WATCH)
    total_time = models.IntegerField()
    current_watch_time = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user_course', 'lesson',)

    def change_status(self):
        if self.current_watch_time > self.total_time * 0.9:
            self.status = self.Status.FINISHED
        elif self.current_watch_time > 0:
            self.status = self.Status.IN_PROGRESS
        else:
            self.status = self.Status.NO_WATCH
        self.save()

    def change_current_watched_time(self):
        watched_times = self.user_lesson_watched.filter(is_used=False)
        for w_time in watched_times:
            w_time.is_used = True
            w_time.save()
            self.current_watch_time += w_time.to_time - w_time.from_time
        self.save()

    def __str__(self):
        return f'{self.user_course}\'s {self.lesson}'


class UserLessonWatched(BaseModel):
    user_lesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE,
                                    related_name='user_lesson_watched')
    from_time = models.IntegerField(default=0)
    to_time = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_lesson}, ({self.from_time}, {self.to_time})'


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





