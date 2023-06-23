from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat
from Skill.Attributes import *


# 1차 스킬
class MP증가(PassiveSkill, BuffAttribute):
    def __init__(self, level=20):
        max = 20
        stat = SpecVector()
        stat[CoreStat.STAT_MP_PERCENTAGE] = level
        stat[CoreStat.STAT_MP] = 20+5*level

        # 추후 변경점: 완드 착용시 크확 5% 증가

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.First, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

    def DeleteBuff(self):
        pass

# 매직 가드, 에너지 볼트, 텔레포트, 마나 웨이브, 매직 아머