from Core.SpecElements import SpecVector, CoreStat
from Core.Job import JobType, JobTypeInfo
from math import floor
    
def toPercent(num:int):
    return (100+num)/100

def BattlePower(spec:SpecVector, jobtype:JobType, considerGuard = 300, isBoss = True, elementalResistance = False):
    spec.Arrange()

    result = 0

    MainStatList = [e for e in jobtype.value[JobTypeInfo.MainStat.value]]
    SubStatList = [e for e in jobtype.value[JobTypeInfo.SubStat.value]]

    STR = spec[CoreStat.STAT_STR]*toPercent(spec[CoreStat.STAT_STR_PERCENTAGE])+spec[CoreStat.STAT_STR_FIXED]
    DEX = spec[CoreStat.STAT_DEX]*toPercent(spec[CoreStat.STAT_DEX_PERCENTAGE])+spec[CoreStat.STAT_DEX_FIXED]
    INT = spec[CoreStat.STAT_INT]*toPercent(spec[CoreStat.STAT_INT_PERCENTAGE])+spec[CoreStat.STAT_INT_FIXED]
    LUK = spec[CoreStat.STAT_LUK]*toPercent(spec[CoreStat.STAT_LUK_PERCENTAGE])+spec[CoreStat.STAT_LUK_FIXED]
    HP = None
    MP = None
    ATK = floor(spec[CoreStat.ATTACK_PHYSICAL]*toPercent(spec[CoreStat.ATTACK_PHYSICAL_PERCENTAGE])+spec[CoreStat.ATTACK_PHYSICAL_FIXED])
    SPELL = floor(spec[CoreStat.ATTACK_SPELL]*toPercent(spec[CoreStat.ATTACK_SPELL_PERCENTAGE])+spec[CoreStat.ATTACK_SPELL_FIXED])

    if jobtype == JobType.Xenon:
        pass
    elif MainStatList[0] == CoreStat.STAT_STR:
        result = (STR*4 + LUK)*0.01 * ATK
        pass
    elif MainStatList[0] == CoreStat.STAT_DEX:
        #궁수, 덱해적
        result = (DEX*4 + LUK)*0.01 * ATK
    elif MainStatList[0] == CoreStat.STAT_INT:
        result = (INT*4 + LUK)*0.01 * SPELL
    elif MainStatList[0] == CoreStat.STAT_LUK:
        result = (LUK*4 + DEX)*0.01 * ATK
        pass
    elif MainStatList[0] == CoreStat.STAT_HP:
        # 데벤
        pass

    if isBoss:
        result = result * toPercent(spec[CoreStat.DAMAGE_PERCENTAGE_BOSS] + spec[CoreStat.DAMAGE_PERCENTAGE])
    else:
        result = result * toPercent(spec[CoreStat.DAMAGE_PERCENTAGE])

    FianlDamage = (toPercent(spec[CoreStat.FINAL_DAMAGE_PERCENT])) 
    result = result * FianlDamage

    CriticalDamage = 1 + (spec[CoreStat.CRITICAL_DAMAGE] + 35)/100 * max(spec[CoreStat.CRITICAL_PERCENTAGE] , 100)/ 100
    result = CriticalDamage * result

    if considerGuard == 0:
        pass
    else:
        IgnoreGuardConst = 1 - considerGuard * (100-spec[CoreStat.IGNORE_GUARD_PERCENTAGE])/10000
        result = IgnoreGuardConst * result

    if elementalResistance == True:
        resistanceConst = (100 + spec[CoreStat.IGNORE_ELEMENTAL_RESISTANCE])/200
        result = resistanceConst * result

    return max(1, result)

