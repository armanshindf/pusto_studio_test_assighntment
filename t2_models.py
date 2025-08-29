from django.db import models

class Player(models.Model): 
    player_id = models.CharField(max_length=100)

class Level(models.Model): 
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0) 

class Prize(models.Model):
    title = models.CharField()

class PlayerLevel(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)


    def assign_prizes_for_level_completion(player_level: PlayerLevel):
        if not player_level.is_completed:
            return
        level_prizes = LevelPrize.objects.filter(level=player_level.level).values_list('prize', flat=True).distinct()
        for prize_id in level_prizes:
            exists = LevelPrize.objects.filter(
                player=player_level.player,
                level=player_level.level,
                prize_id=prize_id
                ).exists()
            if not exists:
                LevelPrize.objects.create(
                    player=player_level.player,
                    level=player_level.level,
                    prize_id=prize_id,
                    received=timezone.now().date()
            )

class LevelPrize( models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='level_prizes')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()