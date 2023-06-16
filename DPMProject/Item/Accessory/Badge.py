from Core.Server import GameServer
from Item.ItemGroup import Badge
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel


class CristalVentusBadge(Badge):
    def __init__(
            self, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "크리스탈 웬투스 뱃지"
        self.RequiredLevel = ReqLevel.Lv130.value
        self.BelongedItemSet = ItemSetEnum.BossAccessory

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.ATTACK_PHYSICAL] = 5
        stat[CoreStat.ATTACK_SPELL] = 5
    
        Badge.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            itemset=self.BelongedItemSet,
            server=server
        )

class SevenDaysBadge(Badge):
    def __init__(self, server=GameServer.NormalServer):

        itemName = "칠요의 뱃지"
        requiredLevel = 100

        itemBasicStat = SpecVector()
        itemBasicStat[CoreStat.STAT_STR] = 7
        itemBasicStat[CoreStat.STAT_DEX] = 7
        itemBasicStat[CoreStat.STAT_INT] = 7
        itemBasicStat[CoreStat.STAT_LUK] = 7
        itemBasicStat[CoreStat.ATTACK_PHYSICAL] = 7
        itemBasicStat[CoreStat.ATTACK_SPELL] = 7
        itemBasicStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        itemset = ItemSetEnum.SevenDays

        Badge.__init__(
            self=self, 
            itemName=itemName, 
            requiredLevel= requiredLevel, 
            itemBasicStat= itemBasicStat, 
            itemset= itemset, 
            server= server
            )

class GenesisBadge(Badge):
    def __init__(
        self,
        server = GameServer.NormalServer
    ):
        self.ItemName = "창세의 뱃지"
        self.RequiredLevel = ReqLevel.Lv200.value
        self.BelongedItemSet = ItemSetEnum.PitchedBoss

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 15
        stat[CoreStat.STAT_DEX] = 15
        stat[CoreStat.STAT_INT] = 15
        stat[CoreStat.STAT_LUK] = 15
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        Badge.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            itemset=self.BelongedItemSet,
            server=server
        )
