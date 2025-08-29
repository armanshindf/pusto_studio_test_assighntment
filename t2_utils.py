import pandas as pd
from pusto_studio_test_assignment.models import PlayerLevel, LevelPrize


def export_player_level_data(file_path):
    batch_size = 10000
    pd.DataFrame(columns=['player_id', 'level_title', 'is_completed', 'prizes']).to_csv(file_path, index=False)
    qs = PlayerLevel.objects.select_related('player', 'level').all()
    total = qs.count()
    for start in range(0, total, batch_size):
        batch = qs[start:start+batch_size]
        player_ids = set(pl.player_id for pl in batch)
        level_ids = set(pl.level_id for pl in batch)
        prizes_qs = LevelPrize.objects.filter(
            player_id__in=player_ids,
            level_id__in=level_ids
        ).select_related('prize')
        prizes_dict = {}
        for lp in prizes_qs:
            key = (lp.player_id, lp.level_id)
            prizes_dict.setdefault(key, []).append(lp.prize.title)
        data = []
        for pl in batch:
            prizes = prizes_dict.get((pl.player_id, pl.level_id), [])
            prizes_str = ';'.join(prizes) if prizes else ''
            data.append({
                'player_id': pl.player.player_id,
                'level_title': pl.level.title,
                'is_completed': pl.is_completed,
                'prizes': prizes_str
            })
        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='a', index=False, header=False)