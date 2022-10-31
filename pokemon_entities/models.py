from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    title_ru = models.CharField("Название на русском языке", max_length=200)
    title_en = models.CharField("Название на английском языке", max_length=200, null=True, blank=True)
    title_jp = models.CharField("Название на японском языке", max_length=200, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Изображение", null=True, blank=True)
    previous_evolutions = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
        verbose_name="Предыдущая эволюция", 
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон, к которому относится")
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField("С какого момента начнет действовать", default=timezone.now)
    disappeared_at = models.DateTimeField("До какого момента будет действовать", default=timezone.now)
    level = models.IntegerField("Уровень", blank=True, null=True)
    health = models.IntegerField("Здоровье", blank=True, null=True)
    strength = models.IntegerField("Атака", blank=True, null=True)
    defence = models.IntegerField("Защита", blank=True, null=True)
    stamina = models.IntegerField("Выносливость", blank=True, null=True)
        
    def __str__(self):
        return self.pokemon.title_ru
