from Core.SpecElements import *
from Core.ABCItem import ABCItem, ItemParts
from Core.ABCSkill import PassiveSkill, AutomateActivativeSkill, OnPressSkill, Skill, KeydownSkill
from Core.Job import JobType, GetMainStatList, GetSubStatList, JobTypeInfo
from Core.Damage import BattlePower
from Core.Cooldown import Cooldown, verifyCooldown, TIME_UNIT, TIME_ZERO
from abc import ABC, abstractmethod
from Item.ItemSlot import ItemSlot
from Item.ItemSet import ItemSet, ItemSetOptionLevel, ItemSetEnum
from Item.Symbol.ArcaneSymbol import ArcaneSymbol
from Item.Symbol.AuthenticSymbol import AuthenticSymbol
from Item.Weapons.Weapon import GenesisWeapon
from Character.Ability import CharacterAbilityEnum,ABILITY_SLOT_MAX
from Character.Trait import Trait
from Character.Union import Legion, LegionOption, LegionGrade, LEGION_8500_MAX_MEMBER
from Character.FarmMonster import FarmMonster
from Character.Portion import PortionDoping
from Character.Managers import CooldownManager, BuffManager, SummonManager, ProjectileManager
from typing import Dict, List
from Skill.LinkSkill import MAX_LINK_SLOT
from Skill.Attributes import *
from Skill.CommonSkill import 파괴의_얄다바오트
import math
import datetime
import itertools
from sympy import symbols, lambdify
import numpy as np



class InvalidInputException(Exception):
    pass

class AttackType(Enum):
    Physical = 0
    Spell = 1

class CharacterStatus(Enum):
    """캐릭터의 현재 상태에 대한 열거형

    Attributes:
        Idle: 대기 상태
        UsingSkill: 스킬을 사용 중인 상태
        Stunned: 상태이상으로 인해 행동 불가능
        Moving: 이동 중
    """
    Idle = 0
    Using_Skill= 1
    Stunned = 2
    Moving = 3
    Keydown = 4
    
    
class CheckList(Enum):
    성향 = "성향"
    링크 = "링크"
    유니온 = "유니온"
    어빌리티 = "어빌리티"
    아이템_슬롯 = "아이템 슬롯"
    농장 = "농장"
    도핑 = "도핑"
    하이퍼_스텟 = "하이퍼 스텟"
    레벨 = "레벨"
    스킬 = "스킬"


class ABCCharacter(ABC):
    """
    Abstract Base Class (ABC) for a game character.

    This class describes common functions and attributes that game characters should have. 
    The class is intended to be inherited by other classes.

    Attributes:
        _Status (StatusEnum): Current status of the character.
        _Name (str): Name of the character.
        _Level (int): Character's level, an integer between 0 and 300.
        _Job (JobType): Character's job type (e.g., Warrior, Archer).
        _Constant (float): Product of weapon constant and job constant.
        _Mastery (int): Mastery, an integer between 0 and 100.
        _ItemSlot (ItemSlot): Slot for equipped items.
        _AttackType (AttackType): Type of attack (physical damage, magical damage).
        _TotalSpec (SpecVector): Total specification of the character.
        _IsIdle (bool): Whether the character is idle or not.
        _HyperStatPoint (int): Points that can be invested in hyper stats.
        _ArcaneForce (int): Arcane force of the character.
        _AuthenticForce (int): Authentic force of the character.
        _ItemSetOption (ItemSetOptionLevel): Set options for the character's items.
        _LegionPoint (int): Points for the Union's occupation effect.
        _Cooldown (int): Cooldown reduction options that can appear from the hat.
        _CooldownPercent (int): Cooldown reset options that can appear from the farm, abilities, skills, etc.
        _BuffDuration (list[int]): Buff duration increase from the farm, skills, tendencies, Union attack member effect, occupation effect.
        _SummonDuration (int): Summon duration effect that can appear from the farm, skills, Union attack member effect.
        _IsPassiveLevel (bool): Whether passive level 1 options appear in abilities.
        _IsTargetExt (bool): Whether the target increase option appears in the farm and abilities.
        _PersonalTrait (list[Trait]): Personal traits, assumed to be maxed.
        _AbilitySlot (set[CharacterAbilityEnum]): Ability slots of the character.
        _Farm (set[FarmMonsterEnum]): List of farm monsters.
        _LegionList (list): List of Union members.

        # 컴뱃오더스를 포함한 펫버프, 시드링, 특수코어 설정은 Simulation.py 에서 수행            
    """

    # 캐릭터 기본 사항
    _Status: CharacterStatus                 # 현재 캐릭터 상태
    _JobName:str                           # 캐릭터 이름(엔젤릭버스터 등)
    _Level: int                         # 캐릭터 레벨
    _Job:JobType                        # 캐릭터의 직업군(전사, 궁수 등)
    _Constant:float                     # 무기 상수 * 직업 상수
    _Mastery: int                       # 숙련도
    _ItemSlot: ItemSlot                 # 장비 착용 슬롯
    _PetSlot: list                      # 미구현(펫 버프)
    _AttackType: AttackType             # 공격 유형(물리데미지, 마법데미지)
    _TotalSpec: SpecVector
    

    # 파생 스텟
    _HyperStatPoint:int                 # 하이퍼스텟에 투자할 수 있는 포인트
    _ArcaneForce: int                   # 아케인포스
    _AuthenticForce: int                # 어센틱 포스
    _ItemSetOption: ItemSetOptionLevel  # 세트옵션
    _LegionPoint: int                   # 유니온 점령효과 포인트
    
    # 특수 옵션
    
    
    _BuffDuration: list[int]            # 농장, 스킬, 성향, 유니온 공격대원 효과, 점령효과에서 등장하는 버프 지속시간 증가
    _SummonDuration: int                # 농장, 스킬, 유니온 공격대원 효과에서 등장하는 소환수 지속시간 효과
    _IsPassiveLevel: bool               # 패시브 레벨 1 옵션, 어빌리티에서 등장
    _IsTargetExt: bool                  # 타겟수 증가 옵션, 농장과 어빌리티에서 등장        
    
    # 추가적인 스펙업 수단
    _PersonalTrait: list[Trait]             # 성향은 만렙으로 가정함.
    _AbilitySlot: set[CharacterAbilityEnum] # 어빌리티 슬롯
    _LinkSkillSlot: set[Skill]              # 링크 스킬 리스트 - 미구현 
    _Farm: list[FarmMonster]             # 농장 몬스터 목록
    _LegionList: list[Legion]               # 유니온 대원목록
    _PetBuffList: list                      # 미구현(스킬의 리스트로 설정)
    _DopingBuff: list                       # 물약, 스킬에 의한 장시간 지속 버프
    
    # 특수목적 스킬 리스트
    _PassiveSkillList: list
    _AutomateSkillList: list
    _OnPressSkillList: list
    _SkipableSkillList: list

    # 스킬의 지속시간, 쿨타임 관리 매니저
    CooldownManager : CooldownManager
    BuffManager : BuffManager
    SummonManager : SummonManager
    ProjectileManager: ProjectileManager
    
   
    def __init__(self, name:JobName, level:int, job:JobType, constant:float, mastery:int, attacktype:AttackType):
        # Validating name
        assert isinstance(name, JobName), "Name must be a string"

        # Validating level
        if not isinstance(level, int) or level < 0 or level > 300:
            raise InvalidInputException("Level must be an integer between 0 and 300")

        # Validating job
        if not isinstance(job, JobType):
            raise InvalidInputException("Job must be an instance of JobType")

        # Validating constant
        if not isinstance(constant, float) or constant < 0:
            raise InvalidInputException("Constant must be a non-negative integer")

        # Validating mastery
        if not isinstance(mastery, int) or mastery < 0 or mastery > 100:
            raise InvalidInputException("Mastery must be an integer between 0 and 100")

        basic = SpecVector()
        mainstat = GetMainStatList(job)[0]
        basic[mainstat] = 5*level+18-4
        basic[CoreStat.STAT_ALL] = 4
        basic[CoreStat.CRITICAL_PERCENTAGE] = 5
        self._checklist = dict()
        self._JobName = name
        self.Level = level
        self._Job = job
        self._Constant = constant
        self._Mastery = mastery
        self._ItemSlot = ItemSlot()
        self._IsPassiveLevel = False
        self._BuffDuration = 0
        self._PersonalTrait = [t for t in Trait]
        self.AttackType = attacktype
        self._Farm = []
        self._DopingBuff = []
        self._TotalSpec = basic
        self._LinkSkillSlot = set()
        self._SummonDuration = 0
        self._LegionPoint = 0
        self._PassiveSkillList = []
        self._AutomateSkillList = []
        self._OnPressSkillList = []
        self._KeydownSkillList = []
        self._SkipableSkillList = []
        self._OnAttackSkillList = []
        self._IsTargetExt = 0
        

        self._ArcaneForce = 0
        self._AuthenticForce = 0
        self._Status = CharacterStatus.Idle
        self.CooldownManager = CooldownManager()
        self.BuffManager = BuffManager()
        self.SummonManager = SummonManager()
        self.ProjectileManager = ProjectileManager()
        
        self._Delay = Cooldown(milliseconds=0)

        self.SetupPersonalTrait()

    @property
    def Delay(self):
        return self._Delay

    @Delay.setter
    def Delay(self, delay:Cooldown):
        verifyCooldown(delay)
        self._Delay = delay
        

    
    def Tick(self):
        self.CooldownManager.Tick()
        self.BuffManager.Tick()
        summonLog = self.SummonManager.Tick()
        projLog = self.ProjectileManager.Tick()


        self._Delay.update()

        return summonLog + projLog

    def ReadyFor(self, skill:Skill):
        return self.CooldownManager.isReady(skill)

    @property
    def ExtraBuffStat(self):
        """캐릭터의 가동율 있는 버프로 인한 스텟의 합계 반환

        Returns:
            _type_: _description_
        
        """
        # 자동 발동 스킬 리스트로부터 발동조건을 받아옴
        for autoSkill in self._AutomateSkillList:
            # autoSkill은 callable 으로써, Activator 은 클래스 메소드임
            det = autoSkill.active()
            
            if det == True:
                if self.CooldownManager.isReady(autoSkill):
                    self.BuffManager.Add(autoSkill())
                    self.CooldownManager.Count(autoSkill)

        

        return self.BuffManager.GetBuff()

       

    @property
    def SetupCheckList(self):
        """캐릭터 스펙 요소가 적절히 적용되었는지 확인하는 체크리스트

        Returns:
            _type_: _description_
        """
        return self._checklist
    
    @SetupCheckList.setter
    def SetupCheckList(self, key:CheckList):
        if not isinstance(key, CheckList):
            raise TypeError("key must be a instance of CheckList")
        self._checklist.update({key:True})

    @property
    def Level(self):
        """캐릭터의 레벨을 반환함

        Returns:
            _type_: _description_
        """
        return self._Level

    @Level.setter
    def Level(self, level):
        if not isinstance(level, int) or level < 0 or level > 300:
            raise InvalidInputException("Level must be an integer between 0 and 300")
        self._Level = level
        self._HyperStatPoint = self.GetHyperStatPoint()
        self.SetupCheckList = CheckList.레벨

    
    @property
    def Status(self):
        """캐릭터의 현재 상태를 나타냄

        Returns:
            StatusEnum : 캐릭터의 현재 상태를 나타내는 열거형
        """
        if self._Delay > TIME_ZERO:
            return CharacterStatus.Using_Skill
        elif self._Delay == TIME_ZERO:
            return CharacterStatus.Idle

    @property
    def FarmList(self):
        """적용된 농장의 몬스터 리스트

        Returns:
            set[FarmMonster]: 농장 몬스터 리스트
        """
        return self._Farm
    
    @FarmList.setter
    def FarmList(self, farmlist:list):
        if not isinstance(farmlist, list) or not isinstance(farmlist[0], FarmMonster):
            raise TypeError("farmlist must be list of FarmMonster")
        
        if len(farmlist) > 18:
            raise ValueError("maximum monster cap is 18")

        self._Farm = farmlist
        if self.SetupFarm():
            self.SetupCheckList = CheckList.농장
        else:
            raise AttributeError("농장 초기화 실패")

    def SetupFarm(self) -> bool:
        """농장의 몬스터 효과를 적용시킴

        Returns:
            bool: 적용의 성공 여부
        """
        for monster in self.FarmList:
            if isinstance(monster.value, SpecVector):
                self.TotalSpec += monster.value
            elif monster in [FarmMonster.쁘띠_루미너스_이퀄리브리엄]:
                self.TotalSpec[CoreStat.ATTACK_PHYSICAL_FIXED] = self.TotalSpec[CoreStat.ATTACK_PHYSICAL_FIXED] + self.Level//20
                self.TotalSpec[CoreStat.ATTACK_SPELL_FIXED] = self.TotalSpec[CoreStat.ATTACK_SPELL_FIXED] + self.Level//20
            elif monster in [
                FarmMonster.사랑에_빠진_커플예티,
                FarmMonster.빅_펌킨
            ]:
                self._SummonDuration += int(monster.value/10)
            elif monster in [
                FarmMonster.쁘띠_아카이럼,
                FarmMonster.반반,
                FarmMonster.군단장_윌
            ]:
                self._BuffDuration += int(monster.value//10)
            elif monster in [
                FarmMonster.큰_운영자의_벌룬,
                FarmMonster.쁘띠_은월
            ]:
                self.CooldownManager.Reset += monster.value
            elif monster in [FarmMonster.쁘띠_루미너스]:
                self._IsTargetExt += 1
            else:
                return False
        return True
   
    @property
    def TotalSpec(self):
        """캐릭터의 총 스펙을 나타냄

        Returns:
            _type_: _description_
        """
        self._TotalSpec.Arrange()
        return self._TotalSpec
    
    @TotalSpec.setter
    def TotalSpec(self,spec:SpecVector):
        determine = self._TotalSpec
        self._TotalSpec = spec
        for stat in CoreStat:
            if determine[stat] > self._TotalSpec[stat]:
                raise ValueError("Spec 값에 원치 않는 값을 대입함")

    @property
    def AttackType(self):
        """캐릭터의 공격 유형을 나타냄

        Returns:
            AttackType: 공격 유형 정보를 담은 열거형
        """
        return self._AttackType
    
    @AttackType.setter
    def AttackType(self, type:AttackType):
        if not isinstance(type, AttackType):
            raise TypeError("type must be AttackType type")
        self._AttackType = type

    @property
    def CharItemSlot(self):
        """캐릭터가 장비하는 아이템 슬롯

        Returns:
            _type_: _description_
        """
        return self._ItemSlot
    
    @property
    def MainStat(self):
        main = GetMainStatList(self._Job)
        return main

    @CharItemSlot.setter
    def CharItemSlot(self, slot:ItemSlot):
        """캐릭터의 아이템 슬롯. 아이템을 착용하자 마자 효과 적용함

        Args:
            slot (ItemSlot): 착용중인 장비 묘사

        Raises:
            InvalidInputException: _description_
            AttributeError: _description_
        """
        if not isinstance(slot, ItemSlot):
            raise InvalidInputException("slot must be an instance of ItemSlot")
        
        for parts, itemlist in slot:
            for item in itemlist:
                # 아이템 슬롯에 아이템 추가함
                self.AddItemToSlot(item)

        self._ItemSlot = slot
        # 아이템 슬롯에 있는 아이템 효과를 적용함
        if self.SetupItemSlotSpec():
            self.SetupCheckList = CheckList.아이템_슬롯
        else:
            raise AttributeError("아이템 슬롯 세팅 오류")
    
    def AddItemToSlot(self, item: ABCItem):
        """슬롯에 아이템을 추가합니다.
        
        Args:
            item (ABCItem): 추가할 아이템 객체

        Raises:
            InvalidInputException: 아이템이 유효하지 않을 경우 발생합니다.
        """
        if not isinstance(item, ABCItem):
            raise InvalidInputException("아이템은 ABCItem의 인스턴스여야 합니다.")
        # 아이템을 슬롯에 추가합니다.
        self._ItemSlot.AddItem(item.ItemPart, item)

    def SetupItemSlotSpec(self) -> bool:
        """아이템 효과를 적용시킵니다

        Raises:
            TypeError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        belongedItemSetList = ItemSetOptionLevel()
        for parts, itemlist in self._ItemSlot:
            # 한 부위에 2가지 이상의 아이템이 있을 수 있으므로 파트:리스트[아이템] 임
            # 예를 들어 펜던트 반지, 펫장비 등등
            for item in itemlist:
                # 아이템 스펙을 total spec에 더해줌
                itemStat, cool = item.TotalSpec()
                self.TotalSpec += itemStat
                self.CooldownManager.Cap += cool

                # 세트 옵션 누적 카운팅
                if item.BelongedSet is not None:
                    belongedItemSetList[item.BelongedSet] += 1

                # 아케인 심볼을 집산함
                if parts in [ItemParts.Symbol]:
                    if isinstance(item, ArcaneSymbol):
                        self._ArcaneForce += item.GetForce()
                    elif isinstance(item, AuthenticSymbol):
                        self._AuthenticForce += item.GetForce()
                    else:
                        raise TypeError("심볼 아이템이 아니므로 포스를 얻을 수 없음")
                    
                # 제네무기 처리 로직. 추후 수정 필요함
                if issubclass(type(item), GenesisWeapon):
                    self.SetSkill(파괴의_얄다바오트())
                    # 제대로된 로직은 아니지만, 현재 럭키아이템은 제네무기만 취급하고, 루타비스만 증가함
                    belongedItemSetList[ItemSetEnum.Rootabyss] += 1
                    


        # 세트옵션을 적용
        for set in ItemSetEnum:
            if set == ItemSetEnum.Lucky:
                continue
            itemset = ItemSet(self._Job)

            itemStat = SpecVector()
            if belongedItemSetList[set] != 0:
                itemStat = itemset[set][belongedItemSetList[set]-1]
                
            if isinstance(itemStat, SpecVector):
                self.TotalSpec += itemStat
            else:
                raise ValueError("더하는 값이 스펙 벡터가 아님")
        
        return True
       
    # 성향 스펙을 적용함        
    def SetupPersonalTrait(self) -> bool:
        """성향 시스템 효과를 적용함

        Returns:
            bool: 성공 여부
        """
        for t in Trait:
            # 카리스마, 통찰력, 의지
            if isinstance(t.value, SpecVector):
                self.TotalSpec += t.value
            elif t in [Trait.감성]:
                self._BuffDuration += t.value
            else:
                pass
                
        self.SetupCheckList = CheckList.성향
        return True

    @property
    def AbilitySlot(self):
        """캐릭터에 적용중인 어빌리티 목록

        Returns:
            _type_: _description_
        """
        return self._AbilitySlot

    
    @AbilitySlot.setter
    def AbilitySlot(self, slot:list[CharacterAbilityEnum]):
        """ 어빌리티 슬롯을 설정함. 설정함과 함께 효과 적용

        Args:
            slot (list[CharacterAbilityEnum]): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            AttributeError: _description_
        """
        if len(slot) > ABILITY_SLOT_MAX:
            raise ValueError(f"어빌리티 슬롯 최대 갯수는{ABILITY_SLOT_MAX}개")
        for abil in slot:
            if not isinstance(abil, CharacterAbilityEnum):
                raise ValueError("어빌리티 자료형 CharacterAbilityEnum이 아님")
        
        self._AbilitySlot = slot
        if self.SetupAbilitySlot():
            self.SetupCheckList = CheckList.어빌리티
        else:
            raise AttributeError("어빌리티 설정 실패")
        
    # 어빌리티 슬롯을 스펙에 적용함
    def SetupAbilitySlot(self) ->bool:
        """어빌리티의 효과를 적용함

        Raises:
            TypeError: _description_

        Returns:
            bool: _description_
        """
        stat = SpecVector()
        for i, e in enumerate(self._AbilitySlot):
            value = e.value[max(1, len(e.value)-i-1)]
            if e in [CharacterAbilityEnum.BossDamage]:
                stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = value
            elif e in [CharacterAbilityEnum.BuffDuration]:
                self._BuffDuration += value
            elif e in [CharacterAbilityEnum.CooldownReset]:
                self.CooldownManager._Reset += value
            elif e in [CharacterAbilityEnum.CriticalProp]:
                stat[CoreStat.CRITICAL_PERCENTAGE] = value
            # 상태이상시 추가데미지지만, 모법링크가 있으면 데미지로 치환할 수 있음
            elif e in [CharacterAbilityEnum.PanicDamage]:           
                # if 링크스킬에 모법 링크가 있다면(링크스킬 구현시 수정)
                stat[CoreStat.DAMAGE_PERCENTAGE] = value
            elif e in [CharacterAbilityEnum.PassiveLevel]:
                self._IsPassiveLevel = True
            elif e in [CharacterAbilityEnum.TargetExtension]:
                self._IsTargetExt = True
            else:
                raise TypeError("어빌리티 적용에 오류가 발생")
        
        self.TotalSpec += stat
        return True

    # 총 하이퍼스텟 포인트를 반환. 하이퍼스텟 일반식을 이용
    
    def GetHyperStatPoint(self) -> int:
        first_digit = int(str(self._Level)[-1])
        rest = int((self._Level - first_digit) / 10) - 12
        self.SetupCheckList = CheckList.하이퍼_스텟
        return 5*(rest-2)*(rest+3) + (rest+1)*(first_digit+1)

    # 하이퍼스텟을 모두 사용하는 경우의 수를 만들어냄
    def HyperStatCaseGeneration(self) -> list:
        # 다이나믹 프로그래밍을 할 수 없는 이유는 해당 스텟들의 증가가 선형적이지 않고, 교환법칙 성립하지 않기 때문임
        # 그리디 알고리즘또한 최적성을 보장해주지 못함
        # 특정 스펙에 대한 최적화 알고리즘은 쉽지만 딜사이클의 데미지, 방무등에 따라서 최적의 해가 바뀌므로 전수조사하기로 결정
        POINTS_REQUIRED = [0, 1, 3, 7, 15, 25, 40, 60, 85, 115, 150, 200, 265, 345, 440, 550]
        # 크확 투자
        # 필요한 크확을 구하여 스펙에 대입 하이퍼스텟 5레벨부터는 유니온에비해 효율이 낮으므로 패스함.
        if self._Job == JobType.Bowman:
            requireCritical = 15
        else:    
            requireCritical = min(5,100 - self.TotalSpec[CoreStat.CRITICAL_PERCENTAGE])
        self._TotalSpec[CoreStat.CRITICAL_PERCENTAGE] += requireCritical
        # 필요한 크확을 충족하는 하이퍼 레벨을 구함
        hyperCritProp = math.ceil((requireCritical + min(6, requireCritical))//2)
        # 필요한 하이퍼레벨을 찍고 그만큼 하이퍼스텟 포인트 차감함
        point = self.GetHyperStatPoint() - POINTS_REQUIRED[hyperCritProp]

        hyperset = set()
        # 연산량을 줄이기 위해서 옵션별로 루프의 상한선, 하한선을 설정함
        mainstatCap = 5
        substatCap = 2
        critBody = 10
        ignoreBody = 8
        damageBody = 11
        bossBody = 12
        atkCap = 7
        for a, mainstat in enumerate(POINTS_REQUIRED[:mainstatCap]):
            aa = mainstat
            if aa <= point:
                for b, substat in enumerate(POINTS_REQUIRED[:substatCap]):
                    bb = aa + substat
                    if bb <= point:
                        for c, crit in enumerate(POINTS_REQUIRED[critBody:]):
                            cc = bb + crit
                            if cc<=point:                        
                                for d, ignore in enumerate(POINTS_REQUIRED[ignoreBody:]):
                                    dd = cc + ignore
                                    if dd <= point:
                                        for e, damage in enumerate(POINTS_REQUIRED[damageBody:]):
                                            ee = dd + damage
                                            if ee <= point:                                
                                                for f, boss in enumerate(POINTS_REQUIRED[bossBody:]):
                                                    ff = ee + boss
                                                    if ff <= point:
                                                        for g, atk in enumerate(POINTS_REQUIRED[:atkCap]):
                                                            gg = ff + atk

                                                            if  point - gg < (POINTS_REQUIRED[g+1] - POINTS_REQUIRED[g]):
                                                                hyperset.add(tuple(self.HyperToSpec([a,b,c + critBody,d + ignoreBody,e+damageBody,f+bossBody,g])))
                                                                break
                                                            elif point - gg == (POINTS_REQUIRED[g+1] - POINTS_REQUIRED[g]):
                                                                hyperset.add(tuple(self.HyperToSpec([a,b,c + critBody,d+ ignoreBody,e+damageBody,f+bossBody,g+1])))
                                                                break
                                                            
                                                    else:
                                                        if f != 0:
                                                            hyperset.add(tuple(self.HyperToSpec([a,b,c + critBody,d+ ignoreBody,e+damageBody,f-1+bossBody,0])))
                                                        break
                                            else:
                                                #hyperset.append(self.HyperToSpec([a,b,c,d,e-1,0,0]))
                                                break
                                    else:
                                        #hyperset.append(self.HyperToSpec([a,b,c,d-1,0,0,0]))
                                        break
                            else:
                                #hyperset.append(self.HyperToSpec([a,b,c-1,0,0,0,0]))
                                break
                    else:
                        #hyperset.append(self.HyperToSpec([a,b-1,0,0,0,0,0]))
                        break
            else:
                #hyperset.append(self.HyperToSpec([a-1,0,0,0,0,0,0]))
                break
        result = []
        for hyper in hyperset:
            result.append(SpecVector(hyper))

        return result
        


    def HyperToSpec(self, hyper:list)->SpecVector:
        """하이퍼 스펙 포인트를 스펙 벡터로 변환해줌

        Args:
            hyper (list): 하이퍼 스텟 레벨 정보를 담은 리스트

        Raises:
            KeyError: _description_

        Returns:
            SpecVector: 하이퍼 스텟에 대응하는 벡터
        """
        result = SpecVector()
        MainStatList = GetMainStatList(self._Job)
        SubStatList = GetSubStatList(self._Job)
        
        if self._Job == JobType.Xenon:
            pass
        elif MainStatList[0] == CoreStat.STAT_STR:
            #전사, 힘해적
            pass
        elif MainStatList[0] == CoreStat.STAT_DEX:
            #궁수, 덱해적
            pass
        elif MainStatList[0] == CoreStat.STAT_INT:
            result[CoreStat.STAT_INT_FIXED] = 30*hyper[0]
            result[CoreStat.STAT_LUK_FIXED] = 30*hyper[1]
        elif MainStatList[0] == CoreStat.STAT_LUK:
            # 도적, 힘도적
            pass
        elif MainStatList[0] == CoreStat.STAT_HP:
            # 데벤
            pass

        result[CoreStat.CRITICAL_DAMAGE] = hyper[2]
        result[CoreStat.IGNORE_GUARD_PERCENTAGE] = 3 * hyper[3]
        result[CoreStat.DAMAGE_PERCENTAGE] = 3 * hyper[4]
        if 4 * hyper[5] - min(5, hyper[5]) < 0:
            raise KeyError("")
        result[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 4 * hyper[5] - min(5, hyper[5])
        result[CoreStat.ATTACK_PHYSICAL] = 3 * hyper[6]
        result[CoreStat.ATTACK_SPELL] = 3 * hyper[6]

        return result

    @property
    def LegionList(self):
        """캐릭터에 적용중인 유니온 공격대원 목록

        Returns:
            _type_: _description_
        """
        return self._LegionList
    
    @LegionList.setter
    def LegionList(self, memberlist:list):
        """유니온 목록을 설정하고, 효과를 적용시킴

        Args:
            memberlist (list): 유니온 대원효과 정보를 담은 리스트

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            AttributeError: _description_
        """
        if not isinstance(memberlist, List):
            raise ValueError("유니온 멤버 리스트는 리스트형식")
        
        for member in memberlist:
            if not isinstance(member, Legion):
                raise ValueError("유니온 대원 리스트 멤버는 Legion")
            
        # 현재 기준 dpm 스펙은 유니온 8500, SSS 3종류
        if len(memberlist) > LEGION_8500_MAX_MEMBER:
            raise ValueError("유니온 점령은 최대 37캐릭터(유니온 8500 기준")
        
        self._LegionList = memberlist
        # 유니온 대원 효과를 적용시킴
        if self.SetupUnion():
            self.SetupCheckList = CheckList.유니온
        else:
            raise AttributeError("유니온 설정 실패")
 
    def SetupUnion(self) -> bool:
        """ 유니온 대원 효과를 적용함

        Raises:
            AttributeError: _description_
            AttributeError: _description_

        Returns:
            bool: 성공여부
        """
        
        if len(self._LegionList) < 2:
            raise AttributeError("유니온 셋팅은 멤버 리스트 설정 이후에 가능")

        memberCount = LEGION_8500_MAX_MEMBER
        for member in self._LegionList:
            optionType = member.value.Option
            effect = optionType.value[0]
            if isinstance(effect, SpecVector):
                self.TotalSpec += effect
            elif optionType == LegionOption.SummonDuration:
                self._SummonDuration += effect
            elif optionType == LegionOption.CooldownPercent:
                self.CooldownManager.Mercedes += effect
            elif optionType == LegionOption.BuffDuration:
                self._BuffDuration += effect
            elif optionType == LegionOption.WildHunter:
                # 와일드헌터 20% 확률로 데미지 16~020% 증가. 일단 3.2%로 가정
                self.TotalSpec += CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 3.2)
            else:
                raise AttributeError("유니온 대원 효과 오류")
            
            if member.value.Grade == LegionGrade.SSS:
                self._LegionPoint += 1
            else:
                pass
        self._LegionPoint += memberCount * 4
        return True

    @property
    def LinkSkillSlot(self):
        """캐릭터에 적용중인 링크 스킬 목록

        Returns:
            _type_: _description_
        """
        return self._LinkSkillSlot
    
    @LinkSkillSlot.setter
    def LinkSkillSlot(self, skillSet: set):
        """링크 스킬 슬롯을 설정하고, 효과를 적용시킴

        Args:
            skillSet (set): _description_

        Raises:
            AttributeError: _description_
            AttributeError: _description_
            AttributeError: _description_

        Returns:
            _type_: _description_
        """
        if not isinstance(skillSet, set):
            raise("skilSset must be list type")
        
        if len(skillSet) > MAX_LINK_SLOT + len(self.LinkSkillSlot):
            raise("SkillSet must have 12 elements")

        for i, skill in enumerate(skillSet):
            if not issubclass(skill, Skill):
                raise AttributeError("skillSet elements are not subclass of Skill")
            self._LinkSkillSlot.add(skill)
        
        if len(self._LinkSkillSlot) == MAX_LINK_SLOT:
            # 링크 스킬 효과 적용
            if self.SetupLinkSkill():
                self.SetupCheckList = CheckList.링크
                return True
            else:
                raise AttributeError("링크스킬 설정 오류")
        else:
            raise AttributeError("링크 스킬의 갯수가 13개가 아님")
        

    
    def SetupLinkSkill(self) -> bool:
        """ 링크 스킬을 캐릭터에 적용함

        Returns:
            bool: _description_
        """
        self.SetSkillList(list(self.LinkSkillSlot))
        return True
    
    @property
    def DopingBuff(self):
        """캐릭터에 적용중인 도핑 리스트

        Returns:
            _type_: _description_
        """
        return self._DopingBuff
    
    @DopingBuff.setter
    def DopingBuff(self, portionlist):
        """도핑 버프 적용

        Args:
            portionlist (SpecVector)): 포션 효과

        Raises:
            TypeError: _description_
            AttributeError: _description_
        """
        for buff in portionlist:
            if not isinstance(buff, PortionDoping):
                raise TypeError("instance is not PortionDoping type")
        
        self._DopingBuff = portionlist
        # 도핑 효과를 적용함
        if self.SetupDoping():
            self.SetupCheckList = CheckList.도핑
        else:
            raise AttributeError("도핑 적용 실패")

    def SetupDoping(self) -> bool:
        """도핑 효과를 적용함

        Raises:
            TypeError: _description_

        Returns:
            bool: _description_
        """
        for buff in self._DopingBuff:
            if isinstance(buff.value, SpecVector):
                self.TotalSpec += buff.value
            else:
                raise TypeError("버프 자료형은 SpecVector")
        return True

    def SetSkillList(self, skillList:list):
        """스킬을 리스트를 입력받아 스킬을 저장

        Args:
            skillList (list): _description_
        """
        for skill in skillList:
            self.SetSkill(skill)
        self.SetupCheckList = CheckList.스킬
        
    def SetSkill(self, skill:Skill):
        """스킬을 입력받아 적절한 유형의 스킬 리스트에 추가하고, 패시브는 즉시 적용함

        Args:
            skill (Skill): _description_

        Raises:
            TypeError: _description_
            AttributeError: _description_
        """
        if not issubclass(skill, Skill):
            raise TypeError("스킬 자료형이 아님")
        
        if issubclass(skill, PassiveSkill):
            self._PassiveSkillList.append(skill)
            skill = skill()
            skill.Owner = self
            if issubclass(type(skill), CombatOrdersAttribute):
                skill.ApplyCombat(isOriginal= (self._JobName == JobName.Paladin))

            if hasattr(skill, 'BuffStat'):
                self._TotalSpec += skill.BuffStat
            if issubclass(type(skill), MasteryAttribute):
                self._Mastery += skill.Mastery
            if issubclass(type(skill), BuffDurationAttribute):
                self._BuffDuration += skill.BuffDurationOption

            
    
        elif issubclass(skill, AutomateActivativeSkill):
            self._AutomateSkillList.append(skill)
        elif issubclass(skill, OnPressSkill):
            self._OnPressSkillList.append(skill)
            if issubclass(skill, SkipableAttribute):
                self._SkipableSkillList.append(skill)
        elif issubclass(skill, KeydownSkill):
            self._KeydownSkillList.append(skill)
        else:
            raise AttributeError("Skill의 형태가 허용되지 않은 형태임")
    
    def Optimization(self, weapon:bool, hyper:bool, printing:bool):
        # 최적화 항목
        # 1. 무보엠
        # 2. 링크 스킬
        # 3. 반빨별 vs 고관비 vs 명장 버프
        # 4. 하이퍼 스텟
        # 5. 유니온 점령효과
        # 6. 하이퍼 스킬 - 패시브 : 이건 당장은 계획 없음.
        # 7. 딜사이클 - simulation.py에서 수행 예정
        # 8. 쿨감효과
        PrintResult = printing

        if len(self.SetupCheckList) != len(CheckList):
            raise AttributeError("최적화 진행하기 전에 셋업 체크리스트를 완료해야함")

        start = datetime.datetime.now()
        # 1. 무보엠 구하기
        weaponList = self.WeaponPotentialCaseGeneration()
        weapontime = datetime.datetime.now()
        if PrintResult:
            print(f"무보엠 계산: {(weapontime - start).total_seconds()}")

        if weapon == False:
            # 빠른 빌드를 위해 쓸만한 잠재를 임시로 사용함
            instanceWeapon = SpecVector()
            instanceWeapon[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 130
            instanceWeapon[CoreStat.IGNORE_GUARD_PERCENTAGE] = 40
            instanceWeapon[CoreStat.ATTACK_SPELL_PERCENTAGE] = 39
            instanceWeapon[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = 39
            weaponList = [instanceWeapon]

        # 번외) 장갑 에디 - 궁수용
        
        # 2. 링크스킬 -> 일단 이건 고정함(너무 리소스 많이듬)
        
        # 3. 도핑 -> 이것도 일단 패스
        
        # 5. 하이퍼 스텟
        hyperlist = self.HyperStatCaseGeneration()
        
        if hyper == False:
            # 빠른 빌드를 위해 적당한 하이퍼스텟 주어진대로 대입
            instancehyper = SpecVector()
            instancehyper[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 47
            instancehyper[CoreStat.DAMAGE_PERCENTAGE] = 33
            instancehyper[CoreStat.ATTACK_SPELL] = 18
            instancehyper[CoreStat.IGNORE_GUARD_PERCENTAGE] = 42
            instancehyper[CoreStat.CRITICAL_DAMAGE] = 11
            instancehyper[CoreStat.STAT_ALL_FIXED] = 120
            
            hyperlist = [instancehyper]
            

        hypertime = datetime.datetime.now()
        if PrintResult:
            print(f"하이퍼스텟 계산: {(hypertime - weapontime).total_seconds()}")


        # 4. 유니온 점령효과
        # 특수 점령효과를 위한 길목, 크뎀, 필요하다면 벞지를 적용 후 남은 포인트 반환
        unionrestpoint = self.PartialApplyUnion(self._LegionPoint)
        
        uniontime = datetime.datetime.now()
        if PrintResult:
            print(f"유니온 효과 계산: {(uniontime - hypertime).total_seconds()}")

        
        MaxScore = 0
        result = []
        totalCount = len(weaponList) * len(hyperlist)
        rest = 0
        # 유니온 스텟의 경우 순서 상관 없고, 방무 제외하면 선형적으로 증가함
        # 또한, 유니온 스텟까지 최적화 진행하게 되면 연산량이 너무 많음
        # 그리디 알고리즘으로 최적화 진행해도 높은 수준으로 최적의 해 설정함
        for weapon in weaponList:
            for hyper in hyperlist:
                unionStat = SpecVector()
                tryingStat = self.TotalSpec + weapon + hyper
                # 유니온 포인트를 사용하여 유니온 점령효과에 투자함    
                unionStat = self.GetNextUnionLevelup(tryingStat, unionrestpoint)

                rest += 1
                bp = BattlePower(    
                    spec=tryingStat + unionStat,
                    jobtype=self._Job,
                    # 임시로 방무 300 기준 최적 하이퍼스텟 설정
                    considerGuard= 300,
                    isBoss=True
                )
                if MaxScore < bp:
                    result = [weapon, hyper, unionStat]
                    
                    MaxScore = bp
                    
                    if PrintResult:
                        print(f"진행율: {(rest/totalCount)*100}")
                        weapon.Show()
                        hyper.Show()
                        unionStat.Show()

        
            print("무기")
            result[0].Show()
            print("hyper")
            result[1].Show()
            print("union")
            result[2].Show()
            print(f"MAxScore: {MaxScore}")
            
        self.TotalSpec += result[0] + result[1] + result[2]
        totalTime = datetime.datetime.now()
        if PrintResult:
            print(f"총 소요시간: {(totalTime - start).total_seconds()}")
        

    def GetNextUnionLevelup(self, nowstat:SpecVector, point:int) -> SpecVector:
        # 미분식을 활용해 greedy한 탐색으로 유니온 포인트 배정
        # 심볼 생성
        atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_per, substat_fixed, damage_total, ignore_now, ignore_add = symbols('a b c d e f g h i j')
        # 식 정의
        y = atk*(4*(mainstat*(1+0.01*mainstat_per) +mainstat_fixed)+substat*(1+0.01*substat_per)+substat_fixed)*(1+0.01*damage_total)*(100-3*(100-ignore_now)*(100-ignore_add)/100)/100
        # 각 변수에 대한 편미분
        diff_atk = y.diff(atk)
        diff_mainstat = y.diff(mainstat)
        diff_damage = y.diff(damage_total)
        diff_ignore = y.diff(ignore_add)

        # 각 편미분 결과를 함수로 변환
        f_atk = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_per, substat_fixed, damage_total, ignore_now, ignore_add), diff_atk, "numpy")
        f_mainstat = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_per, substat_fixed,damage_total, ignore_now, ignore_add), diff_mainstat, "numpy")
        f_g = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_per, substat_fixed,damage_total, ignore_now, ignore_add), diff_damage, "numpy")
        f_i = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_per, substat_fixed, damage_total, ignore_now, ignore_add), diff_ignore, "numpy")

        atkconst =0
        mainstatconst = 0
        mainstatper = 0
        mainstatfixed = 0
        substatconst = 0
        substatfixed = 0
        substatper = 0

        atktype = None
        main = None
        if self._Job == JobType.Magician:
            main = CoreStat.STAT_INT
            atktype = CoreStat.ATTACK_SPELL
            atkconst = nowstat[CoreStat.ATTACK_SPELL]
            mainstatconst = nowstat[CoreStat.STAT_INT]            
            mainstatper = nowstat[CoreStat.STAT_INT_PERCENTAGE]
            mainstatfixed = nowstat[CoreStat.STAT_INT_FIXED]
            substatconst = nowstat[CoreStat.STAT_LUK]            
            substatper = nowstat[CoreStat.STAT_LUK_PERCENTAGE]
            substatfixed = nowstat[CoreStat.STAT_LUK_FIXED]

        elif self._Job == JobType.Bowman:
            main = CoreStat.STAT_DEX
            atktype = CoreStat.ATTACK_PHYSICAL
            
            mainstatconst = nowstat[CoreStat.STAT_DEX]            
            mainstatper = nowstat[CoreStat.STAT_DEX_PERCENTAGE]
            mainstatfixed = nowstat[CoreStat.STAT_DEX_FIXED]
            substatconst = nowstat[CoreStat.STAT_STR]            
            substatper = nowstat[CoreStat.STAT_STR_PERCENTAGE]
            substatfixed = nowstat[CoreStat.STAT_STR_FIXED]
            atkconst = nowstat[CoreStat.ATTACK_PHYSICAL]
        else:
            raise ValueError("설정안했지 미래의나 ")
        
        damageconst = nowstat[CoreStat.DAMAGE_PERCENTAGE_BOSS] + nowstat[CoreStat.DAMAGE_PERCENTAGE]
        ignorenow = nowstat[CoreStat.IGNORE_GUARD_PERCENTAGE]

        
        
        result = SpecVector()
        
        levelupStat = [0,0,0,0]
        # 공, 주스텟, 데미지, 방무 각각의 미분값을 보고 포인트 투자함
        for _ in range(0, point):
            args = (atkconst+levelupStat[0], mainstatconst+levelupStat[1], mainstatper, mainstatfixed, substatconst, substatper, substatfixed, damageconst+levelupStat[2],ignorenow, levelupStat[3])
            resultatk = f_atk(*args)
            resultmainstat = f_mainstat(*args)*5
            resultdamage = f_g(*args)
            resultIgnore = f_i(*args)

            identify = np.array([resultatk, resultmainstat, resultdamage, resultIgnore])
            position = np.argsort(identify)[::-1]

            for pos in position:
                # 스텟당 40칸까지 점령 가능
                if levelupStat[pos] < 40:
                    levelupStat[pos] += 1
                    break
        for i, stat in enumerate([atktype, main, CoreStat.DAMAGE_PERCENTAGE_BOSS, CoreStat.IGNORE_GUARD_PERCENTAGE]):
            if stat in [CoreStat.STAT_STR,CoreStat.STAT_DEX, CoreStat.STAT_INT, CoreStat.STAT_LUK]:
                result[stat] = levelupStat[i] * 5
            else:
                result[stat] = levelupStat[i]

        
        return result
        


    def PartialApplyUnion(self, Point:int) -> list:
        # 중앙 점령지역(2) + 주요 스펙에 접근하기 위한 다리(10) + 크뎀(40) + 보공,벞지,방무,공격력
        UnionSpecVector = SpecVector()
        LPoint = Point
        MaxArea = 40

        requiredCrit = 0
        # 부족한 크확 충당함
        if self._Job == JobType.Bowman:
            requiredCrit = 20
        else:
            requiredCrit = 100-self._TotalSpec[CoreStat.CRITICAL_PERCENTAGE]
        UnionSpecVector[CoreStat.CRITICAL_PERCENTAGE] += requiredCrit
        LPoint -= requiredCrit

        MainStatList = GetMainStatList(self._Job)
        SubStatList = GetSubStatList(self._Job)

        # 직업에 따라 특수 투자스텟 존재(크확, 벞지)
        # TODO:테스트용으로 모법 40투자 임의로 설정
        
        if self._JobName in [JobName.ArchmageFP,JobName.ArchmageTC, JobName.Bishop]:
            LPointToBuff = MaxArea
            LPoint -= LPointToBuff
            self._BuffDuration += LPointToBuff

        if self._Job == JobType.Xenon:
            pass
        elif MainStatList[0] == CoreStat.STAT_STR:
            #전사, 힘해적
            pass
        elif MainStatList[0] == CoreStat.STAT_DEX:
            #궁수, 덱해적
            UnionSpecVector[MainStatList[0]] = 5 * 5
            LPoint -= 5
            UnionSpecVector[SubStatList[0]] = 1 * 5
            LPoint -= 1
            UnionSpecVector[CoreStat.ATTACK_SPELL] = 1
            LPoint -= 1
            # 점수 한 개는 불가피하게 낭비해야함
            UnionSpecVector[CoreStat.ATTACK_PHYSICAL] = 5
            LPoint -= 5
        elif MainStatList[0] == CoreStat.STAT_INT:
            UnionSpecVector[MainStatList[0]] = 5 * 5
            LPoint -= 5
            UnionSpecVector[SubStatList[0]] = 1 * 5
            LPoint -= 1
            UnionSpecVector[CoreStat.ATTACK_SPELL] = 5
            LPoint -= 5
            # 점수 한 개는 불가피하게 낭비해야함
            UnionSpecVector[CoreStat.ATTACK_PHYSICAL] = 1
            LPoint -= 1
        elif MainStatList[0] == CoreStat.STAT_LUK:
            # 도적, 힘도적
            pass
        elif MainStatList[0] == CoreStat.STAT_HP:
            # 데벤
            pass

    
        LPointToCriticalDamage = min(MaxArea, LPoint)
        LPoint -= LPointToCriticalDamage
        UnionSpecVector[CoreStat.CRITICAL_DAMAGE] = LPointToCriticalDamage/2
        self.TotalSpec += UnionSpecVector
        return LPoint
    
    def WeaponPotentialCaseGeneration(self):
        """ 무기류 잠재능력 모든 경우의 수를 생성하여 리스트로 반환
        """
        options = []
        if self._Job == JobType.Magician:
            options = [CoreStat.ATTACK_SPELL_PERCENTAGE, CoreStat.IGNORE_GUARD_PERCENTAGE, CoreStat.DAMAGE_PERCENTAGE_BOSS]
        else:
            options = [CoreStat.ATTACK_PHYSICAL_PERCENTAGE, CoreStat.IGNORE_GUARD_PERCENTAGE, CoreStat.DAMAGE_PERCENTAGE_BOSS]
        num_options = 9

        instresult = set()
        # 모든 조합 생성
        all_combinations = list(itertools.product(options, repeat=num_options))

        # 필터링된 조합을 저장할 리스트
        filtered_combinations = []

        # 첫 3개 옵션은 레전더리 옵션 나머지는 일반옵션
        # 1부터 시작할 때, 3의 배수번째 번호는 엠블렘임
        for combination in all_combinations:
            # 엠블 옵션에 방무 있으면 컷
            if CoreStat.DAMAGE_PERCENTAGE_BOSS in [combination[i*3+2] for i in range(0,int(len(combination)/3))]:
                    continue
                
            # 각 조합에서 "방어율 무시"와 "보스 데미지"의 수 세기
            ignore_defense_count = combination.count(CoreStat.IGNORE_GUARD_PERCENTAGE)
            boss_damage_count = combination.count(CoreStat.DAMAGE_PERCENTAGE_BOSS)

            # 제약 조건을 만족하면 set에 추가(중복 없애기)
            if ignore_defense_count <= 1 and boss_damage_count <= 4:
                inst = SpecVector()
                l = combination[0:3]
                u = combination[3:]
                for legend in l:
                    if legend in [CoreStat.ATTACK_PHYSICAL_PERCENTAGE, CoreStat.ATTACK_SPELL_PERCENTAGE]:
                        inst[legend] += 12
                    elif legend in [CoreStat.IGNORE_GUARD_PERCENTAGE]:
                        inst[legend] = 100 - (100-40) * (100-inst[legend])/100
                    else:
                        inst[legend] += 40
                    
                for unique in u:
                    if unique in [CoreStat.ATTACK_PHYSICAL_PERCENTAGE, CoreStat.ATTACK_SPELL_PERCENTAGE]:
                        inst[unique] += 9
                    elif unique in [CoreStat.IGNORE_GUARD_PERCENTAGE]:
                        inst[unique] = 100 - (100-30) * (100-inst[unique])/100
                    else:
                        inst[unique] += 30
                instresult.add(tuple(inst))
        result = []
        for tpl in instresult:
            result.append(SpecVector(tpl))
        return result
            
        
    