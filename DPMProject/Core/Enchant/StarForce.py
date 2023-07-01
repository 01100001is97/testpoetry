from Core.ABCItem import ItemParts, ItemType
from Core.Job import JobType, JobTypeInfo
from Core.SpecElements import SpecVector, CoreStat
from Core.Enchant.Scroll import Upgrade, UpgradeScrolls
from Core.Server import GameServer
import csv
    


class StarForce(Upgrade):
    __instance = None
    StarforceLevel: int
    StarforceStat: SpecVector
    StarforceStatTable: list
    StarforceArmorAtkTable: list
    StarforceWeaponAtkTable: list
    StarforceHPMPTable: list
    LevelTable: list

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.OpenStarforceOptionTable()
            cls.LevelTable = [i[0] for i in cls.StarforceStatTable]

            return cls.__instance
        else:
            return super().__new__(cls)
            
    def __init__(
            self, 
            itemName: str,
            requiredLevel: int,
            requiredJobType: list[JobType],
            itemBasicStat: SpecVector,
            itemPart: ItemParts,
            upgrade_chance: int,
            upgrade_history: list[UpgradeScrolls],
            starforce: int,
            server= GameServer.NormalServer
            ):
        super().__init__(
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            upgrade_chance=upgrade_chance,
            upgrade_history=upgrade_history,
            server=server
        )
        if not isinstance(starforce, int):
            raise TypeError("스타포스값은 정수로 입력해야함")

        if (starforce < 0) or (starforce > 25):
            raise ValueError("스타포스 수치는 0~25")
        
        self.StarforceLevel = starforce
    
    @classmethod
    def OpenStarforceOptionTable(cls):
        StarforceTablePath = "Core/Enchant/StarforceTable/"
        
        StatTableFileName = StarforceTablePath + "StarforceStat.csv"
        ArmorATKTableFileName = StarforceTablePath + "StarforceArmorAtk.csv"
        WeaponATKTableFileName = StarforceTablePath + "StarforceWeaponAtk.csv"
        HPMPTableFileName = StarforceTablePath + "StarforceHPMPStat.csv"

        cls.StarforceStatTable = cls.ParseStarforceTable(StatTableFileName)
        cls.StarforceArmorAtkTable = cls.ParseStarforceTable(ArmorATKTableFileName)
        cls.StarforceWeaponAtkTable = cls.ParseStarforceTable(WeaponATKTableFileName)
        cls.StarforceHPMPTable = cls.ParseStarforceTable(HPMPTableFileName)
        
    @classmethod
    def ParseStarforceTable(cls, file_path: str) -> list:
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            
            
            # 숫자 리스트를 저장할 빈 리스트를 생성합니다.
            numbers_list = []
            
            # 각 줄에 대해
            for row in csv_reader:
                # 각 항목을 숫자로 변환하거나, 빈 문자열이면 None을 리스트에 추가합니다.
                numbers = [int(item) if item.isdigit() else None for item in row]
                numbers_list.append(numbers)
                
        return numbers_list

    def GetStarforceLevel(self) -> int:
        return self.StarforceLevel
    
    def GetStatSetOfReqiredJob(self, jobList: list[JobType]) -> set:
        result = set[CoreStat]()
        for job in jobList:
            stats = job.value
            mainStat = stats[JobTypeInfo.MainStat.value][0]
            subStat = stats[JobTypeInfo.SubStat.value][0]
            result.add(mainStat)
            result.add(subStat)
            
        return result

    def StarforceToVector(self) -> SpecVector:
        # 스텟 부여는 무기, 방어구, 악세서리 모두 동일
        result = SpecVector()
        if self.StarforceLevel == 0: return result

        # 블빈마, 파풀마의 경우 5레벨 낮은 수치를 적용함
        ReqLevel= next(i for i, level in enumerate(self.LevelTable) if level == self.RequiredLevel - self.RequiredLevel%10)

        # 부여할 스텟 종류를 고름
        StarforceEnchantStatSet = self.GetStatSetOfReqiredJob(self.RequiredJobType)
        
        # 부여할 스텟별로 수치 부여
        BaseStat = [CoreStat.STAT_STR, CoreStat.STAT_DEX, CoreStat.STAT_INT, CoreStat.STAT_LUK]
        for stat in BaseStat:
            if stat in StarforceEnchantStatSet:
                result[stat] = self.StarforceStatTable[ReqLevel][self.StarforceLevel]
            elif stat not in StarforceEnchantStatSet and self.StarforceLevel>15 and self.ItemPart in [ItemParts.Shoulder]:
                result[stat] = self.StarforceStatTable[ReqLevel][self.StarforceLevel] - self.StarforceStatTable[ReqLevel][15]
            else:
                pass
        
        # HP,MP 스텟 부여 로직 
        if self.ItemPart in [
                ItemParts.Cap,
                ItemParts.Clothes,
                ItemParts.Pants, 
                ItemParts.Cape, 
                ItemParts.Ring, 
                ItemParts.Pendant, 
                ItemParts.Belt, 
                ItemParts.Shoulder, 
                ItemParts.Shield,
                ItemParts.Weapon
                ]:
                result[CoreStat.STAT_HP] = self.StarforceHPMPTable[0][min(len(self.StarforceHPMPTable[0]),self.StarforceLevel)-1]
        if self.ItemPart in [ItemParts.Weapon]:
                result[CoreStat.STAT_MP] = self.StarforceHPMPTable[0][min(len(self.StarforceHPMPTable[0]),self.StarforceLevel)-1]
            

        # 방어구/악서서리 류 공마        
        if self.ItemPart.value[1] in [ItemType.Armor, ItemType.Accessory]:
            result[CoreStat.ATTACK_PHYSICAL] = self.StarforceArmorAtkTable[ReqLevel][self.StarforceLevel]
            result[CoreStat.ATTACK_SPELL] = self.StarforceArmorAtkTable[ReqLevel][self.StarforceLevel]

        UpgradeResult, _ = Upgrade.TotalSpec(self)
        # 장갑 전용 공/마 상승 로직
        if self.ItemPart == ItemParts.Gloves:
            for i in range(1, self.StarforceLevel+1):
                if i in [5,7,9,11,13,14,15]:
                    if JobType.Magician in self.RequiredJobType:
                        result[CoreStat.ATTACK_SPELL] += 1
                    else:
                        result[CoreStat.ATTACK_PHYSICAL] += 1
                    
        # 무기류 공마
        elif self.ItemPart.value[1]  == ItemType.Weapon:
            for star in range(1,self.StarforceLevel+1):
                if star < 16:
                    # 공격력
                    AtkBasicStat = self.ItemBasicStat[CoreStat.ATTACK_PHYSICAL]
                    AtkUpgradeStat = UpgradeResult[CoreStat.ATTACK_PHYSICAL]
                    AtkDiff = ((AtkBasicStat + AtkUpgradeStat + result[CoreStat.ATTACK_PHYSICAL]) // 50) + 1
                    result[CoreStat.ATTACK_PHYSICAL] += AtkDiff
                    # 마력
                    SpellBasicStat = self.ItemBasicStat[CoreStat.ATTACK_SPELL]
                    SpellUpgradeStat = UpgradeResult[CoreStat.ATTACK_SPELL]
                    SpellDiff = ((SpellBasicStat + SpellUpgradeStat + result[CoreStat.ATTACK_SPELL]) // 50) + 1
                    result[CoreStat.ATTACK_SPELL] += SpellDiff
                elif star >= 16:
                    result[CoreStat.ATTACK_PHYSICAL] += self.StarforceWeaponAtkTable[ReqLevel][star]
                    result[CoreStat.ATTACK_SPELL] += self.StarforceWeaponAtkTable[ReqLevel][star]
                    
        
        return result + UpgradeResult

    def TotalSpec(self) -> tuple[SpecVector, int]:
        """스타포스 상승치

        Returns:
            SpecVector: 스타포스로 인한 상승치
        """        
        return self.StarforceToVector(), 0
    
    
