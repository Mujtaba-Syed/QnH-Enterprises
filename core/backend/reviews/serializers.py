from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
    
    def create(self, validated_data):
        # User will be set in the view from request.user
        return Review.objects.create(**validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url if instance.image else None
        if instance.whtsapp_image:
            data['whtsapp_image'] = instance.whtsapp_image.url if instance.whtsapp_image else None
        return data
