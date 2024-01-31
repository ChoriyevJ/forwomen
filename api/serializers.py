from rest_framework import serializers
from course import models
from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('title',)


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'author', 'image', 'status', 'price',
                  'category')


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.Comment
        fields = ('user', 'content', 'rating')


class CourseDetailImageSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(
        queryset=models.Comment.objects.all(), many=True)

    class Meta:
        model = models.Course
        fields = ('title', 'image', 'description', 'comments')


class CourseDetailVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = ('title', 'video', '')

