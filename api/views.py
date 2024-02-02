from rest_framework import serializers as rest_serializers
from rest_framework import generics
from rest_framework.response import Response

from api import serializers
from course import models
from accounts.models import CustomUser


class CategoryView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CourseListView(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            course_id = data['id']

            buyers_ids = models.UserCourse.objects.filter(
                course_id=course_id, is_bought=True).values_list('user', flat=True)

            buyers_serializer = serializers.UserSerializer(
                CustomUser.objects.filter(id__in=buyers_ids), many=True
            )
            data['buyers'] = buyers_serializer.data

        return Response(serializer.data)


class CourseListByCatListView(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseListByCatSerializer


class CourseDetailView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        models.UserCourse.objects.get_or_create(
            course=course,
            user=self.request.user
        )
        comments = models.Comment.objects.filter(course=course)
        comments_serializer = serializers.CommentSerializer(comments, many=True)

        serializer = self.get_serializer(course)
        data = serializer.data
        data['comments'] = comments_serializer.data

        return Response(data)


class CourseLessonListView(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        queryset = models.Lesson.objects.filter(
            course_id=self.kwargs.get('course_id')
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for data in serializer.data:
            lesson_id = data['id']
            user_lesson = models.UserLesson.objects.get_or_create(
                user_course=models.UserCourse.objects.get(
                    course_id=self.kwargs.get('course_id')),
                lesson=models.Lesson.objects.get(id=lesson_id),
                total_time=1000
            )
            if user_lesson:
                user_lesson = user_lesson[0]
            user_lesson_serializer = serializers.UserLessonSerializer(user_lesson)
            data['user_lesson'] = user_lesson_serializer.data

        return Response(serializer.data)


class CourseLessonDetailView(generics.RetrieveAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(course_id=self.kwargs.get('course_id'))
        return queryset


class CourseFinishedView(generics.ListAPIView):
    queryset = models.UserLesson
    serializer_class = serializers.UserLessonSerializer

    def get_queryset(self):
        queryset = models.UserLesson.objects.filter(
            user_course__course_id=self.kwargs.get('pk'),
            user_course__user=self.request.user,
            user_course__is_bought=True
        )
        return queryset


class GetCertificateView(generics.CreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.UserCommentSerializer

    def create(self, request, *args, **kwargs):
        class TitleSer(rest_serializers.Serializer):
            title = rest_serializers.CharField()

        user_course = models.UserCourse.objects.filter(
            user=request.user.id,
            course_id=self.kwargs.get('pk'),
            is_bought=True,
            is_finished=True
        ).get(course_id=self.kwargs.get('pk'))
        course_name = user_course.course.title
        user = request.user
        comment = models.Comment.objects.create(
            user=user.id,
            course=user_course.course.id,
            content=request.data['content'],
            rating=request.data['rating']
        )
        comment.save()

        serializer = self.get_serializer(comment)
        serializer.is_valid()

        serializer.data[2] = TitleSer(course_name).data

        self.perform_create(serializer)

        return Response(serializer.data, status=201)


class PaymentView(generics.CreateAPIView):
    serializer_class = serializers.PaymentSerializer

    def get(self, request, *args, **kwargs):
        course = models.Course.objects.get(pk=kwargs.get('pk'))
        course_seril = serializers.PaymentCourseSerializer(course)

        return Response(course_seril.data)
