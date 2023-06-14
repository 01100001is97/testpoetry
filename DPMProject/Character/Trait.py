from Core.SpecElements import SpecVector, CoreStat


TraitStat = SpecVector()

# 카리스마
TraitStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

# 통찰력
TraitStat[CoreStat.IGNORE_ELEMENTAL_RESISTANCE] = 5

# 감성
TraitStat[CoreStat.STAT_HP] = 2000
TraitBuffDuration = 10

# 의지 
TraitStat[CoreStat.STAT_HP] += 2000

# 손재주
#매력