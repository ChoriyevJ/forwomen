from rest_framework import serializers
from course import models
from accounts.models import CustomUser


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = 'id', 'title',


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserCourse
        fields = ('id', 'course', 'user', 'is_bought', 'is_finished')


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'image', 'price', 'discount',
                  'category',)


class CourseListByCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'author', 'image', 'status', 'price',
                  'category')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'user', 'content', 'rating')


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('content', 'rating',)


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'image', 'description')

    # def to_representation(self, instance):


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lesson
        fields = ('id', 'title', 'video', 'content')


class UserLessonSerializer(serializers.ModelSerializer):
    user_course = UserCourseSerializer()

    class Meta:
        model = models.UserLesson
        fields = ('id', 'user_course', 'status', 'total_time')


class PaymentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('title', 'price')


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserCourse
        fields = ('payment_type',)
