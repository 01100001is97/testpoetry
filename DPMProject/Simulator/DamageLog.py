from Core.ABCSkill import Skill
from Core.SpecElements import SpecVector
from datetime import timedelta
from Core.Condition import ConditionEnum
from copy import deepcopy
class DamageLog:
    """
    데미지 로그 클래스. 
    
    Skill 클래스의 인스턴스, 데미지(float), 버프(SpecVector), 디버프(SpecVector)를 입력받아
    데미지 로그를 기록하며, 기록 시각을 저장합니다.
    
    Args:
        skill (Skill): 사용한 스킬을 나타내는 Skill 클래스의 인스턴스.
        damage (float): 해당 스킬 사용으로 인한 데미지.
        buff (SpecVector): 해당 스킬 사용 시점의 버프 상태를 나타내는 SpecVector 인스턴스.
        debuff (SpecVector): 해당 스킬 사용 시점의 디버프 상태를 나타내는 SpecVector 인스턴스.
        add (SpecVector): 해당 스킬에만 적용되는 특수 스펙
    Raises:
        TypeError: skill이 Skill 타입이 아닐 경우, 
                   time이 timedelta 타입이 아닐 경우.
    """

    def __init__(self, skillname: Skill, damage: float, point: int, buff: SpecVector, debuff: SpecVector, add:SpecVector, condition:ConditionEnum, line:int):
        self._SkillName = skillname
        self._Damage = damage
        self._Buff = buff
        self._Debuff = debuff
        self._Timestamp = None
        self._Add = add
        self._MonsterCondition = deepcopy( condition)
        self._Point = point
        self._AttackLine = line

    @property
    def Timestamp(self):
        """Timestamp 속성에 대한 getter 메서드.

        Returns:
            datetime.timedelta: Timestamp의 값을 반환.
        """
        return self._Timestamp

    @Timestamp.setter
    def Timestamp(self, time: timedelta):
        """Timestamp 속성에 대한 setter 메서드.

        Args:
            time (timedelta): Timestamp에 설정할 값. timedelta 타입이어야 함.

        Raises:
            TypeError: time이 timedelta 타입이 아닐 경우.
        """
        if not isinstance(time, timedelta):
            raise TypeError("time must be a timedelta type")
        self._Timestamp = time

    def __str__(self):
        """
        DamageLog 클래스의 인스턴스를 사람이 읽을 수 있는 문자열 형태로 출력합니다.
        
        Returns:
            str: DamageLog 인스턴스의 상세 정보.
        """
        return f"###Timestamp###: {self._Timestamp}\n" \
            f"Skill------------------------\n{self._SkillName}\n" \
            f"Damage p%--------------------\n{self._Point} * {self._AttackLine}\n" \
            f"Damage per Line--------------\n{self._Damage}\n" \
            f"Buff-------------------------\n{self._Buff}\n" \
            f"Debuff-----------------------\n{self._Debuff}\n" \
            f"Additional Spec--------------\n{self._Add}\n" \
            f"Condition--------------------\n{self._MonsterCondition}\n\n"
