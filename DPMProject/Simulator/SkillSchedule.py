from Skill.CommonSkill import *
from Skill.LinkSkill import 소울_컨트랙트
from datetime import timedelta


class SkillSchedule(list):
    """SkillSchedule는 스킬의 스케줄을 관리합니다.
    
    SkillSchedule는 list를 상속받아 사용하며, 스킬을 순차적으로 사용하기 위한 메서드와 프로퍼티를 제공합니다.

    Attributes:
        Index: 현재 스케줄의 위치를 나타내는 인덱스입니다.
    """
    def __init__(self, *args):
        super().__init__(*args)
        self._Index = 0
    
    @property
    def Index(self):
        """Index 속성의 getter입니다."""
        return self._Index
    
    @Index.setter
    def Index(self, num: int):
        """Index 속성의 setter입니다."""
        if not isinstance(num, int):
            raise TypeError("Index must be an integer.")
        if num < 0:
            raise ValueError("Index must be within the range of the SkillSchedule.")
        self._Index = num

    def Next(self):
        """다음에 사용할 스킬을 반환하며, 스케줄을 다음으로 진행합니다."""
        if self.Index >= len(self):
            return None
        next_skill = self[self.Index]
        self.Index += 1
        return next_skill
    
    def Before(self):
        if self.Index >= 2:
            return self[self.Index-2]
        else:
            raise ValueError("이전 스킬이 존재하지 않음")
    
    def __add__(self, other):
        """두 SkillSchedule를 결합합니다."""
        if not isinstance(other, SkillSchedule):
            raise TypeError("Only SkillSchedule instances can be added.")
        return SkillSchedule(list(self) + other)

    def __mul__(self, num):
        """SkillSchedule를 주어진 횟수만큼 반복합니다."""
        if not isinstance(num, int):
            raise TypeError("A SkillSchedule can only be multiplied by an integer.")
        return SkillSchedule(list(self) * num)
    
    def __iadd__(self, other):
        """기존 SkillSchedule에 다른 SkillSchedule를 추가합니다."""
        if not isinstance(other, SkillSchedule):
            raise TypeError("Only SkillSchedule instances can be added.")
        self.extend(other)
        return self
    
    def Duration(self):
        result = timedelta()
        for skill in self:
            if issubclass(skill, SkillDelayAttribute):
                delay = skill().AttackDelay.delta
                result += delay
            elif issubclass(skill, 대기):
                result += timedelta(milliseconds=10)
            else:
                continue
                #raise AttributeError("스킬 딜레이가 없는 스킬을 사용하려 함")
        return result

    
    def __str__(self):
        result = ""
        대기중 = "대기중"
        waitingCount = 0
        for i in self:
            if str(i()) == 대기중:
                waitingCount += 0.01
            else:
                if waitingCount > 0:  # 대기 시간이 있으면 결과 문자열에 추가
                    result += f"약 {round(waitingCount,2)}초 대기 -> "
                    waitingCount = 0  # 대기 시간 초기화
                result += str(i()) + " -> "
        if waitingCount > 0:  # 마지막 요소가 대기중인 경우를 처리
            result += f"{waitingCount}초 대기"
        return result

    


리레 = SkillSchedule([리스트레인트링])
웨폰I = SkillSchedule([웨폰퍼프_I링])
웨폰S = SkillSchedule([웨폰퍼프_S링])
웨폰D = SkillSchedule([웨폰퍼프_D링])
웨폰L = SkillSchedule([웨폰퍼프_L링])
엔버링크 = SkillSchedule([소울_컨트랙트])
에픽 = SkillSchedule([에픽_어드벤처])
메여축 = SkillSchedule([메이플_여신의_축복])
스인미 = SkillSchedule([스파이더_인_미러])
크오솔 = SkillSchedule([크레스트_오브_더_솔라])
ms_10 = SkillSchedule([대기])
