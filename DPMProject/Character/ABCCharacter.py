from Core.SpecElements import *
from Core.ABCItem import ABCItem, ItemParts
from abc import ABC, abstractmethod
from Item.ItemSlot import ItemSlot
from Item.ItemSet import ItemSet, ItemSetOptionLevel
from Item.ItemGroup import ArcaneSymbol, AuthenticSymbol
from Core.Job import JobType
from Character.CharacterAbility import CharacterAbilityEnum
from Character.Trait import Trait
from Character.Union import Legion, LegionOption
from Character.FarmMonster import FarmMonsterEnum
#from Skill.CommonSkill import LinkSkillSlot
from typing import Dict, List

class InvalidInputException(Exception):
    pass



class AttackType(Enum):
    Physical = 0
    Spell = 1

class ABCCharacter(ABC):
    """캐릭터 기본 클래스로, 캐릭터들이 공통적으로 가지고 있는 기능들 묘사

    Args:
        ABC (_type_): _description_
    Level:int
    """    

    # 캐릭터 기본 사항
    _Name:str                           # 캐릭터 이름
    _Level: int                         # 캐릭터 레벨
    _Job:JobType                        # 캐릭터의 직업군(전사, 궁수 등)
    _WeaponConstant:int                 # 무기 상수
    _Mastery: int                       # 숙련도
    _ItemSlot: ItemSlot                 # 장비 착용 슬롯
    _PetSlot: list                      # 미구현(펫 버프, 펫장비, 펫효과)
    _AttackType: AttackType             # 공격 유형(물리데미지, 마법데미지)
    _TotalSpec: SpecVector

    _IsIdle: bool                       # 캐릭터가 행동 가능한 상태인지 

    # 파생 스텟
    _HyperStatPoint:int                 # 하이퍼스텟에 투자할 수 있는 포인트
    _ArcaneForce: int                   # 아케인포스
    _AuthenticForce: int                # 어센틱 포스
    _ItemSetOption: ItemSetOptionLevel  # 세트옵션
    _LegionPoint: int                   # 유니온 점령효과 포인트
    
    # 특수 옵션
    _Cooldown:int                       # 모자에서 등장할 수 있는 쿨타임 감소 옵션
    _CooldownPercent:int                # 농장, 어빌리티, 스킬 등에서 등장하는 쿨타임 초기화 옵션
    _BuffDuration: list[int]            # 농장, 스킬, 성향, 유니온 공격대원 효과, 점령효과에서 등장하는 버프 지속시간 증가
    _SummonDuration: int                # 농장, 스킬, 유니온 공격대원 효과에서 등장하는 소환수 지속시간 효과
    _IsPassiveLevel: bool               # 패시브 레벨 1 옵션, 어빌리티에서 등장
    _IsTargetExt: bool                  # 타겟수 증가 옵션, 농장과 어빌리티에서 등장        
    
    # 추가적인 스펙업 수단
    _PersonalTrait: list[Trait]             # 성향은 만렙으로 가정함.
    _AbilitySlot: set[CharacterAbilityEnum] # 어빌리티 슬롯
    #_LinkSkillSlot: LinkSkillSlot              # 링크 스킬 리스트 - 미구현 
    _Farm: set[FarmMonsterEnum]             # 농장 몬스터 목록
    _LegionList: list[Legion]               # 유니온 대원목록
    _PetBuffList: list                      # 미구현(스킬의 리스트로 설정)
    _DopingBuff: list                       # 물약, 스킬에 의한 장시간 지속 버프
    
    # 미구현(링크 스킬, 유니온(와헌), 0차, 1~5차 등)
    _SkillList: list

    def __init__(self, name:str, level:int, job:JobType, constant:int, mastery:int):
        # Validating name
        assert isinstance(name, str), "Name must be a string"

        # Validating level
        if not isinstance(level, int) or level < 0 or level > 300:
            raise InvalidInputException("Level must be an integer between 0 and 300")

        # Validating job
        if not isinstance(job, JobType):
            raise InvalidInputException("Job must be an instance of JobType")

        # Validating constant
        if not isinstance(constant, int) or constant < 0:
            raise InvalidInputException("Constant must be a non-negative integer")

        # Validating mastery
        if not isinstance(mastery, int) or mastery < 0 or mastery > 100:
            raise InvalidInputException("Mastery must be an integer between 0 and 100")

        self._Name = name
        self._Level = level
        self._Job = job
        self._WeaponConstant = constant
        self._Mastery = mastery
        self._ItemSlot = ItemSlot()
        self._IsPassiveLevel = False
        self._PersonalTrait = [t for t in Trait]
        
        self._HyperStatPoint = self.GetHyperStatPoint()
        
    # 아이템 슬롯을 설정
    def SetItemSlot(self, slot:ItemSlot):
        if not isinstance(slot, ItemSlot):
            raise InvalidInputException("slot must be an instance of ItemSlot")
        self._ItemSlot = slot
    
    # 아이템 슬롯에 아이템을 추가함
    def AddItemToSlot(self, item: ABCItem):
        """슬롯에 아이템을 추가합니다.
        
        Args:
            item (ABCItem): 추가할 아이템 객체

        Raises:
            InvalidInputException: 아이템이 유효하지 않을 경우 발생합니다.
        """
        if not isinstance(item, ABCItem):
            raise InvalidInputException("아이템은 ABCItem의 인스턴스여야 합니다.")
        
        slot = item.ItemPart

        # 아이템을 슬롯에 추가합니다.
        self._ItemSlot.AddItem(slot, item)

    # 착용중인 아이템의 스텟을 캐릭터에 적용시킴. 테스트 필요
    def SetupItemSlotSpec(self):
        belongedItemSetList = ItemSetOptionLevel
        for parts, itemlist in self._ItemSlot:
            for item in itemlist:
                # 아이템 스펙을 total spec에 더해줌
                stat, cool = item.TotalSpec()
                self._TotalSpec += stat
                self._Cooldown += cool

                # 세트 옵션 누적 카운팅
                belongedItemSetList[item.BelongedSet] += 1

                if parts in [ItemParts.Symbol]:
                    if isinstance(item, ArcaneSymbol):
                        self._ArcaneForce += item.GetForce()
                    elif isinstance(item, AuthenticSymbol):
                        self._AuthenticForce += item.GetForce()
                    else:
                        raise TypeError("심볼 아이템이 아니므로 포스를 얻을 수 없음")
                    

        # 세트옵션을 적용
        for setLevel in belongedItemSetList:
            itemset = ItemSet(self._Job)
            if isinstance(itemset[setLevel], SpecVector):
                self._TotalSpec += itemset[setLevel]
            else:
                raise ValueError("더하는 값이 스펙 벡터가 아님")
        

    # 성향 스펙을 적용함        
    def SetupPersonalTrait(self):
        for t in Trait:
            # 카리스마, 통찰력, 의지
            if isinstance(t.value, SpecVector):
                self._TotalSpec += t.value
            elif t in [Trait.감성]:
                self._BuffDuration += t.value
            else:
                pass
                
    # 어빌리티 슬롯을 설정함
    def SetAbilitySlot(self, slot:list[CharacterAbilityEnum]):
        self._AbilitySlot = slot

    # 어빌리티 슬롯을 스펙에 적용함
    def SetupAbilitySlot(self):
        stat = SpecVector()
        for i, e in enumerate(self._AbilitySlot):
            value = e.value[max(1, len(e.value)-i)]
            if e in [CharacterAbilityEnum.BossDamage]:
                stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = value
            elif e in [CharacterAbilityEnum.BuffDuration]:
                self._BuffDuration += value
            elif e in [CharacterAbilityEnum.CooldownReset]:
                self._CooldownPercent = value
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
        
        self._TotalSpec += stat

    # 총 하이퍼스텟 포인트를 반환. 하이퍼스텟 일반식을 이용
    def GetHyperStatPoint(self) -> int:
        first_digit = int(str(self._Level)[-1])
        rest = int((self._Level - first_digit) / 10) - 12
        
        return 5*(rest-2)*(rest+3) + (rest+1)*(first_digit+1)


    ############# 해야함 ##############3
    def SetupHyperStat(self):
        pass

    # 아케인포스를 반환
    def GetArcaneForce(self) ->int:
        return self._ArcaneForce
    # 어센틱 포스를 반환
    def GetAuthenticForce(self) -> int:
        return self._AuthenticForce

    # 유니온 대원 리스트를 설정함
    def SetUnionMemberList(self, _list:list):
        if not isinstance(_list, List):
            raise ValueError("유니온 멤버 리스트는 리스트형식")
        
        if not isinstance(_list[0], Legion):
            raise ValueError("유니온 대원 리스트 멤버는 Legion")
        
        self._LegionList = _list

    ############## 미완성 유니온 점령효과 ###############
    def SetupUnion(self):
        # 유니온 대원 효과를 적용함
        for member in self._LegionList:
            optionType = member.value._Option
            effect = optionType.value[0]
            if isinstance(effect, SpecVector):
                self._TotalSpec += effect
            elif optionType == LegionOption.SummonDuration:
                self._SummonDuration += effect
            elif optionType == LegionOption.CooldownPercent:
                self._CooldownPercent += effect
            elif optionType == LegionOption.BuffDuration:
                self._BuffDuration += effect
            elif optionType == LegionOption.WildHunter:
                pass    # 와일드헌터 20% 확률로 데미지 16~020% 증가. 스킬로 구현

        # 유니온 점령 효과를 적용함

    # 링크 스킬 목록을 설정함
    def SetLinkSkillList(self, skilllist: list):
        pass

    # 링크 스킬을 캐릭터에 적용함
    def SetupLinkSkill(self):
        pass

    # 모든 스펙요소를 적용함
    def Setup(self):
        self.SetupItemSlotSpec()
        self.SetupPersonalTrait()
        self.SetupAbilitySlot()
        self.SetupUnion()
        self.SetupLinkSkill()
        pass    #...
