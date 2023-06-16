from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from enum import Enum

class Trait(Enum):
    카리스마 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 10) 
    통찰력 = CreateSpecVector([CoreStat.IGNORE_ELEMENTAL_RESISTANCE], 5) 
    감성 = 10
    의지 = CreateSpecVector([CoreStat.STAT_HP], 2000) 
    손재주 = None
    매력 = None
