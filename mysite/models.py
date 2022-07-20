from django.db import models

# Create your models here.
class Input(models.Model):
    # link = models.CharField(max_length=200)
    json_input = models.JSONField()


class Data(models.Model):
    ref_id = models.CharField(max_length=500)
    words = models.IntegerField()
    filler_words = models.IntegerField()
    grammatical_errors = models.IntegerField()
    pauses = models.IntegerField()
    repeated_words = models.IntegerField()
    variation = models.IntegerField()

    def __str__(self):
        return str(self.pk)