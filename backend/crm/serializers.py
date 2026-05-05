from rest_framework import serializers
from .models import Lead, Interaction, Task, Project

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
