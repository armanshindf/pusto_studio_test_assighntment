from django.db import models

class Player(models.Model):
    
    first_login = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Первый вход",
        help_text="Дата и время первого входа игрока"
    )
    
    points = models.IntegerField(
        default=0,
        verbose_name="Баллы",
        help_text="Общее количество накопленных баллов"
    )
    
    level = models.PositiveIntegerField(
        default=1,
        verbose_name="Уровень",
        help_text="Текущий уровень"
    )
    
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последний вход",
        help_text="Дата и время последнего входа"
    )
    
    consecutive_logins = models.PositiveIntegerField(
        default=0,
        verbose_name="Дней подряд",
        help_text="Количество дней подряд с входом в игру"
    )
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['-points']
    
    

class Boost(models.Model):

    BOOST_TYPES = (
        ('speed', 'Скорость'),
        ('shield', 'Защита'),
        ('double_xp', 'Двойной опыт'),
        ('extra_coins', 'Доплнительные монеты'),
    )
    
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='boosts',
        verbose_name="Игрок",
        help_text="Игрок, которому принадлежит буст"
    )
    
    boost_type = models.CharField(
        max_length=20,
        choices=BOOST_TYPES,
        verbose_name="Тип буста",
        help_text="Тип усилителя игрока"
    )
    
    amount = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество",
        help_text="Количество активаций буста"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Дата получения буста"
    )
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Истекает",
        help_text="Дата истечения срока действия буста"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Активен ли буст"
    )
    
    class Meta:
        verbose_name = "Буст"
        verbose_name_plural = "Бусты"
        unique_together = ['player', 'boost_type']  # Уникальная пара игрок-тип буста
        ordering = ['-created_at']