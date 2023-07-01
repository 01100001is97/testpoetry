from Core.Enchant.Potential import PotentialOptionSlot
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import SubWeapon, Blade, Shield
from Core.SpecElements import CoreStat, SpecVector
from Core.ReqLevel import ReqLevel

# 백금의 서
class WhiteGoldBook(SubWeapon):
    _itemName:str
    _requiredLevel: int
    _requiredJob: list[JobType]
    _set = None
    def __init__(
            self,
            potential: list[PotentialOptionSlot],
            addPotential: list[PotentialOptionSlot]
    ):
        self._itemName = "백금의 서"
        self._requiredLevel = ReqLevel.Lv100.value
        self._requiredJob = [JobType.Magician]

        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.ATTACK_SPELL] = 3

        SubWeapon.__init__(
            self=self,
            itemName=self._itemName,
            requiredJobType=self._requiredJob,
            requiredLevel=self._requiredLevel,
            itemBasicStat=stat,
            potentialOptionList=potential,
            itemset=self._set,
            additionalPotentialOptionList=addPotential,
            server=GameServer.NormalServer
        )


# 청은의 서
class MetallicBlueBook(SubWeapon): pass

# 적녹의 서
class RustyBook(SubWeapon): pass


# 패스파인더 보조 퍼펙트 렐릭
class PerfectRelic(SubWeapon):
    _itemName:str
    _requiredLevel: int
    _requiredJob: list[JobType]
    _set = None
    def __init__(
            self,
            potential: list[PotentialOptionSlot],
            addPotential: list[PotentialOptionSlot]
    ):
        self._itemName = "퍼펙트 렐릭"
        self._requiredLevel = ReqLevel.Lv100.value
        self._requiredJob = [JobType.Bowman]

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.ATTACK_PHYSICAL] = 3

        SubWeapon.__init__(
            self=self,
            itemName=self._itemName,
            requiredJobType=self._requiredJob,
            requiredLevel=self._requiredLevel,
            itemBasicStat=stat,
            potentialOptionList=potential,
            itemset=self._set,
            additionalPotentialOptionList=addPotential,
            server=GameServer.NormalServer
        )

