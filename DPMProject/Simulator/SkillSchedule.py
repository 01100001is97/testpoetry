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