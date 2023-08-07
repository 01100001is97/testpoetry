from Core.Enchant.Potential import PotentialOptionSlot
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Emblem
from Core.SpecElements import CoreStat, SpecVector
from Core.ReqLevel import ReqLevel


class GoldMapleLeafEmblem(Emblem):
    _itemName:str
    _requiredLevel: int
    _requiredJob: list[JobType]
    _set = None
    def __init__(
            self,
            potential: list[PotentialOptionSlot],
            addPotential: list[PotentialOptionSlot]
    ):
        self._itemName = "골드 메이플리브 엠블렘"
        self._requiredLevel = ReqLevel.Lv100.value
        self._requiredJob = [JobType.Warrior, JobType.Bowman, JobType.Magician, JobType.Thief, JobType.Pirate]

        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 10
        stat[CoreStat.ATTACK_SPELL] = 2
        stat[CoreStat.ATTACK_PHYSICAL] = 2

        Emblem.__init__(
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
