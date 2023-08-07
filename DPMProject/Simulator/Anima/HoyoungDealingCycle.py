from Skill.Anima.Hoyoung import *
from Simulator.SkillSchedule import *
from Character.ABCCharacter import ABCCharacter

# 호영 스킬
여의선 = SkillSchedule([여의선_인])
토파류 = SkillSchedule([토파류_지])
지진쇄 = SkillSchedule([지진쇄_지])
파초풍 = SkillSchedule([파초풍_천])
멸화염 = SkillSchedule([멸화염_천])
금고봉 = SkillSchedule([금고봉_인])
귀화부 = SkillSchedule([추적_귀화부])
분신부 = SkillSchedule([환영_분신부])
호로부 = SkillSchedule([마봉_호로부])
와류 = SkillSchedule([권술_흡성와류])
미생강변 = SkillSchedule([권술_미생강변])
호접지몽 = SkillSchedule([권술_호접지몽])
선단 = SkillSchedule([선기_영약_태을선단])
난무 = SkillSchedule([선기_극대_분신난무])
산령소환 = SkillSchedule([권술_산령소환])
난신 = SkillSchedule([선기_강림_괴력난신])
난신막타 = SkillSchedule([선기_강림_괴력난신_신들의_강림])
천지인 = SkillSchedule([선기_천지인_환영_버프])
파천황 = SkillSchedule([선기_파천황])
레투다2단계 = SkillSchedule([레디_투_다이_2단계])
그여축 = SkillSchedule([그란디스_여신의_축복])

# 호영 딜사이클
준비 = 점프 + 멸화염 + 호접지몽 + 분신부  + 선단 + 와류 + 귀화부
토금파금 = 토파류 + 금고봉 + 파초풍 + 금고봉
# 마지막에 금고봉 넣어야함
극딜 = 그여축 + 산령소환 + 천지인 + 난무 + 토파류 + 난신 + 토파류 + 금고봉 + 엔버링크 +  토파류 + 레투다2단계 + 리레 + 미생강변 + 파천황 + 금고봉
호영테스트딜사이클 = 준비 + 극딜 + 토금파금 * 8 + 난신막타 + 토금파금*2

class HoyoungDealingMode(Enum):
    준비 = 점프 + 멸화염 +호접지몽 + 분신부 + 선단 + 와류 + 귀화부
    # 극딜 마지막에 금고봉 넣은거 의도한 것.
    극딜 = 그여축 + 산령소환 + 천지인 + 난무 + 토파류 + 난신 + 토파류 + 금고봉 + 엔버링크 +  토파류 + 레투다2단계 + 리레 + 미생강변 + 파천황 + 금고봉 + ms_10
    토금파금 = 토파류 + 금고봉 + 파초풍
    토금 = 토파류 + 금고봉


class HoyoungSkillSchedule(SkillSchedule):
    ExtremeAttackMode: HoyoungDealingMode
    Owner: ABCCharacter
    def __init__(self, *args):
        super().__init__(*args)
        self += HoyoungDealingMode.준비.value
        self += HoyoungDealingMode.극딜.value

        
   


    def Next(self):
        # 입력 스킬을 모두 사용하고 난 뒤에 처리
        if len(self) == self.Index and self.Owner.Status not in [CharacterStatus.Using_Skill]:
            # 상황에 따라 다음 스킬 확정
            if self.Owner.BuffManager.isRegistered(선기_강림_괴력난신) and self.Owner.BuffManager.GetRemainingTime(선기_강림_괴력난신) < Cooldown(seconds=0.70):
                self.append(선기_강림_괴력난신_신들의_강림)
                

            if self.ExtremeAttackMode == HoyoungDealingMode.토금파금 and self.Owner.BuffManager.isRegistered(선기_천지인_환영_버프):
                # 금고봉을 사용할 수 있으면 사용
                if self.Owner.CooldownManager.isReady(금고봉_인):
                    self.append(금고봉_인)
                # 금고봉을 사용할 수 없다면, 토파류, 파초풍 사용하여 연계 완성
                else:
                    #1) 금고봉 사용 후 남은 속성 1가지: 남은 속성 보고 토파류, 파초풍 -> 금고봉 
                    #2) 금고봉 사용 후 남은 속성 2가지: 토파류. 여기서 천지인 환영으로 연계 안될 시 남은 속성 사용, 연계될 시 금고봉 사용
                    if 부적.Status[천지인_속성.지.value] == False:
                        self.append(토파류_지)
                        
                    elif 부적.Status[천지인_속성.천.value] == False:
                        self.append(파초풍_천)
                        
                    elif 부적.Status[천지인_속성.인.value] == False:
                        self.append(여의선_인)
                        
            else:
                if self.Owner.CooldownManager.isReady(금고봉_인):
                    self.append(금고봉_인)
                else:
                    self.append(여의선_인)
                    
        
        elif len(self) == self.Index and self.Owner.Status in [CharacterStatus.Using_Skill]:
            return 대기

        
        return super().Next()
