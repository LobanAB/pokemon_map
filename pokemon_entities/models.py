from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='images', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    title_en = models.CharField('Название англ.', max_length=200, blank=True)
    title_jp = models.CharField('Название яп.', max_length=200, blank=True)
    previous_evolution = models.ForeignKey('self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Предэволюция',
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    Lat = models.FloatField('Широта')
    Lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Появится в...')
    disappeared_at = models.DateTimeField('Исчезнет в...')
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return self.Pokemon.title
