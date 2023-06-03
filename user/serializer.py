from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Tag,Snippet


class userserilalizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','username','password'] 
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 

class Tagserializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class SnippetSerializer(serializers.ModelSerializer):
    tag = Tagserializer()
    class Meta:
        model = Snippet
        fields = "__all__"


        