from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from enum import Enum

class PortionDoping(Enum):
    반빨별 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 20)
    반파별 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 20)
    고대비 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 10)
    전영비 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    고관비 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 20)
    고보킬 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 20)
    명장버프 = CreateSpecVector([CoreStat.CRITICAL_DAMAGE], 4)
    주스텟물약 = CreateSpecVector([CoreStat.STAT_ALL], 30)
    익스레드 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL], 30)
    익스블루 = CreateSpecVector([CoreStat.ATTACK_SPELL], 30)
    우뿌 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    길축 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    MVP슈파 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    유힘 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    붕뿌_생축_러파 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 30)
    만렙버프275 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 50)
    영메 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL_PERCENTAGE, CoreStat.ATTACK_SPELL_PERCENTAGE], 4)
    길드크뎀 = CreateSpecVector([CoreStat.CRITICAL_DAMAGE], 30)
    길드뎀지 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 30)
    길드보공 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 30)
    하울링 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 10)


DopingListAlchemy = [
        PortionDoping.반빨별,
        PortionDoping.고관비,
        PortionDoping.주스텟물약,
        PortionDoping.익스레드,
        PortionDoping.익스블루,
        PortionDoping.우뿌,
        PortionDoping.길축,
        PortionDoping.MVP슈파,
        PortionDoping.유힘,
        PortionDoping.붕뿌_생축_러파,
        PortionDoping.만렙버프275,
        PortionDoping.영메,
        PortionDoping.길드크뎀,
        PortionDoping.길드뎀지,
        PortionDoping.길드보공
    ]