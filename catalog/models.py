from django.db import models


class GenusModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PlatformModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class TitleModel(models.Model):
    class Type(models.TextChoices):
        MOVIE = 'movie', 'Filme'
        SERIES = 'series', 'Serie'

    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.MOVIE
    )
    release_year = models.PositiveSmallIntegerField(null=True, blank=True)
    genres = models.ManyToManyField(GenusModel, blank=True)
    total_seasons = models.PositiveSmallIntegerField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.name
