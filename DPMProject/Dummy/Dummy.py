from enum import Enum
from Core.Server import GameServer
from Core.SpecElements import SpecVector, CoreStat
from Core.ABCSkill import Skill
from Character.ABCCharacter import ABCCharacter
from Core.Damage import BattlePower
from math import floor
from Skill.Attributes import *
from Core.Condition import ConditionEnum
from collections import defaultdict
from Simulator.DamageLog import DamageLog
import copy


class DummySize(Enum):
    small = 0
    medium = 1
    large = 2

MAX_DAMAGE = 700000000000

class Dummy:
    def __init__(self, Size: DummySize, Level: int, Guard: int, Arcane: int, ElementalResistance: bool, Server: GameServer):
        self.Size = Size
        self.Level = Level
        self.Guard = Guard
        self.Arcane = Arcane
        self.ElementalResistance = ElementalResistance
        self.Server = Server
        self._Condition = defaultdict(int)
        self._DebuffList = list()



    @property
    def Condition(self):
        return self._Condition
    
    def increment_condition(self, cond):
        # 상태이상별 최대 중첩 횟수
        cap = 1
        if cond in [ConditionEnum.빙결]:
            cap = 5

        current = self._Condition[cond]
        self._Condition[cond] = min(current + 1, cap)

    def decrement_condition(self, cond):
        current = self._Condition[cond]
        self._Condition[cond] = max(current - 1, 0)


    @property
    def LevelDiffTable(self):
        """레벨 차이에 따른 데미지 증폭률 반환

        Raises:
            AttributeError: _description_

        Returns:
            _type_: _description_
        """
        if self.Server in [GameServer.NormalServer, GameServer.BurningServer]:
            return [1.1, 1.12, 1.14, 1.16, 1.18, 1.2]
        elif self.Server in [GameServer.RebootServer]:
            return [1.1, 1.12, 1.14, 1.16, 1.18, 1.2]
        else:
            raise AttributeError("서버 설정이 되어있지 않음")
   
    @property
    def Size(self):
        return self._Size

    @Size.setter
    def Size(self, Size: DummySize):
        if not isinstance(Size, DummySize):
            raise TypeError("Size must be an instance of DummySize.")
        self._Size = Size

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level: int):
        if not isinstance(Level, int):
            raise TypeError("Level must be an integer.")
        if Level < 1:
            raise ValueError("Level must be at least 1.")
        self._Level = Level

    @property
    def Guard(self):
        return self._Guard

    @Guard.setter
    def Guard(self, Guard: int):
        if not isinstance(Guard, int):
            raise TypeError("Guard must be an integer.")
        if Guard < 0:
            raise ValueError("Guard must be non-negative.")
        self._Guard = Guard

    @property
    def Arcane(self):
        return self._Arcane

    @Arcane.setter
    def Arcane(self, Arcane: int):
        if not isinstance(Arcane, int):
            raise TypeError("Arcane must be an integer.")
        if Arcane < 0:
            raise ValueError("Arcane must be non-negative.")
        self._Arcane = Arcane

    @property
    def ElementalResistance(self):
        return self._ElementalResistance

    @ElementalResistance.setter
    def ElementalResistance(self, ElementalResistance: int):
        if not isinstance(ElementalResistance, bool):
            raise TypeError("ElementalResistance must be an bool.")
        self._ElementalResistance = ElementalResistance

    @property
    def Server(self):
        return self._Server

    @Server.setter
    def Server(self, Server: GameServer):
        if not isinstance(Server, GameServer):
            raise TypeError("Server must be an instance of GameServer.")
        self._Server = Server

    @property
    def Health(self):
        return self._Health

    @Health.setter
    def Health(self, Health: int):
        if not isinstance(Health, int):
            raise TypeError("Health must be an integer.")
        if Health < 0:
            raise ValueError("Health must be non-negative.")
        self._Health = Health

    
    def TakeAttack(self, char:ABCCharacter, skill:DamageAttribute, add = SpecVector()) -> DamageLog:
        """ 방어율, 속성 저항에 감소되기 전의 데미지를 받음. 

        Args:
            char (ABCCharacter): 허수아비를 공격한 캐릭터
            skill (DamageAttribute): 허수아비를 공격한 스킬
            add (_type_, optional): 해당 스킬에만 적용되는 스펙

        Raises:
            TypeError: _description_

        Returns:
            DamageLog: _description_
        """
        if not issubclass(type(skill), DamageAttribute):
            raise TypeError("공격 스킬의 종류는 DamageAttribute를 상속해야함")
        # 캐릭터의 버프
        buffStat = char.ExtraBuffStat
        # 허수아비의 디버프
        debuffStat = SpecVector()
        for stat in self._DebuffList:
            debuffStat += stat
        

        # 스텟 계산, 데미지p%, 직업상수*무기상수, 숙련도 보정
        preDamage = BattlePower(
            spec=char.TotalSpec + buffStat + debuffStat + add, # 스킬 자체의 버프
            jobtype=char._Job,
            considerGuard=self.Guard,
            isBoss= True,
            elementalResistance= self.ElementalResistance
        ) * char._Constant * (char._Mastery + 100)/200 * skill.DamagePoint/100 

        #  렙차 보정
        preDamage = preDamage * self.LevelDiffTable[char.Level - self.Level]

        # TODO:아케인 포스 보정 단, 현재로써는 1.5배로 고정함
        preDamage = preDamage * 1.5 

        result = DamageLog(
            skill = type(skill),
            damage= min(preDamage, MAX_DAMAGE) * skill.AttackLine,
            original= char.TotalSpec,
            buff=buffStat, 
            debuff=debuffStat,
            add = add
        )
        return result


        
        

        

        
        
    
    
