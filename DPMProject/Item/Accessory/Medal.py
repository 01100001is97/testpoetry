from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Medal
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel


class SevenDayMonsterParker(Medal):
    def __init__(
            self, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "칠요의 몬스터파커"
        self.RequiredLevel = ReqLevel.Lv130.value
        self.BelongedItemSet = ItemSetEnum.SevenDays

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 7
        stat[CoreStat.STAT_DEX] = 7
        stat[CoreStat.STAT_INT] = 7
        stat[CoreStat.STAT_LUK] = 7
        stat[CoreStat.ATTACK_PHYSICAL] = 7
        stat[CoreStat.ATTACK_SPELL] = 7
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        Medal.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            itemset=self.BelongedItemSet,
            server=server
        )

class ChaosVellumCrusher(Medal):
    def __init__(
        self,
        server=GameServer.NormalServer
    ):
        self.ItemName = "카오스 벨룸 킬러"
        self.RequiredLevel = 0

        stat = SpecVector()
        stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 5

        Medal.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            server=server
        )
