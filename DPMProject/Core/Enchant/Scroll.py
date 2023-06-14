from Core.ABCItem import ABCItem, ItemParts, ItemType, ItemInfo
from Core.SpecElements import SpecVector, CoreStat
from Core.Job import JobType
from Core.Server import GameServer

class WeaponScrolls:
    """무기류 주문서를 묘사함.
        PieceSTR15: SpecVector - 무기 공격력 주문서(힘) 15%
        PieceDEX15: SpecVector
        PieceINT15: SpecVector
        PieceLUK15: SpecVector
        MagicalATK: SpecVector - 매지컬 공격력 스크롤
        MagicalSPELL: SpecVector - 매지컬 마력 스크롤
    """    

    PieceSTR15: SpecVector
    PieceDEX15: SpecVector
    PieceINT15: SpecVector
    PieceLUK15: SpecVector
    MagicalATK: SpecVector
    MagicalSPELL: SpecVector

    def __init__(self):
        # 120렙 이상 무기류 주문서 15%작. 공/마 9, 해당 스텟 4, HP 200
        WeaponScrollPieceSTR15Stat = SpecVector()
        WeaponScrollPieceSTR15Stat[CoreStat.ATTACK_PHYSICAL] = 9
        WeaponScrollPieceSTR15Stat[CoreStat.STAT_STR] = 4
        self.PieceSTR15 = WeaponScrollPieceSTR15Stat

        WeaponScrollPieceDEX15Stat = SpecVector()
        WeaponScrollPieceDEX15Stat[CoreStat.ATTACK_PHYSICAL] = 9
        WeaponScrollPieceDEX15Stat[CoreStat.STAT_DEX] = 4
        self.PieceDEX15 = WeaponScrollPieceDEX15Stat

        WeaponScrollPieceINT15Stat = SpecVector()
        WeaponScrollPieceINT15Stat[CoreStat.ATTACK_SPELL] = 9
        WeaponScrollPieceINT15Stat[CoreStat.STAT_INT] = 4
        self.PieceINT15 = WeaponScrollPieceINT15Stat

        WeaponScrollPieceLUK15Stat = SpecVector()
        WeaponScrollPieceLUK15Stat[CoreStat.ATTACK_PHYSICAL] = 9
        WeaponScrollPieceLUK15Stat[CoreStat.STAT_LUK] = 4
        self.PieceLUK15 = WeaponScrollPieceLUK15Stat

        # 매지컬의 경우 실제 공/마는 9(50%) 10(40%) 11(10%) 이지만, 기대값 9.6이므로 10이라고 가정.
        MagicalWeaponScrollATKStat = SpecVector()
        MagicalWeaponScrollATKStat[CoreStat.ATTACK_PHYSICAL] = 10
        MagicalWeaponScrollATKStat[CoreStat.STAT_ALL] = 3
        self.MagicalATK = MagicalWeaponScrollATKStat
        
        MagicalWeaponScrollSPELLStat = SpecVector()
        MagicalWeaponScrollSPELLStat[CoreStat.ATTACK_SPELL] = 10
        MagicalWeaponScrollSPELLStat[CoreStat.STAT_ALL] = 3
        self.MagicalSPELL = MagicalWeaponScrollSPELLStat

class ArmorScrolls:
    """
    방어구 주문서를 묘사함

        PieceSTR15: SpecVector - 방어구 힘 주문서 15%
        PieceDEX15: SpecVector
        PieceINT15: SpecVector
        PieceLUK15: SpecVector
        PieceALL15: SpecVector - 방어구 올스텟 주문서 15%
        PieceHP15: SpecVector - 방어구 HP 주문서 15%
        PieceATK15: SpecVector - (장갑) 공격력 주문서 15%
        PieceSPELL15: SpecVector - (장갑) 마력 주문서 15%
        PieceSTR30: SpecVector - 방어구 힘 주문서 30%
        PieceDEX30: SpecVector
        PieceINT30: SpecVector
        PieceLUK30: SpecVector
        PieceALL30: SpecVector
        PieceHP30: SpecVector
        PieceATK30: SpecVector
        PieceSPELL30: SpecVector
        ATK: SpecVector - (방패) 방어구 공격력 주문서
        SPELL: SpecVector - (방패) 방어구 마력 주문서
    """    
    PieceSTR15: SpecVector
    PieceDEX15: SpecVector
    PieceINT15: SpecVector
    PieceLUK15: SpecVector
    PieceALL15: SpecVector
    PieceHP15: SpecVector
    PieceATK15: SpecVector
    PieceSPELL15: SpecVector
    PieceSTR30: SpecVector
    PieceDEX30: SpecVector
    PieceINT30: SpecVector
    PieceLUK30: SpecVector
    PieceALL30: SpecVector
    PieceHP30: SpecVector
    PieceATK30: SpecVector
    PieceSPELL30: SpecVector
    ATK: SpecVector
    SPELL: SpecVector

    def __init__(self):
        # 120렙 이상 방어구 주문서 15%작. 해당 스텟 10 or 올스텟 4 or HP 670, 공통: HP 170
        STR15Stat = SpecVector()
        STR15Stat[CoreStat.STAT_STR] = 10
        STR15Stat[CoreStat.STAT_HP] = 170
        self.PieceSTR15 = STR15Stat

        DEX15Stat = SpecVector()
        DEX15Stat[CoreStat.STAT_DEX] = 10
        DEX15Stat[CoreStat.STAT_HP] = 170
        self.PieceDEX15 = DEX15Stat

        INT15Stat = SpecVector()
        INT15Stat[CoreStat.STAT_INT] = 10
        INT15Stat[CoreStat.STAT_HP] = 170
        self.PieceINT15 = INT15Stat

        LUK15Stat = SpecVector()
        LUK15Stat[CoreStat.STAT_LUK] = 10
        LUK15Stat[CoreStat.STAT_HP] = 170
        self.PieceLUK15 = LUK15Stat

        ALL15Stat = SpecVector()
        ALL15Stat[CoreStat.STAT_ALL] = 4
        ALL15Stat[CoreStat.STAT_HP] = 170
        self.PieceAll15 = ALL15Stat

        HP15Stat = SpecVector()
        HP15Stat[CoreStat.STAT_HP] = 670
        self.PieceHP15 = HP15Stat

        # --GPT가 작성--
        ATK15Stat = SpecVector()
        ATK15Stat[CoreStat.ATTACK_PHYSICAL] = 4
        self.PieceATK15 = ATK15Stat

        SPELL15Stat = SpecVector()
        SPELL15Stat[CoreStat.ATTACK_SPELL] = 4
        self.PieceSPELL15 = SPELL15Stat

        # 120렙 이상 방어구 주문서 30%작. 해당 스텟 7 or 올스텟 3 or HP 470, 공통: hp120
        STR30Stat = SpecVector()
        STR30Stat[CoreStat.STAT_STR] = 7
        STR30Stat[CoreStat.STAT_HP] = 120
        self.PieceSTR30 = STR30Stat

        DEX30Stat = SpecVector()
        DEX30Stat[CoreStat.STAT_DEX] = 7
        DEX30Stat[CoreStat.STAT_HP] = 120
        self.PieceDEX30 = DEX30Stat

        INT30Stat = SpecVector()
        INT30Stat[CoreStat.STAT_INT] = 7
        INT30Stat[CoreStat.STAT_HP] = 120
        self.PieceINT30 = INT30Stat

        LUK30Stat = SpecVector()
        LUK30Stat[CoreStat.STAT_LUK] = 7
        LUK30Stat[CoreStat.STAT_HP] = 120
        self.PieceLUK30 = LUK30Stat

        ALL30Stat = SpecVector()
        ALL30Stat[CoreStat.STAT_ALL] = 3
        ALL30Stat[CoreStat.STAT_HP] = 120
        self.PieceALL30 = ALL30Stat

        HP30Stat = SpecVector()
        HP30Stat[CoreStat.STAT_HP] = 470
        self.PieceHP30 = HP30Stat

        ATK30Stat = SpecVector()
        ATK30Stat[CoreStat.ATTACK_PHYSICAL] = 3
        self.PieceATK30 = ATK30Stat

        SPELL30Stat = SpecVector()
        SPELL30Stat[CoreStat.ATTACK_SPELL] = 3
        self.PieceSPELL30 = SPELL30Stat

        # 방어구 공격력 주문서 - 상승 수치는 2~3이나, 2로 가정.
        ATKStat = SpecVector()
        ATKStat[CoreStat.ATTACK_PHYSICAL] = 2
        self.ATK = ATKStat

        SPELLStat = SpecVector()
        SPELLStat[CoreStat.ATTACK_SPELL] = 2
        self.SPELL = SPELLStat

class AccessoryScrolls:
    """
    악세서리 주문서를 묘사함

    PieceSTR30: SpecVector - 악세서리 힘 주문서 30%
    PieceDEX30: SpecVector
    PieceINT30: SpecVector
    PieceLUK30: SpecVector
    PieceALL30: SpecVector - 악세서리 올스텟 주문서 30%
    ATK: SpecVector - 악세서리 공격력 주문서
    PremiumATK: SpecVector - 프리미엄 악세서리 공격력 주문서
    SPELL: SpecVector - 악세서리 마력 주문서
    PremiumSPELL: SpecVector - 프리미엄 악세서리 마력 주문서
    """

    PieceSTR30: SpecVector
    PieceDEX30: SpecVector
    PieceINT30: SpecVector
    PieceLUK30: SpecVector
    PieceALL30: SpecVector
    ATK: SpecVector
    PremiumATK: SpecVector
    SPELL: SpecVector
    PremiumSPELL: SpecVector
    Dominator: SpecVector 

    def __init__(self):
        # 악세서리 힘 주문서 30% - 상승 수치는 5
        PieceSTR30Stat = SpecVector()
        PieceSTR30Stat[CoreStat.STAT_STR] = 5
        self.PieceSTR30 = PieceSTR30Stat

        # 악세서리 덱 주문서 30% - 상승 수치는 5
        PieceDEX30Stat = SpecVector()
        PieceDEX30Stat[CoreStat.STAT_DEX] = 5
        self.PieceDEX30 = PieceDEX30Stat

        # 악세서리 인트 주문서 30% - 상승 수치는 5
        PieceINT30Stat = SpecVector()
        PieceINT30Stat[CoreStat.STAT_INT] = 5
        self.PieceINT30 = PieceINT30Stat

        # 악세서리 럭 주문서 30% - 상승 수치는 5
        PieceLUK30Stat = SpecVector()
        PieceLUK30Stat[CoreStat.STAT_LUK] = 5
        self.PieceLUK30 = PieceLUK30Stat

        # 악세서리 올스텟 주문서 30% - 각 스탯 상승 수치는 3
        PieceALL30Stat = SpecVector()
        PieceALL30Stat[CoreStat.STAT_ALL] = 3
        self.PieceALL30 = PieceALL30Stat

        # 악세서리 공격력 주문서 - 상승 수치는 2
        ATKStat = SpecVector()
        ATKStat[CoreStat.ATTACK_PHYSICAL] = 2
        self.ATK = ATKStat

        # 프리미엄 악세서리 공격력 주문서 - 상승 수치는 4
        PremiumATKStat = SpecVector()
        PremiumATKStat[CoreStat.ATTACK_PHYSICAL] = 4
        self.PremiumATK = PremiumATKStat

        # 악세서리 마력 주문서 - 상승 수치는 2
        SPELLStat = SpecVector()
        SPELLStat[CoreStat.ATTACK_SPELL] = 2
        self.SPELL = SPELLStat

        # 프리미엄 악세서리 마력 주문서 - 상승 수치는 4
        PremiumSPELLStat = SpecVector()
        PremiumSPELLStat[CoreStat.ATTACK_SPELL] = 4
        self.PremiumSPELL = PremiumSPELLStat

        dominatorStat = SpecVector()
        dominatorStat[CoreStat.STAT_ALL] = 3
        dominatorStat[CoreStat.STAT_HP] = 40
        dominatorStat[CoreStat.STAT_MP] = 40
        dominatorStat[CoreStat.ATTACK_PHYSICAL] = 3
        dominatorStat[CoreStat.ATTACK_SPELL] = 3
        self.Dominator = dominatorStat

class HeartScrolls:
    """하트 주문서를 묘사함

        PieceATK30: SpecVector - 하트 공격력 주문서 30%
        PieceSPELL30: SpecVector - 하트 마력 주문서 30
    """
    PieceATK30: SpecVector
    PieceSPELL30: SpecVector
    MagicalATK: SpecVector
    MagicalSPELL: SpecVector
    BlackHeart: SpecVector

    def __init__(self):
        # 하트 주문서 30% - 상승 수치는 5
        HeartScrollPieceATK30Stat = SpecVector()
        HeartScrollPieceATK30Stat[CoreStat.ATTACK_PHYSICAL] = 5
        self.PieceATK30 = HeartScrollPieceATK30Stat

        HeartScrollPieceSPELL30Stat = SpecVector()
        HeartScrollPieceSPELL30Stat[CoreStat.ATTACK_SPELL] = 5
        self.PieceSPELL30 = HeartScrollPieceSPELL30Stat

        BlackHeartStat = SpecVector()
        BlackHeartStat[CoreStat.ATTACK_PHYSICAL] = 7
        BlackHeartStat[CoreStat.ATTACK_SPELL] = 7
        self.BlackHeart = BlackHeartStat
        
        MagicalATKSTAT = SpecVector()
        MagicalATKSTAT[CoreStat.ATTACK_PHYSICAL] = 9
        MagicalATKSTAT[CoreStat.STAT_ALL] = 3
        
        self.MagicalATK = MagicalATKSTAT
        
        MagicalSPELLSTAT = SpecVector()
        MagicalSPELLSTAT[CoreStat.ATTACK_SPELL] = 9
        MagicalSPELLSTAT[CoreStat.STAT_ALL] = 3
        
        self.MagicalSPELL = MagicalSPELLSTAT
        

class ChaosScrolls:
    """혼돈의 주문서를 묘사함.

    Returned61: SpecVector - 공/마6 올스텟 1
    Returned62: SpecVector - 공/마6 올스텟 2
    Returned66: SpecVector - 공/마6 올스텟 6
    """    
    Returned6_1: SpecVector
    Returned6_2: SpecVector
    Returned6_6: SpecVector

    def __init__(self):
        
        ReturnedChaosScroll6_1Stat = SpecVector()
        ReturnedChaosScroll6_1Stat[CoreStat.ATTACK_PHYSICAL] = 6
        ReturnedChaosScroll6_1Stat[CoreStat.ATTACK_SPELL] = 6
        ReturnedChaosScroll6_1Stat[CoreStat.STAT_STR] = 1
        ReturnedChaosScroll6_1Stat[CoreStat.STAT_DEX] = 1
        ReturnedChaosScroll6_1Stat[CoreStat.STAT_INT] = 1
        ReturnedChaosScroll6_1Stat[CoreStat.STAT_LUK] = 1
        ReturnedChaosScroll6_1Stat[CoreStat.STAT_HP] = 10
        self.Returned6_1 = ReturnedChaosScroll6_1Stat

        ReturnedChaosScroll6_2Stat = SpecVector()
        ReturnedChaosScroll6_2Stat[CoreStat.ATTACK_PHYSICAL] = 6
        ReturnedChaosScroll6_2Stat[CoreStat.ATTACK_SPELL] = 6
        ReturnedChaosScroll6_2Stat[CoreStat.STAT_STR] = 2
        ReturnedChaosScroll6_2Stat[CoreStat.STAT_DEX] = 2
        ReturnedChaosScroll6_2Stat[CoreStat.STAT_INT] = 2
        ReturnedChaosScroll6_2Stat[CoreStat.STAT_LUK] = 2
        ReturnedChaosScroll6_2Stat[CoreStat.STAT_HP] = 20
        self.Returned6_2 = ReturnedChaosScroll6_2Stat

        ReturnedChaosScroll6_6Stat = SpecVector()
        ReturnedChaosScroll6_6Stat[CoreStat.ATTACK_PHYSICAL] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.ATTACK_SPELL] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.STAT_STR] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.STAT_DEX] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.STAT_INT] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.STAT_LUK] = 6
        ReturnedChaosScroll6_6Stat[CoreStat.STAT_HP] = 60
        self.Returned6_6 = ReturnedChaosScroll6_6Stat

class UpgradeScrolls:
    """주문서 체계 정보를 담은 클래스
    Weapon: WeaponScroll - 무기류
    Armor: ArmorScroll - 방어구
    Accessory: AccessoryScroll - 장신구
    Heart: HeartScroll - 하트 부위
    Chaos: ChaosScroll - 혼돈의 주문서류
    """    
    Weapon: WeaponScrolls
    Armor: ArmorScrolls
    Accessory: AccessoryScrolls
    Heart: HeartScrolls
    Chaos: ChaosScrolls

    def __init__(self):
        self.Weapon = WeaponScrolls()
        self.Armor = ArmorScrolls()
        self.Accessory = AccessoryScrolls()
        self.Heart = HeartScrolls()
        self.Chaos = ChaosScrolls()


class Upgrade(ABCItem):
    """주문서 업그레이드 기능을 묘사

    Args:
        ABCItem (class): 아이템 추상 클래스
        UpgradeChance (int): 업그레이드 횟수
        UpgradeHistory (list[UpgradeScroll]): 주문서 사용 내역

    Raises:
        ValueError: _description_
        ValueError: _description_
        TypeError: _description_
        ValueError: _description_
        TypeError: _description_

    """    
    UpgradeChance: int
    UpgradeHistory: list[UpgradeScrolls]
    
    def __init__(
            self, 
            itemName: str,
            requiredLevel: int,
            requiredJobType: list[JobType],
            itemBasicStat: SpecVector,
            itemPart: ItemParts,
            upgrade_chance: int,
            upgrade_history: list[UpgradeScrolls],
            server= GameServer.NormalServer
            ):
        ABCItem.__init__(
            self=self,
            itemName = itemName,
            requiredLevel = requiredLevel,
            requiredJobType = requiredJobType,
            itemBasicStat = itemBasicStat,
            itemPart = itemPart,
            server=server
        )
        
        if upgrade_chance < 0:
            raise ValueError("업그레이드 횟수는 0 이상")
        
        if upgrade_chance > 12:
            raise ValueError("업그레이드 횟수는 최대 12")
        
        self.UpgradeChance = upgrade_chance

        if not isinstance(upgrade_history,list):
            raise TypeError("인스턴스가 아님")
        
        if len(upgrade_history) > 12:
            raise ValueError("업그레이드 횟수는 최대 12")
        
        if upgrade_chance < len(upgrade_history):
            raise ValueError("업그레이드 횟수를 초과하는 주문서 입력")
        
        
        self.UpgradeHistory = upgrade_history
        self.UpgradeChance -= len(self.UpgradeHistory)

    def UpgradeSpec(self) -> SpecVector:
        """주문서 업그레이드로 인한 스펙을 계산함

        Raises:
            TypeError: _description_

        Returns:
            SpecVector: 주문서 업그레이드로 상승한 스펙을 벡터로 반환
        """
        result = SpecVector()

        # 업그레이드 요소를 더해줌
        for i, spec in enumerate(self.UpgradeHistory, start=1):
            if not isinstance(spec, SpecVector):
                raise TypeError("UpgradeHistory 내 강화 정보가 누락됨")
            result = result + spec

            # 방어구는 4번째 주문서 업그레이드가 주문의 흔적인 경우 공/마 1 추가로 오름
            if (self.ItemPart.value[ItemInfo.ItemGroup.value] == ItemType.Armor) and (i == 4):
                if spec[CoreStat.STAT_INT] > 0 or spec[CoreStat.ATTACK_SPELL] > 0:
                    result[CoreStat.ATTACK_SPELL] = result[CoreStat.ATTACK_SPELL] + 1
                else:
                    result[CoreStat.ATTACK_PHYSICAL] = result[CoreStat.ATTACK_PHYSICAL] + 1

        return result
    
    def GetUpgradeHistory(self) -> list[SpecVector]:
        result = []
        if self.ServerOption != GameServer.RebootServer:
            result = self.UpgradeHistory
        return result
    
    def GetUpgradeChance(self) -> int:
        result = 0
        if self.ServerOption != GameServer.RebootServer:
            result = self.UpgradeChance
        return result
    
    def DoUpgrade(self, scroll: UpgradeScrolls) -> bool:
        if self.UpgradeChance < 1:  return False
        if not isinstance(scroll):  return False

        self.UpgradeHistory.append(scroll)
        self.UpgradeChance -= 1

        return True
    
    def TotalSpec(self) -> tuple[SpecVector, int]:
        """주문서로 상승한 스텟을 반환함

        Returns:
            SpecVector: 주문서로 상승한 스텟 정보를 담은 SpecVector
        """
        if self.ServerOption == GameServer.RebootServer:
            return SpecVector(), 0
        else:
            return self.UpgradeSpec(), 0
    
    def Clear(self):
        """주문서 업그레이드 정보를 초기화함
        """
        self.UpgradeChance = self.UpgradeChance + len(self.UpgradeHistory)
        self.UpgradeHistory = []

    