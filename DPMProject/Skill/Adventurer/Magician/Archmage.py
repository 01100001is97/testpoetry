from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat
from Skill.Attributes import *


# 2차 스킬
class 매직_엑셀레이션(PassiveSkill, BuffAttribute):
    def __init__(self, level= 10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 2*level

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

class 메디테이션(OnPressSkill, BuffAttribute, DurationAttribute):
    def __init__(self, level=20):
        max = 20
        meditationIcon = any
        stat = SpecVector()
        stat[CoreStat.ATTACK_SPELL] = 10+level
        OnPressSkill.__init__(self=self, icon = meditationIcon, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        DurationAttribute.__init__(self=self, duration=Cooldown(minutes=4), serverlack=True, isbuffmult=True)

    def UseSkill(self, **kwargs):
        return super().UseSkill(**kwargs)

class 스펠_마스터리(PassiveSkill, BuffAttribute, MasteryAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.ATTACK_SPELL] = level
        mastery = 50

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        MasteryAttribute.__init__(self=self, mastery=mastery)

class 하이_위즈덤(PassiveSkill, BuffAttribute):
    def __init__(self, level =5):
        max = 5
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = level*8

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

# 3차 스킬
class 엘리멘탈_리셋(PassiveSkill, BuffAttribute):
    def __init__(self, level = 9):
        max = 9
        stat = SpecVector()
        stat[CoreStat.IGNORE_ELEMENTAL_RESISTANCE] = 1 + level
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 4 + 4 * level

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)


class 매직_크리티컬(PassiveSkill, BuffAttribute):
    def __init__(self, level = 10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.CRITICAL_PERCENTAGE] = 10 + 2 * level
        stat[CoreStat.CRITICAL_DAMAGE] = 3 + level
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

class 엘리먼트_앰플리피케이션(PassiveSkill, BuffAttribute):
    def __init__(self, level = 10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.DAMAGE_PERCENTAGE] = 5 * level

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)


