from rest_framework import serializers
from .models import BlogPost

# create serializer for models and the fields to be returned
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "published_date"]