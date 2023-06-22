from Core.ABCItem import ABCItem, ItemParts, JobType, ItemType, ItemInfo
from Core.SpecElements import SpecVector, CoreStat
from Core.Server import GameServer
from Core.ReqLevel import ReqLevel
from enum import Enum
import csv    
import math


class BonusOptionEnum(Enum):
    """게임 내 다양한 종류의 보너스 옵션을 표현하는 열거형입니다.

    이 열거형의 각 멤버는 아이템에 적용할 수 있는 다른 종류의 보너스 옵션을 나타냅니다.

    멤버:
        AttackPhysical: 물리 공격 보너스 옵션을 나타냅니다.
        AttackSpell: 주문 공격 보너스 옵션을 나타냅니다.
        StrSingleStat: 힘 보너스 옵션을 나타냅니다.
        DexSingleStat: 민첩성 보너스 옵션을 나타냅니다.
        IntSingleStat: 지능 보너스 옵션을 나타냅니다.
        LukSingleStat: 행운 보너스 옵션을 나타냅니다.
        StrDexDoubleStat: 힘과 민첩성 보너스 옵션을 나타냅니다.
        StrIntDoubleStat: 힘과 지능 보너스 옵션을 나타냅니다.
        StrLukDoubleStat: 힘과 행운 보너스 옵션을 나타냅니다.
        DexIntDoubleStat: 민첩성과 지능 보너스 옵션을 나타냅니다.
        DexLukDoubleStat: 민첩성과 행운 보너스 옵션을 나타냅니다.
        IntLukDoubleStat: 지능과 행운 보너스 옵션을 나타냅니다.
        BossDamage: 보스 데미지 보너스 옵션을 나타냅니다.
        Damage: 데미지 보너스 옵션을 나타냅니다.
        AllStatPercentage: 모든 스탯을 퍼센트로 증가시키는 보너스 옵션을 나타냅니다.
        HPStat: 체력 보너스 옵션을 나타냅니다.
        MPStat: 마나 포인트 보너스 옵션을 나타냅니다.
        
    """    
    AttackPhysical = 0
    AttackSpell = 1
    StrSingleStat = 2
    DexSingleStat = 3
    IntSingleStat = 4
    LukSingleStat = 5
    StrDexDoubleStat = 6
    StrIntDoubleStat = 7
    StrLukDoubleStat = 8
    DexIntDoubleStat = 9
    DexLukDoubleStat = 10
    IntLukDoubleStat = 11
    BossDamage = 12
    Damage = 13
    AllStatPercentage = 14
    HPStat = 15
    MPStat = 16

class BonusOptionGrade(Enum):
    """메이플 추가옵션의 등급을 나타냄

    이 열거형의 각 멤버는 아이템에 적용할 수 있는 다른 등급의 추가 옵션을 나타냅니다.

    멤버:
        first: 보너스 옵션의 첫 번째 등급을 나타냅니다.
        second: 보너스 옵션의 두 번째 등급을 나타냅니다.
        third: 보너스 옵션의 세 번째 등급을 나타냅니다.
        fourth: 보너스 옵션의 네 번째 등급을 나타냅니다.
        fifth: 보너스 옵션의 다섯 번째 등급을 나타냅니다.
    """    
    first = 7
    second = 6
    third = 5
    fourth = 4
    fifth = 3

class BonusOptionSlot(dict):
    """추가옵션의 종류와 등급을 매칭하는 딕셔너리 구조형

    Args:
        dict (class): _description_
    
    Attributes:
        BONUS_OPTION_SLOT (int): 추가 옵션 부여 최대 갯수

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    
    """    
    BONUS_OPTION_SLOT = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if len(self) > self.BONUS_OPTION_SLOT:
            raise ValueError("추가옵션 갯수는 4개를 넘을 수 없음")
    
    def __setitem__(self, __key: str, __value: BonusOptionGrade) -> None:
        if len(self) > self.BONUS_OPTION_SLOT:
            raise ValueError("추가옵션 갯수는 최대 4개입니다")
        return super().__setitem__(__key, __value)

    def update(self, other=None, **kwargs):
        if other is not None:
            temp = dict(other)
        else:
            temp = dict(**kwargs)
        if len(self) + len(temp) > self.BONUS_OPTION_SLOT:
            raise ValueError("추가옵션 갯수는 최대 4개입니다")
        super().update(other, **kwargs)


class BonusOption(ABCItem):
    """추가옵션을 표현하는 클래스

    Args:
        ABCItem (class): 추상 아이템 클래스

    Attributes:
        _instance: 옵션 표를 한 번만 열기 위해 객체의 최초 생성 여부를 담고 있음
        OptionSlot: 추가 옵션의 종류와 등급을 담은 딕셔너리
        BonusOptionDict: 해당 추가옵션 종류와 등급의 수치를 담은 딕셔너리
    Raises:
        TypeError: _description_
        ValueError: _description_
        ValueError: _description_
        AttributeError: _description_
        AttributeError: _description_
        TypeError: _description_

    Methods:
        OpenBonusOptionTable(): CSV 파일에서 보너스 옵션 테이블을 열고 파싱하는 클래스 메소드입니다.
        ParseBonusOptionTable(file_path: str): CSV 파일에서 보너스 옵션 테이블을 파싱하는 클래스 메소드입니다.
        TotalSpec(): 보너스 옵션에 따른 아이템의 총 사양을 계산합니다.
        WeaponATKCalc(basicATK:int, grade:BonusOptionGrade): 무기 아이템의 공격 값을 계산합니다.
        BonusOptionToSpec(option:BonusOptionSlot): 보너스 옵션을 사양 벡터로 변환합니다.
   
    """    
    _instance = None
    OptionSlot: BonusOptionSlot
    BonusOptionDict = {}
    _weaponbasicATK = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.OpenBonusOptionTable()
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
            optionslot: BonusOptionSlot,
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

        if not isinstance(optionslot, BonusOptionSlot):
            raise TypeError("인스턴스 누락")
        
        if len(optionslot) > 4:
            raise ValueError("추가옵션은 4종류 이하입니다")
        
        self.OptionSlot = optionslot

    @classmethod
    def OpenBonusOptionTable(cls):
        """CSV 파일에서 추가 옵션 표를 열기 위해 파일 경로를 파싱하고, 불러들임
        """        
        BonusOptionTablePath = "/Users/mac/Documents/testpoetry/DPMProject/Core/Enchant/BonusOptionTable/"

        cls.BonusOptionDict.update({
            ReqLevel.Lv130.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor130.csv"),
            ReqLevel.Lv140.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor140.csv"),
            ReqLevel.Lv150.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor150.csv"),
            ReqLevel.Lv160.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor160.csv"),
            ReqLevel.Lv200.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor200.csv"),
            ReqLevel.Lv250.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArmor250.csv"),
            ReqLevel.Lv200Weapon.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionWeapon200.csv"),
            ReqLevel.Lv200ArcaneWeapon.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionArcaneWeapon.csv"),
            ReqLevel.Lv200GenesisWeapon.value: cls.ParseBonusOptionTable(BonusOptionTablePath + "BonusOptionGenesisWeapon.csv")
        })

    @classmethod
    def ParseBonusOptionTable(cls, file_path: str) -> list:
        """추가 옵션 파일을 리스트 형태로 파싱함(raw text -> list)

        Args:
            file_path (str): 파싱할 csv 파일의 경로

        Returns:
            list: 옵션 list
        """        
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # 첫 번째 줄(태그)을 건너뜁니다.

            # 숫자 리스트를 저장할 빈 리스트를 생성합니다.
            numbers_list = []

            # 각 줄에 대해
            for row in csv_reader:
                # 각 항목을 숫자로 변환하거나, 빈 문자열이면 None을 리스트에 추가합니다.
                numbers = [int(item) if item.isdigit() else None for item in row[0:]]
                numbers_list.append(numbers)

        return numbers_list

    
    def TotalSpec(self) -> tuple[SpecVector, int]:
        """추가 옵션의 총 사양을 반환

        Returns:
            SpecVector: 벡터 형식의 총 사양
        """        
        if self.ServerOption == GameServer.RebootServer:
            return SpecVector(), 0
        else:
            return self.BonusOptionToSpec(self.OptionSlot), 0
    
    def WeaponATKCalc(self, basicATK:int, grade:BonusOptionGrade) -> int:
        """무기 아이템 옵션 등급에 따른 추가옵션 반환

        Args:
            basicATK (int): 무기의 기본 공격력
            grade (BonusOptionGrade): 무기 추가옵션의 등급

        Returns:
            int: 등급에 따른 추가옵션 반환
        """        
        result = math.ceil((basicATK / 100) * (math.floor(self.RequiredLevel / 40) + 1) * grade.value * (1.1 ** (grade.value - 3)))
        return result

    def BonusOptionToSpec(self, option:BonusOptionSlot) -> SpecVector:
        """부여된 보너스 옵션을 계산해 반환함

        Args:
            option (BonusOptionSlot): 옵션과 등급을 key, value 로 가지는 딕셔너리

        Raises:
            ValueError: _description_
            AttributeError: _description_
            AttributeError: _description_
            TypeError: _description_

        Returns:
            SpecVector: 추가옵션 총 상승량
        """        
        if len(option) > BonusOptionSlot.BONUS_OPTION_SLOT:
            raise ValueError("추가 옵션은 종류는 4개까지입니다")
        
        result = SpecVector()

        Type = self.ItemPart.value[ItemInfo.ItemGroup.value]

        reqLevelTable = list
        if self.ItemPart in [ItemParts.Weapon]:
            reqLevelTable = self.BonusOptionDict[ReqLevel.Lv200Weapon.value]
        else:
            reqLevelTable = self.BonusOptionDict[self.RequiredLevel]
        


        
            # 아이템 기본 정보가 정확한지 확인
            # 아이템이 공격/마력 인지 확인

        for opt, grade in self.OptionSlot.items():
            # 무기 계열은 공격력/마력 추가옵션 로직이 다르므로 별도로 처리함
            if opt == BonusOptionEnum.AttackPhysical:
                if Type in [ItemType.Accessory, ItemType.Armor]:
                    result[CoreStat.ATTACK_PHYSICAL] += grade.value * reqLevelTable[opt.value][CoreStat.ATTACK_PHYSICAL.value]
                elif Type in [ItemType.Weapon]:
                    basicStat = self.ItemBasicStat[CoreStat.ATTACK_PHYSICAL]
                    increase = self.WeaponATKCalc(basicATK=basicStat, grade=grade, reqLev=self.RequiredLevel)
                    result[CoreStat.ATTACK_PHYSICAL] += increase
            elif opt == BonusOptionEnum.AttackSpell:
                if Type in [ItemType.Accessory, ItemType.Armor]:
                    result[CoreStat.ATTACK_SPELL] += grade.value * reqLevelTable[opt.value][CoreStat.ATTACK_SPELL.value]
                elif Type in [ItemType.Weapon]:
                    basicStat = self.ItemBasicStat[CoreStat.ATTACK_SPELL]
                    increase = self.WeaponATKCalc(basicATK=basicStat, grade=grade)
                    result[CoreStat.ATTACK_SPELL] += increase
            elif opt == BonusOptionEnum.StrSingleStat:
                result[CoreStat.STAT_STR] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_STR.value]
            elif opt == BonusOptionEnum.DexSingleStat:
                result[CoreStat.STAT_DEX] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_DEX.value]
            elif opt == BonusOptionEnum.IntSingleStat:
                result[CoreStat.STAT_INT] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_INT.value]
            elif opt == BonusOptionEnum.LukSingleStat:
                result[CoreStat.STAT_LUK] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_LUK.value]
            elif opt == BonusOptionEnum.StrDexDoubleStat:
                result[CoreStat.STAT_STR] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_STR.value]
                result[CoreStat.STAT_DEX] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_DEX.value]
            elif opt == BonusOptionEnum.StrIntDoubleStat:
                result[CoreStat.STAT_STR] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_STR.value]
                result[CoreStat.STAT_INT] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_INT.value]
            elif opt == BonusOptionEnum.StrLukDoubleStat:
                result[CoreStat.STAT_STR] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_STR.value]
                result[CoreStat.STAT_LUK] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_LUK.value]
            elif opt == BonusOptionEnum.DexIntDoubleStat:
                result[CoreStat.STAT_DEX] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_DEX.value]
                result[CoreStat.STAT_INT] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_INT.value]
            elif opt == BonusOptionEnum.DexLukDoubleStat:
                result[CoreStat.STAT_DEX] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_DEX.value]
                result[CoreStat.STAT_LUK] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_LUK.value]
            elif opt == BonusOptionEnum.IntLukDoubleStat:
                result[CoreStat.STAT_INT] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_INT.value]
                result[CoreStat.STAT_LUK] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_LUK.value]
            elif opt == BonusOptionEnum.BossDamage:
                if Type in [ItemType.Accessory, ItemType.Armor]:
                    raise AttributeError("방어구에 데미지, 보스 데미지 옵션은 부여할 수 없음")
                
                result[CoreStat.DAMAGE_PERCENTAGE_BOSS] += grade.value * reqLevelTable[opt.value][CoreStat.DAMAGE_PERCENTAGE_BOSS.value]
            elif opt == BonusOptionEnum.Damage:
                if Type in [ItemType.Accessory, ItemType.Armor]:
                    raise AttributeError("방어구에 데미지, 보스 데미지 옵션은 부여할 수 없음")
                
                result[CoreStat.DAMAGE_PERCENTAGE] += grade.value * reqLevelTable[opt.value][CoreStat.DAMAGE_PERCENTAGE.value]
            elif opt == BonusOptionEnum.AllStatPercentage:
                result[CoreStat.STAT_ALL_PERCENTAGE] = grade.value * reqLevelTable[opt.value][CoreStat.STAT_ALL_PERCENTAGE.value]
            elif opt == BonusOptionEnum.HPStat:
                result[CoreStat.STAT_HP] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_HP.value]
            elif opt == BonusOptionEnum.MPStat:
                result[CoreStat.STAT_MP] += grade.value * reqLevelTable[opt.value][CoreStat.STAT_MP.value]
            else:
                raise TypeError("추가옵션 열거형을 벗어남")
            
        return result