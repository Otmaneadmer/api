from rest_framework import serializers
from .models import Amphitheatre
from .models import Conference
from .models import Participant

class AmphitheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amphitheatre
        fields = '__all__'

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'