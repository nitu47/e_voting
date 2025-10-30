from django.db import models

class Voter(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Candidate(models.Model):
    name = models.CharField(max_length=150)
    party = models.CharField(max_length=150, blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
