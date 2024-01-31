from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from api import serializers
from course import models


class CategoryView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_serializer_context(self):

        context = super().get_serializer_context()
        user = self.request.user
        if user:
            if user.user_lessons:
                lesson = user.user_lessons.all().last()
                context['last_lesson'] = lesson
        else:
            context['last_lesson'] = None
        return context


class CourseListView(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            get_object_or_404(models.Category, pk=pk)
            queryset = queryset.filter(category__id=pk)
        return queryset


class CourseDetailView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseDetailImageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['comments'] = self.get_object().comments.all()
        return context


