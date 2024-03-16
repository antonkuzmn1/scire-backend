from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'username', 'password',
                  'name', 'title', 'description', 'deleted']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            company = Company.objects.filter(username=username).first()

            if company:
                if check_password(password, company.password):
                    return data
            raise serializers.ValidationError('Invalid username or password.')
        else:
            raise serializers.ValidationError('Both username and password are required.')