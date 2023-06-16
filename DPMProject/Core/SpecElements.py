from enum import Enum


class CoreStat(Enum):
    """메이플스토리 데미지 산식에 관여하는 모든 요소

    Args:
        Enum (_type_): 
        STAT_STR: 순 힘스텟\n
        STAT_DEX: 순 덱스스텟\n
        STAT_INT: 순 인트스텟\n
        STAT_LUK: 순 럭스텟\n
        STAT_STR_FIXED: 고정 힘스텟\n
        STAT_DEX_FIXED: 고정 덱스스텟\n
        STAT_INT_FIXED: 고정 인트스텟\n
        STAT_LUK_FIXED: 고정 럭스텟\n
        STAT_STR_PERCENTAGE: 힘퍼\n
        STAT_DEX_PERCENTAGE: 덱퍼\n
        STAT_INT_PERCENTAGE: 인퍼\n
        STAT_LUK_PERCENTAGE: 럭퍼\n
        ATTACK_PHYSICAL: 물리공격력\n
        ATTACK_SPELL: 마력\n
        ATTACK_PHYSICAL_FIXED: 고정 물리공격력(루미농장)\n
        ATTACK_SPELL_FIXED: 고정 마력(루미농장)\n
        ATTACK_PHYSICAL_PERCENTAGE: 공퍼\n
        ATTACK_SPELL_PERCENTAGE: 마력퍼\n
        DAMAGE_PERCENTAGE: 데미지퍼\n
        DAMAGE_PERCENTAGE_BOSS: 보공퍼\n
        CRITICAL_PERCENTAGE: 크확\n
        CRITICAL_DAMAGE: 크뎀\n
        IGNORE_GUARD_PERCENTAGE: 방무\n
        IGNORE_ELEMENTAL_RESISTANCE: 속성내성저항\n
        FINAL_DAMAGE_PERCENT: 최종뎀\n

    """    
    STAT_STR = 0
    STAT_DEX = 1
    STAT_INT = 2
    STAT_LUK = 3
    STAT_ALL = 4
    STAT_STR_FIXED = 5
    STAT_DEX_FIXED = 6
    STAT_INT_FIXED = 7
    STAT_LUK_FIXED = 8
    STAT_ALL_FIXED = 9
    STAT_STR_PERCENTAGE = 10
    STAT_DEX_PERCENTAGE = 11
    STAT_INT_PERCENTAGE = 12
    STAT_LUK_PERCENTAGE = 13
    STAT_ALL_PERCENTAGE = 14
    STAT_STR_9LEVEL = 15
    STAT_DEX_9LEVEL = 16
    STAT_INT_9LEVEL = 17
    STAT_LUK_9LEVEL = 18
    ATTACK_PHYSICAL = 19
    ATTACK_SPELL = 20
    ATTACK_PHYSICAL_FIXED = 21
    ATTACK_SPELL_FIXED = 22
    ATTACK_PHYSICAL_PERCENTAGE = 23
    ATTACK_SPELL_PERCENTAGE = 24
    DAMAGE_PERCENTAGE = 25
    DAMAGE_PERCENTAGE_BOSS = 26
    CRITICAL_PERCENTAGE = 27
    CRITICAL_DAMAGE = 28
    IGNORE_GUARD_PERCENTAGE = 29
    IGNORE_ELEMENTAL_RESISTANCE = 30
    FINAL_DAMAGE_PERCENT = 31
    STAT_HP = 32
    STAT_HP_PERCENTAGE = 33
    STAT_HP_FIXED = 34
    STAT_MP = 35
    STAT_MP_PERCENTAGE = 36


class SpecVector(list):
    """모든 스펙 요소는 SpecVector의 합으로 이루어짐

    Args:
        list (_type_): CoreStat 요소로 이루어진 1차원 벡터
    """    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _ in range(len(CoreStat)):
            self.append(0)

    def __getitem__(self, key:CoreStat):
        if not isinstance(key, CoreStat):
            raise KeyError(f"Invalid key: {key}")
        return super().__getitem__(key.value)

    def __setitem__(self, key:CoreStat, value:int):
        if not isinstance(key, CoreStat):
            raise KeyError(f"Invalid key: {key}")
        
        if not self.IsValidStat(key,value):
            raise ValueError("Value error: Value out of range")
        
        super().__setitem__(key.value, value)

    def __add__(self, other):
        """ + 연산자를 오버로딩함. 벡터처럼 더하는 연산 제공.
            Args:
                other (SpecVector): The other SpecVector instance to be added to the current instance.

            Raises:
                ValueError: If the 'other' argument is not an instance of SpecVector.

            Returns:
                SpecVector: A new SpecVector instance that is the result of the vector addition of the current instance and the 'other' instance. For each element in the SpecVector, if both corresponding elements in the current instance and the 'other' instance are zero, the element in the result will be zero. Otherwise, the element in the result will be the sum of the corresponding elements in the current instance and the 'other' instance. For the IGNORE_GUARD_PERCENTAGE and FINAL_DAMAGE_PERCENT elements, special calculations are performed instead of simple addition.

            Note:
                This method includes an optimization that avoids performing calculations for elements where both corresponding elements in the current instance and the 'other' instance are zero. This can reduce computational cost when dealing with large SpecVector instances where many of the values are zero.
            """  
        if not isinstance(other, SpecVector):
            raise ValueError("Can only add two SpecVectors")
        
        result = SpecVector()

        for i in CoreStat:
            # 최적화를 위한 조건문
            if self[i] != 0 or other[i] != 0:
                # 방무, 최종뎀 추가연산
                if i == CoreStat.IGNORE_GUARD_PERCENTAGE:
                    result[i] = self.CalcIgnoreGuardPercent(self[i], other[i])
                elif i == CoreStat.FINAL_DAMAGE_PERCENT:
                    result[i] = self.CalcFinalDamagePercent(self[i], other[i])
                else:
                    result[i] = self[i] + other[i]
        return result

    def __iadd__(self, other):
        """ += 연산자를 오버로딩함. 벡터처럼 더하는 연산 제공.
            Args:
                other (SpecVector): The other SpecVector instance to be added to the current instance.

            Raises:
                ValueError: If the 'other' argument is not an instance of SpecVector.

            Note:
                This method updates the current instance instead of returning a new instance. For each element in the SpecVector, if both corresponding elements in the current instance and the 'other' instance are zero, the element in the current instance will be unchanged. Otherwise, the element in the current instance will be updated to be the sum of its original value and the corresponding element in the 'other' instance. For the IGNORE_GUARD_PERCENTAGE and FINAL_DAMAGE_PERCENT elements, special calculations are performed instead of simple addition.

                This method includes an optimization that avoids performing calculations for elements where both corresponding elements in the current instance and the 'other' instance are zero. This can reduce computational cost when dealing with large SpecVector instances where many of the values are zero.
        """  
        if not isinstance(other, SpecVector):
            raise ValueError("Can only add two SpecVectors")

        for i in CoreStat:
            # 최적화를 위한 조건문
            if self[i] != 0 or other[i] != 0:
                # 방무, 최종뎀 추가연산
                if i == CoreStat.IGNORE_GUARD_PERCENTAGE:
                    self[i] = self.CalcIgnoreGuardPercent(self[i], other[i])
                elif i == CoreStat.FINAL_DAMAGE_PERCENT:
                    self[i] = self.CalcFinalDamagePercent(self[i], other[i])
                else:
                    self[i] += other[i]
        return self

    def CalcIgnoreGuardPercent(self, arg1:float , arg2:float) -> float:
        """summary: 두 방어율 무시 수치를 연산함

        Args:\n
            arg1 (float): 첫 번째 방어율 무시 인자\n
            arg2 (float): 두 번째 방어율 무시 인자

        Raises:
            ValueError:\n
            1. 두 인자 중 하나가 주어진 범위를 벗어날 때\n
            2. 인자가 두 개 주어지지 않았을 때

        Returns:\n
            float: 연산된 방어율 수치
        """        
        if arg1 is None or arg2 is None:
            raise ValueError("인자가 반드시 필요합니다.")
        return 100 - ((100 - arg1) * (100 - arg2)) / 100
    
    def CalcFinalDamagePercent(self, arg1:float, arg2:float) -> float:
        """두 최종데미지값을 연산함

        Args:\n
            arg1 (float): 첫 번째 방어율 무시 인자\n
            arg2 (float): 두 번째 방어율 무시 인자

        Raises:
            ValueError:\n
            1. 두 인자 중 하나가 주어진 범위를 벗어날 때\n
            2. 인자가 두 개 주어지지 않았을 때

        Returns:\n
            float: 연산된 최종데미지 수치
        """
        if arg1 is None or arg2 is None:
            raise ValueError("인자가 반드시 필요합니다.")
        return (100 + arg1) * (100 + arg2) / 100 - 100

    def Show(self):
        """SpecVector 내 정보를 보여줌
        """        
        for stat in CoreStat:
            print("{:<30} {}".format(stat.name + ":", self[stat]))

    def Arrange(self):
        """all 스텟 값들을 각 스텟에 더해줌
        """
        all_stat_keys = [CoreStat.STAT_ALL, CoreStat.STAT_ALL_FIXED, CoreStat.STAT_ALL_PERCENTAGE]
        individual_stat_keys = [
            [CoreStat.STAT_STR, CoreStat.STAT_DEX, CoreStat.STAT_INT, CoreStat.STAT_LUK],
            [CoreStat.STAT_STR_FIXED, CoreStat.STAT_DEX_FIXED, CoreStat.STAT_INT_FIXED, CoreStat.STAT_LUK_FIXED],
            [CoreStat.STAT_STR_PERCENTAGE, CoreStat.STAT_DEX_PERCENTAGE, CoreStat.STAT_INT_PERCENTAGE, CoreStat.STAT_LUK_PERCENTAGE]
        ]

        for i, all_stat_key in enumerate(all_stat_keys):
            all_stat_value = self[all_stat_key]
            for individual_stat_key in individual_stat_keys[i]:
                self[individual_stat_key] += all_stat_value
            self[all_stat_key] = 0

    def copy(self):
        result = SpecVector()
        return result + self

    def IsValidStat(self, arg1: CoreStat, arg2:float) -> bool:
        """ CoreStat에 대응하는 Value의 유효성을 간략하게 검사(10만 미만의 값 혹은 100% 이하의 방무)

        Args:
            arg1 (CoreStat): SpecVector의 키 요소
            arg2 (float): SpecVector의 값 요소

        Returns:
            bool: 유효하면 True 반환
        """        
        return (0 <= arg2 <= 100000) and (arg1 not in [CoreStat.IGNORE_GUARD_PERCENTAGE, CoreStat.IGNORE_ELEMENTAL_RESISTANCE] or arg2 <= 100)
    
CreateSpecVector = lambda *args: SpecVector([next((value for stats, value in zip(args[::2], args[1::2]) if e in stats), 0) for i, e in enumerate(CoreStat)])
