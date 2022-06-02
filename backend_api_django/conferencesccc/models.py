from django.db import models

class Amphitheatre(models.Model):
    nom = models.CharField(max_length=250)
    numero = models.CharField(max_length=250)
    capacite = models.TextField()
    cout = models.IntegerField()
     

class Participant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    cin = models.CharField(max_length=20)
    telephone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    type = models.CharField(max_length=20)

class Conference(models.Model):
    titre = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    details = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    frais = models.IntegerField()

    amphi = models.ForeignKey(Amphitheatre,on_delete=models.PROTECT)
    conferencier = models.OneToOneField(Participant, related_name='conferencier',on_delete=models.PROTECT)
    participants = models.ManyToManyField(Participant, related_name='participants', through='conferences_participants')


class conferences_participants(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    conference = models.ForeignKey(Conference, on_delete=models.PROTECT)


