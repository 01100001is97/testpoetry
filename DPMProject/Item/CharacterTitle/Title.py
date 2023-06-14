from Item.ItemGroup import CharacterTitle
from Core.ABCItem import ItemParts
from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat

class WellKnowingMaple(CharacterTitle):
    def __init__(self):
        self.ItemName = "메이플을 잘 아는"
        self.RequiredLevel = 0
        
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 10
        stat[CoreStat.STAT_HP] = 500
        stat[CoreStat.ATTACK_PHYSICAL] = 5
        stat[CoreStat.ATTACK_SPELL] = 5
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10
        self.ItemBasicStat = stat

        CharacterTitle.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=self.ItemBasicStat
        )

class KingOfRootAbyss(CharacterTitle):
    def __init__(self):
        self.ItemName = "킹 오브 루타비스"
        self.RequiredLevel = 0
        
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 8
        stat[CoreStat.STAT_HP] = 300
        stat[CoreStat.STAT_MP] = 300
        stat[CoreStat.ATTACK_PHYSICAL] = 3
        stat[CoreStat.ATTACK_SPELL] = 3
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5
        stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 5

        self.ItemBasicStat = stat

        CharacterTitle.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=self.ItemBasicStat
        )

class YetiPinkBean(CharacterTitle):
    def __init__(self):
        self.ItemName = "예티 X 핑크빈"
        self.RequiredLevel = 0
        
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 20
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10
        stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 10

        self.ItemBasicStat = stat

        CharacterTitle.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=self.ItemBasicStat
        )

class IAmHeist(CharacterTitle):
    def __init__(self):
        self.ItemName = "헤이스트 칭호"
        self.RequiredLevel = 0
        
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 50
        stat[CoreStat.STAT_HP] = 2500
        stat[CoreStat.STAT_MP] = 2500
        stat[CoreStat.ATTACK_PHYSICAL] = 20
        stat[CoreStat.ATTACK_SPELL] = 20
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 30
        stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 30

        self.ItemBasicStat = stat

        CharacterTitle.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=self.ItemBasicStat
        )