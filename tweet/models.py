from django.db import models

class Profile(models.Model):
    profile_name = models.CharField(max_length=500)

    def __str__(self):
        return self.profile_name

class Tweets(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text
