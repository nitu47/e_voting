from django.db import models

class Voter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Candidate(models.Model):
    name = models.CharField(max_length=150)
    party = models.CharField(max_length=150, blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
'''class Voter(models.Model):
    email = models.EmailField(unique=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email'''
