from Skill.Adventurer.Bowman.PathFinder import *
from Simulator.SkillSchedule import *

블래스트 = SkillSchedule([카디널_블래스트])
디스차지 = SkillSchedule([카디널_디스차지])
레이븐_소환 = SkillSchedule([레이븐])
레조 = SkillSchedule([엣지_오브_레조넌스])
트임 = SkillSchedule([트리플_임팩트])
이볼브소환 = SkillSchedule([이볼브])
이볼템 = SkillSchedule([이볼브_템페스트])
#레템 = SkillSchedule([레이븐_템페스트])
가이디드 = SkillSchedule([가이디드_에로우])
크리인 = SkillSchedule([크리티컬_리인포스])
얼블 = SkillSchedule([얼티밋_블래스트])
옵시디언 = SkillSchedule([옵시디언_배리어])
언바운드 = SkillSchedule([렐릭_언바운드])
포렐 = SkillSchedule([포세이큰_렐릭])
인챈트_블래스트 = SkillSchedule([커스_인챈트_블래스트])
인챈트_디스차지 = SkillSchedule([커스_인챈트_디스차지])
인챈트_트랜지션 = SkillSchedule([커스_인챈트_트랜지션])
에볼루션 = SkillSchedule([렐릭_에볼루션])
스인미 = SkillSchedule([스파이더_인_미러_패스파인더])
크오솔 = SkillSchedule([크레스트_오브_더_솔라_패스파인더])

카블디 = 블래스트 + 디스차지

블디레조 = 카블디* 6 + 레조

트임실험 = (블디레조*6 + 트임)*3

연계테스트 = 스인미 + 크오솔 + 에픽 +  메여축 + 이볼브소환 + 엔버링크 + 크리인 + 옵시디언 + 리레 + 이볼템  + 포렐  + 얼블 + 에볼루션 + 언바운드 + 블디레조*10