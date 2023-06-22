from Core.ABCSkill import PassiveSkill, SkillAdvance, OnHitActivate, OnPressSkill, KeydownSkill, AutomateActivativeSkill
from Core.SpecElements import SpecVector, CoreStat
from Attributes import *



# 허수아비 만든 후 변경예정
class 익스트림_매직_불독(AutomateActivativeSkill, BuffAttribute):
    def init(self, level: int):
        max = 10
        stat = SpecVector()
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 2 * level
        
        AutomateActivativeSkill.__init__(
            self = self,
            self=AutomateActivativeSkill, 
            advanced= SkillAdvance.Third,
            level= level,
            max=max,
            # 추후 허수아비 만든 후 람다함수 완성할 것. 
            activator= lambda t: t.GetCondition(),
            target=self._Owner
            )
        BuffAttribute.__init__(self=self, stat=stat)
