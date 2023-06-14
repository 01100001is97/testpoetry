from enum import Enum

class ItemSet(Enum):
    # 방어구
    Rootabyss = 0
    Absolabs = 1
    ArcaneShade = 2
    Eternel = 3
    # 장신구
    BossAccessory = 4
    DawnBoss = 5
    PitchedBoss = 6
    Meister = 7
    SevenDays = 8
    # 캐시 장비
    Master = 9
    Black = 10
    # 펫 버프
    LunarDream = 11
    LunarPetit = 12

class BelongedItemSet:
    BelongedItemSet: ItemSet

    def __init__(self, itemset:ItemSet):
        if itemset == None:
            pass
        elif not isinstance(itemset, ItemSet):
            raise TypeError("아이템 세트 속성 부여 실패")
        self.BelongedSet = itemset