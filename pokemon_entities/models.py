from django.db import models
import os
from pogomap import settings




class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название покемона')
    english_title = models.CharField(max_length=200, verbose_name='Название по-английски', blank=True)
    japanese_title = models.CharField(max_length=200, verbose_name='Название по-японски', blank=True)
    image = models.ImageField(upload_to='pokemon_avatars', verbose_name='Избражение покемона', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='evolutions',
                                           verbose_name='Эвольционирует из', null=True, blank=True)



    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Координаты покемона:', on_delete=models.CASCADE,
                                related_name='pokemon_entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появляется', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Пропадает', null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень', default=1, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', default=1, blank=True)
    strength = models.IntegerField(verbose_name='Сила', default=1, blank=True)
    defence = models.IntegerField(verbose_name='Защита', default=1, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', default=1, blank=True)

    def __str__(self):
        return 'Координаты'
