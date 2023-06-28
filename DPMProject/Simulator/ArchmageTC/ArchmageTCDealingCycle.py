from Skill.Adventurer.Magician.ThunderCold import *
from Simulator.SkillSchedule import *



오브 = SkillSchedule([프로즌_오브])
체라 = SkillSchedule([체인_라이트닝])
썬스 = SkillSchedule([썬더_스피어])
블리자드_사용 = SkillSchedule([블리자드])
썬바 = SkillSchedule([프리징_브레스])
엘퀴 = SkillSchedule([엘퀴네스])
인피 = SkillSchedule([인피니티])
라스피 = SkillSchedule([라이트닝_스피어])
오라 = SkillSchedule([아이스_오라_사용])
썬브 = SkillSchedule([썬더_브레이크])
스오스 = SkillSchedule([스피릿_오브_스노우])
에이지 = SkillSchedule([아이스_에이지])
주썬 = SkillSchedule([주피터_썬더])

스인미 = SkillSchedule([스파이더_인_미러_썬콜])
크오솔 = SkillSchedule([크레스트_오브_더_솔라_썬콜])
프라 = SkillSchedule([프로즌_라이트닝])

testCycle = 라스피 + 썬브 + 체라*2 + 썬브
#testCycle = 썬바+블자 + 썬스 + 오브 + 체라 * 40 + 오브 + 체라 * 40
오브체라 =  오브 + 체라* 6
BurstCycle = 인피 + ms_10 * 9500 + 에픽 + 메여축 + 스인미 + 크오솔 + 스오스 + 오라 + 엔버링크 + 썬바 + 리레 + 에이지 + 체라 + 주썬 + 프라 + 오브  + 라스피 + 썬브 + 체라*3 + 오브체라*4