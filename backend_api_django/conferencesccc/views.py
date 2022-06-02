from rest_framework import viewsets

from .models import Amphitheatre
from .models import Conference
from .models import Participant

from .serializers import AmphitheatreSerializer
from .serializers import ConferenceSerializer
from .serializers import ParticipantSerializer

class AmphitheatreViewSet(viewsets.ModelViewSet):
    serializer_class = AmphitheatreSerializer
    queryset = Amphitheatre.objects.all()

class ConferenceViewSet(viewsets.ModelViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()