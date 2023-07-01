from Core.ABCItem import ABCItem, ItemParts
from Core.SpecElements import SpecVector, CoreStat
from Core.Job import JobType
import csv
from enum import Enum
from Core.Server import GameServer

POTENTIAL_OPTION_SLOT = 3
ADDITIONAL_POTENTIAL_OPTION_SLOT = 3
class PotentialEnum(Enum):
    """잠재능력의 종류를 나타내는 열거형 클래스입니다.
    """
    BossDamage = CoreStat.DAMAGE_PERCENTAGE_BOSS
    IgnoreGuard = CoreStat.IGNORE_GUARD_PERCENTAGE
    AttackPercentage = CoreStat.ATTACK_PHYSICAL_PERCENTAGE
    SpellPercentage = CoreStat.ATTACK_SPELL_PERCENTAGE

    StrPercentage = CoreStat.STAT_STR_PERCENTAGE
    DexPercentage = CoreStat.STAT_DEX_PERCENTAGE
    IntPercentage = CoreStat.STAT_INT_PERCENTAGE
    LukPercentage = CoreStat.STAT_LUK_PERCENTAGE
    AllPercentage = CoreStat.STAT_ALL_PERCENTAGE
    HPPercentage = CoreStat.STAT_HP_PERCENTAGE
    CriticalDamage = CoreStat.CRITICAL_DAMAGE
    StrOverLevel9 = CoreStat.STAT_STR_9LEVEL
    DexOverLevel9 = CoreStat.STAT_DEX_9LEVEL
    IntOverLevel9 = CoreStat.STAT_INT_9LEVEL
    LukOverLevel9 = CoreStat.STAT_LUK_9LEVEL
    Attack = CoreStat.ATTACK_PHYSICAL
    Spell = CoreStat.ATTACK_SPELL
    Cooldown = len(CoreStat)
    Nothing = len(CoreStat)+1


class PotentialGrade(Enum):
    """잠재능력의 등급을 나타내는 열거형 클래스입니다.

    Args:
        Enum (_type_): _description_
    """
    Legendary = 0
    Unique = 1
    Epic = 2
    Rare = 3

class PotentialOptionSlot:
    """잠재능력의 옵션, 등급, 추가 여부를 나타내는 클래스입니다.



    Raises:
        TypeError: _description_
        TypeError: _description_
        TypeError: _description_
    """
    Option: PotentialEnum
    Grade: PotentialGrade
    isadditional: bool

    def __init__(self, option:PotentialEnum, grade:PotentialGrade, isadditional:bool):
        if not isinstance(option, PotentialEnum):
            raise TypeError("인스턴스 누락")
        self.Option = option

        if not isinstance(grade, PotentialGrade):
            raise TypeError("인스턴스 누락")
        self.Grade = grade

        if not isinstance(isadditional, bool):
            raise TypeError("인스턴스 누락")
        self.isadditional = isadditional


class PotentialAbility(ABCItem):
    _instance = None
    PotentialOptionList: list[PotentialOptionSlot]
    AdditionalPotentialOptionList: list[PotentialOptionSlot]
    Under200PotentialOptionTable: list[list]
    Over250PotentialOptionTable: list[list]
    Under200AdditionalPotentialTable: list[list]
    Over250AdditionalPotentialTable: list[list]
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.OpenPotentialTable()
            return cls._instance
        else:
            return super().__new__(cls)
        
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        itemPart: ItemParts,
        potentialOptionList: list[PotentialOptionSlot],
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        ABCItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            server=server
            )
        
        if potentialOptionList is not None and len(potentialOptionList) > POTENTIAL_OPTION_SLOT:
            raise ValueError("잠재능력은 3줄 이하로 설정")

        if not isinstance(potentialOptionList, list):
            raise TypeError("인스턴스가 누락")
        self.PotentialOptionList = potentialOptionList

        if additionalPotentialOptionList is not None:
            if len(additionalPotentialOptionList) > ADDITIONAL_POTENTIAL_OPTION_SLOT:
                raise ValueError("에디셔널 잠재능력은 3줄 이하로 설정")

            if not isinstance(additionalPotentialOptionList, list):
                raise TypeError("인스턴스가 누락")        
        self.AdditionalPotentialOptionList = additionalPotentialOptionList

    @classmethod
    def OpenPotentialTable(cls):
        """잠재능력 정보를 가진 csv 파일을 열고, 정보를 list 형태로 저장함.
        """        
        PotentialTablePath = "Core/Enchant/PotentialTable/"
        Under200PotentialTableFileName = PotentialTablePath + "Under200ItemPotentialTable.csv"
        Under200AdditionalTableFileName = PotentialTablePath + "Under200ItemAdditionalTable.csv"
        Over250PotentialTableFileName = PotentialTablePath + "Over250ItemPotentialTable.csv"
        Over250AdditionalTableFileName = PotentialTablePath + "Over250ItemAdditionalTable.csv"
        
        cls.Under200PotentialOptionTable = cls.ParsePotentialTable(Under200PotentialTableFileName)
        cls.Under200AdditionalPotentialTable = cls.ParsePotentialTable(Under200AdditionalTableFileName)
        cls.Over250PotentialOptionTable = cls.ParsePotentialTable(Over250PotentialTableFileName)
        cls.Over250AdditionalPotentialTable = cls.ParsePotentialTable(Over250AdditionalTableFileName)
        
    @classmethod
    def ParsePotentialTable(cls, file_path: str) -> list:
        """csv 파일 경로를 받아서 바로 사용할 수 있는 형태의 list로 반환함

        Args:
            file_path (str): 열어야 할 파일 경로

        Returns:
            list: 파싱한 list 자료형 반환
        """
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # 첫 번째 줄(태그)을 건너뜁니다.
            
            # 숫자 리스트를 저장할 빈 리스트를 생성합니다.
            numbers_list = []
            
            # 각 줄에 대해
            for row in csv_reader:
                # 각 항목을 숫자로 변환하거나, 빈 문자열이면 None을 리스트에 추가합니다.
                numbers = [int(item) if item.isdigit() else None for item in row]
                numbers_list.append(numbers)
                
        return numbers_list

    def PotentialToSpec(self, option:PotentialOptionSlot) -> tuple[SpecVector, int]:
        """잠재능력을 SpecVector, cooldown 으로 반환함

        Args:
            option (PotentialOptionSlot): 잠재능력 종류, 등급

        Returns:
            tuple[SpecVector, int]: 잠재능력 총합 SpecVector, 쿨감 옵션
        """
        ResultSpecVector = SpecVector()
        ResultCooldown = 0
        
        if (self.ServerOption == GameServer.RebootServer) and (option.isadditional):
            return ResultSpecVector, ResultCooldown

        Tag = option.Option.value
        Grade = option.Grade.value
        
        # 잠재능력 옵션 열거형 중에서
        for opt in PotentialEnum:
            # 알맞는 옵션과 일치할 때,
            if (Tag == opt.value) and ( Tag != PotentialEnum.Cooldown.value):
                # 레벨, 에디셔널 유무에 따라 적합한 테이블을 찾아 값을 대입함
                if self.RequiredLevel <= 200:
                    if option.isadditional == False:
                        ResultSpecVector[opt.value] = self.Under200PotentialOptionTable[Grade][Tag.value]
                    elif option.isadditional == True:
                        ResultSpecVector[opt.value] = self.Under200AdditionalPotentialTable[Grade][Tag.value]
                elif self.RequiredLevel == 250:
                    if option.isadditional == False:
                        ResultSpecVector[opt.value] = self.Over250PotentialOptionTable[Grade][Tag.value]    
                    elif option.isadditional == True:
                        ResultSpecVector[opt.value] = self.Over250AdditionalPotentialTable[Grade][Tag.value]
                break
            elif opt.value == PotentialEnum.Cooldown.value:
                if self.RequiredLevel <= 200:
                    if option.isadditional == False:
                        ResultCooldown += self.Under200PotentialOptionTable[Grade][Tag]
                    elif option.isadditional == True:
                        ResultCooldown += self.Under200AdditionalPotentialTable[Grade][Tag]
                elif self.RequiredLevel == 250:
                    if option.isadditional == False:
                        ResultCooldown += self.Over250PotentialOptionTable[Grade][Tag]
                    elif option.isadditional == True:
                        ResultCooldown += self.Over250AdditionalPotentialTable[Grade][Tag]
                break
            elif opt.value == PotentialEnum.Nothing:
                break
        
        return (ResultSpecVector, ResultCooldown)
    
    def TotalSpec(self) -> tuple[SpecVector, int]:
        """잠재능력으로 인한 아이템 스펙을 반환

        Returns:
            tuple[SpecVector, int]: 잠재능력 SpecVector, 쿨감 옵션
        """
        resultVector = SpecVector()
        resultCooldown = 0

        for slot in self.PotentialOptionList:
            vec, cooldown = self.PotentialToSpec(option=slot)
            resultVector = resultVector + vec
            resultCooldown += cooldown
        
        if self.ServerOption == GameServer.RebootServer:
            return resultVector, resultCooldown
        
        if self.AdditionalPotentialOptionList is not None:
            for slot in self.AdditionalPotentialOptionList:
                vec, cooldown = self.PotentialToSpec(option=slot)
                resultVector = resultVector + vec
                resultCooldown += cooldown
        return resultVector, resultCooldown