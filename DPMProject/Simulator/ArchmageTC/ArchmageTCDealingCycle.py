from Skill.Adventurer.Magician.ThunderCold import *
from Simulator.SkillSchedule import SkillSchedule

오브 = SkillSchedule([프로즌_오브])
체라 = SkillSchedule([체인_라이트닝])
썬스 = SkillSchedule([썬더_스피어])
블자 = SkillSchedule([블리자드])
썬바 = SkillSchedule([프리징_브레스])

testCycle = 썬스 +오브*2
#testCycle = 썬바+블자 + 썬스 + 오브 + 체라 * 40 + 오브 + 체라 * 40