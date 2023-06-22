from enum import Enum
from Core.SpecElements import SpecVector, CoreStat
from Core.Job import JobType, JobTypeInfo
from typing import List

class ItemSetEnum(Enum):
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
    # 럭키아이템
    Lucky = 13

class BelongedItemSet:
    def __init__(self, itemset:ItemSetEnum):
        if itemset == None:
            pass
        elif not isinstance(itemset, ItemSetEnum):
            raise TypeError("아이템 세트 속성 부여 실패")
        self.BelongedSet = itemset

class ItemSetOptionLevel(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _ in range(len(ItemSetEnum)):
            self.append(0)

    def __getitem__(self, key:ItemSetEnum):
        if not isinstance(key, ItemSetEnum):
            raise KeyError(f"Invalid Key: {key}")
        
        return super().__getitem__(key.value)
    def __setitem__(self, key:ItemSetEnum, value):
        if not isinstance(key, ItemSetEnum):
            raise KeyError(f"Invalid Key: {key}")
        
        super().__setitem__(key.value, value)
    

class ItemSet(list):
    """메이플스토리 아이템 세트에 대한 정보를 가지고 있는 클래스

    Args:
        list (_type_): ItemSetEnum과 세트 단계를 키로 사용하여 SpecVector 값을 가지는 2차원 리스트
    """

    def __init__(self, job:JobType):
        super().__init__()
        for _ in range(len(ItemSetEnum)-1):
            super().append([])
        # 메인 스텟을 불러옴            
        mainstat = job.value[JobTypeInfo.MainStat.value][0]
        substat = job.value[JobTypeInfo.SubStat.value][0]

        self.SetRootabyss(mainstat, substat)
        self.SetAbsolabs()
        self.SetArcaneshade()
        self.SetEternal()
        self.SetBossAccessory()
        self.SetDawnBoss()
        self.SetPitchedBoss()
        self.SetMeister()
        self.SetSevendays()
        self.SetMaster()
        self.SetBlack()
        self.SetDream()
        self.SetPetit()


    def __getitem__(self, key:ItemSetEnum):
        if not isinstance(key, ItemSetEnum):
            raise KeyError(f"Invalid key: {key}")
        return super().__getitem__(key.value)

    def append(self, key:ItemSetEnum, value: List[SpecVector]) -> None:
        if not isinstance(key, ItemSetEnum):
            raise KeyError(f"Invalid key: {key}")
        if not all(isinstance(item, SpecVector) for item in value):
            raise ValueError(f"Value must be a list of SpecVector, not {type(value)}")
        self[key.value] = value



    def SetRootabyss(self, mainstat, substat):
        # 루타비스 세트
        rootabyss1 = SpecVector()

        rootabyss2 = rootabyss1.copy()
        rootabyss2[mainstat] = 20
        rootabyss2[substat] = 20
        rootabyss2[CoreStat.STAT_HP] = 1000
        rootabyss2[CoreStat.STAT_MP] = 1000

        rootabyss3 = rootabyss2.copy()
        rootabyss3[CoreStat.STAT_HP_PERCENTAGE] += 10
        rootabyss3[CoreStat.STAT_MP_PERCENTAGE] += 10
        if mainstat in [CoreStat.STAT_INT]:
            rootabyss3[CoreStat.ATTACK_SPELL] += 50
        else:
            rootabyss3[CoreStat.ATTACK_PHYSICAL] += 50

        rootabyss4 = rootabyss3.copy()
        rootabyss4[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 30
        self.append(ItemSetEnum.Rootabyss, [rootabyss1, rootabyss2, rootabyss3, rootabyss4])

        #self[ItemSetEnum.Rootabyss.value] =[rootabyss1, rootabyss2, rootabyss3, rootabyss4]

    def SetAbsolabs(self):
        # Absolabs 세트
        absolabs2 = SpecVector()
        absolabs2[CoreStat.STAT_HP] = 1500
        absolabs2[CoreStat.STAT_MP] = 1500
        absolabs2[CoreStat.ATTACK_PHYSICAL] = 20  # 공격력 / 마력
        absolabs2[CoreStat.ATTACK_SPELL] = 20  # 공격력 / 마력
        absolabs2[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 10

        absolabs3 = absolabs2.copy()
        absolabs3[CoreStat.STAT_ALL] += 30  # 올스탯
        absolabs3[CoreStat.ATTACK_PHYSICAL] += 20  # 공격력 / 마력
        absolabs3[CoreStat.ATTACK_SPELL] += 20  # 공격력 / 마력
        absolabs3[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        absolabs4 = absolabs3.copy()
        absolabs4[CoreStat.ATTACK_PHYSICAL] += 25  # 공격력 / 마력
        absolabs4[CoreStat.ATTACK_SPELL] += 25  # 공격력 / 마력
        absolabs4[CoreStat.IGNORE_GUARD_PERCENTAGE] = +10  # 몬스터 방어율 무시 

        absolabs5 = absolabs4.copy()
        absolabs5[CoreStat.ATTACK_PHYSICAL] += 30  # 공격력 / 마력
        absolabs5[CoreStat.ATTACK_SPELL] += 30  # 공격력 / 마력
        absolabs5[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        
        self.append(ItemSetEnum.Absolabs, [SpecVector(), absolabs2, absolabs3, absolabs4, absolabs5])

    def SetArcaneshade(self):
        # 아케인셰이드 세트
        arcaneshade2 = SpecVector()
        arcaneshade2[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 10
        arcaneshade2[CoreStat.ATTACK_PHYSICAL] = 30
        arcaneshade2[CoreStat.ATTACK_SPELL] = 30

        arcaneshade3 = arcaneshade2.copy()
        arcaneshade3[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10
        arcaneshade3[CoreStat.ATTACK_PHYSICAL] += 30
        arcaneshade3[CoreStat.ATTACK_SPELL] += 30

        arcaneshade4 = arcaneshade3.copy()
        arcaneshade4[CoreStat.STAT_ALL] += 50
        arcaneshade4[CoreStat.ATTACK_PHYSICAL] += 35
        arcaneshade4[CoreStat.ATTACK_SPELL] += 35
        arcaneshade4[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        arcaneshade5 = arcaneshade4.copy()
        arcaneshade5[CoreStat.STAT_HP] += 2000
        arcaneshade5[CoreStat.STAT_MP] += 2000
        arcaneshade5[CoreStat.ATTACK_PHYSICAL] += 40
        arcaneshade5[CoreStat.ATTACK_SPELL] += 40
        arcaneshade5[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        self.append(ItemSetEnum.ArcaneShade, [SpecVector(), arcaneshade2, arcaneshade3, arcaneshade4, arcaneshade5])

    def SetEternal(self):
        # 에테르넬 세트
        eternal2 = SpecVector()
        eternal2[CoreStat.STAT_HP] += 2500
        eternal2[CoreStat.STAT_MP] += 2500
        eternal2[CoreStat.ATTACK_PHYSICAL] += 40
        eternal2[CoreStat.ATTACK_SPELL] += 40
        eternal2[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        eternal3 = eternal2.copy()
        eternal3[CoreStat.STAT_ALL] += 50
        eternal3[CoreStat.ATTACK_PHYSICAL] += 40
        eternal3[CoreStat.ATTACK_SPELL] += 40
        eternal3[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        eternal4 = eternal3.copy()
        eternal4[CoreStat.STAT_HP_PERCENTAGE] += 15
        eternal4[CoreStat.STAT_MP_PERCENTAGE] += 15
        eternal4[CoreStat.ATTACK_PHYSICAL] += 40
        eternal4[CoreStat.ATTACK_SPELL] += 40
        eternal4[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        eternal5 = eternal4.copy()
        eternal5[CoreStat.ATTACK_PHYSICAL] += 40
        eternal5[CoreStat.ATTACK_SPELL] += 40
        eternal5[CoreStat.IGNORE_GUARD_PERCENTAGE] += 20

        eternal6 = eternal5.copy()
        eternal6[CoreStat.STAT_HP_PERCENTAGE] += 15
        eternal6[CoreStat.STAT_MP_PERCENTAGE] += 15
        eternal6[CoreStat.ATTACK_PHYSICAL] += 40
        eternal6[CoreStat.ATTACK_SPELL] += 40
        eternal6[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 30

        eternal7 = eternal6.copy()
        eternal7[CoreStat.STAT_HP] += 2500
        eternal7[CoreStat.STAT_MP] += 2500
        eternal7[CoreStat.STAT_ALL] += 50
        eternal7[CoreStat.ATTACK_PHYSICAL] += 40
        eternal7[CoreStat.ATTACK_SPELL] += 40
        eternal7[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        eternal8 = eternal7.copy()
        eternal8[CoreStat.ATTACK_PHYSICAL] += 40
        eternal8[CoreStat.ATTACK_SPELL] += 40
        eternal8[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        self.append(ItemSetEnum.Eternel , [SpecVector(), eternal2, eternal3, eternal4, eternal5, eternal6, eternal7, eternal8])

    def SetBossAccessory(self):
        # 보스 액세서리 세트
        boss1 = SpecVector()
        
        boss2 = boss1.copy()
        
        boss3 = boss2.copy()
        boss3[CoreStat.STAT_ALL] += 10
        boss3[CoreStat.STAT_HP_PERCENTAGE] += 5
        boss3[CoreStat.STAT_MP_PERCENTAGE] += 5
        boss3[CoreStat.ATTACK_PHYSICAL] += 5
        boss3[CoreStat.ATTACK_SPELL] += 5

        boss4 = boss3.copy()

        boss5 = boss4.copy()
        boss5[CoreStat.STAT_ALL] += 10
        boss5[CoreStat.STAT_HP_PERCENTAGE] += 5
        boss5[CoreStat.STAT_MP_PERCENTAGE] += 5
        boss5[CoreStat.ATTACK_PHYSICAL] += 5
        boss5[CoreStat.ATTACK_SPELL] += 5

        boss6 = boss5.copy()

        boss7 = boss6.copy()
        boss7[CoreStat.STAT_ALL] += 10
        boss7[CoreStat.ATTACK_PHYSICAL] += 10
        boss7[CoreStat.ATTACK_SPELL] += 10
        boss7[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10

        boss8 = boss7.copy()

        boss9 = boss8.copy()
        boss9[CoreStat.STAT_ALL] += 15
        boss9[CoreStat.ATTACK_PHYSICAL] += 10
        boss9[CoreStat.ATTACK_SPELL] += 10
        boss9[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        self.append(ItemSetEnum.BossAccessory , [boss1, boss2, boss3, boss4, boss5, boss6, boss7, boss8, boss9])

    def SetDawnBoss(self):
        # 여명의 눈보라 보스 세트
        dawn1 = SpecVector()
        
        dawn2 = dawn1.copy()
        dawn2[CoreStat.STAT_ALL] += 10
        dawn2[CoreStat.STAT_HP] += 250
        dawn2[CoreStat.ATTACK_PHYSICAL] += 10
        dawn2[CoreStat.ATTACK_SPELL] += 10
        dawn2[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        dawn3 = dawn2.copy()
        dawn3[CoreStat.STAT_ALL] += 10
        dawn3[CoreStat.STAT_HP] += 250
        dawn3[CoreStat.ATTACK_PHYSICAL] += 10
        dawn3[CoreStat.ATTACK_SPELL] += 10

        dawn4 = dawn3.copy()
        dawn4[CoreStat.STAT_ALL] += 10
        dawn4[CoreStat.STAT_HP] += 250
        dawn4[CoreStat.ATTACK_PHYSICAL] += 10
        dawn4[CoreStat.ATTACK_SPELL] += 10
        dawn4[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10

        self.append(ItemSetEnum.DawnBoss , [dawn1, dawn2, dawn3, dawn4])

    def SetPitchedBoss(self):
        # 칠흑의 장신구 보스 세트
        pitched1 = SpecVector()

        pitched2 = pitched1.copy()
        pitched2[CoreStat.STAT_ALL] += 10
        pitched2[CoreStat.STAT_HP] += 250
        pitched2[CoreStat.ATTACK_PHYSICAL] += 10
        pitched2[CoreStat.ATTACK_SPELL] += 10
        pitched2[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        pitched3 = pitched2.copy()
        pitched3[CoreStat.STAT_ALL] += 10
        pitched3[CoreStat.STAT_HP] += 250
        pitched3[CoreStat.ATTACK_PHYSICAL] += 10
        pitched3[CoreStat.ATTACK_SPELL] += 10
        pitched3[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10

        pitched4 = pitched3.copy()
        pitched4[CoreStat.STAT_ALL] += 15
        pitched4[CoreStat.STAT_HP] += 375
        pitched4[CoreStat.ATTACK_PHYSICAL] += 15
        pitched4[CoreStat.ATTACK_SPELL] += 15
        pitched4[CoreStat.CRITICAL_DAMAGE] += 5

        pitched5 = pitched4.copy()
        pitched5[CoreStat.STAT_ALL] += 15
        pitched5[CoreStat.STAT_HP] += 375
        pitched5[CoreStat.ATTACK_PHYSICAL] += 15
        pitched5[CoreStat.ATTACK_SPELL] += 15
        pitched5[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        pitched6 = pitched5.copy()
        pitched6[CoreStat.STAT_ALL] += 15
        pitched6[CoreStat.STAT_HP] += 375
        pitched6[CoreStat.ATTACK_PHYSICAL] += 15
        pitched6[CoreStat.ATTACK_SPELL] += 15
        pitched6[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10

        pitched7 = pitched6.copy()
        pitched7[CoreStat.STAT_ALL] += 15
        pitched7[CoreStat.STAT_HP] += 375
        pitched7[CoreStat.ATTACK_PHYSICAL] += 15
        pitched7[CoreStat.ATTACK_SPELL] += 15
        pitched7[CoreStat.CRITICAL_DAMAGE] += 5

        pitched8 = pitched7.copy()
        pitched8[CoreStat.STAT_ALL] += 15
        pitched8[CoreStat.STAT_HP] += 375
        pitched8[CoreStat.ATTACK_PHYSICAL] += 15
        pitched8[CoreStat.ATTACK_SPELL] += 15
        pitched8[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 10

        pitched9 = pitched8.copy()
        pitched9[CoreStat.STAT_ALL] += 15
        pitched9[CoreStat.STAT_HP] += 375
        pitched9[CoreStat.ATTACK_PHYSICAL] += 15
        pitched9[CoreStat.ATTACK_SPELL] += 15
        pitched9[CoreStat.CRITICAL_DAMAGE] += 5

        self.append(ItemSetEnum.PitchedBoss , [pitched1, pitched2, pitched3, pitched4, pitched5, pitched6, pitched7, pitched8, pitched9])

    def SetMeister(self):
    # Meister 세트
        meister1 = SpecVector()

        meister2 = meister1.copy()
        meister2[CoreStat.STAT_HP] += 10
        meister2[CoreStat.STAT_MP] += 10

        meister3 = meister2.copy()
        meister3[CoreStat.ATTACK_PHYSICAL] += 40
        meister3[CoreStat.ATTACK_SPELL] += 40

        meister4 = meister3.copy()
        meister4[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 20

        self.append(ItemSetEnum.Meister , [meister1, meister2, meister3, meister4])

    def SetSevendays(self):
        # Sevendays 세트
        sevendays1 = SpecVector()

        sevendays2 = sevendays1.copy()
        sevendays2[CoreStat.IGNORE_GUARD_PERCENTAGE] += 10

        self.append(ItemSetEnum.SevenDays , [sevendays1, sevendays2])

    def SetMaster(self):
        # Master 세트
        master1 = SpecVector()

        master2 = master1.copy()
        master3 = master2.copy()
        master3[CoreStat.STAT_ALL] += 5
        master3[CoreStat.ATTACK_PHYSICAL] += 3
        master3[CoreStat.ATTACK_SPELL] += 3

        master4 = master3.copy()
        master5 = master4.copy()
        master5[CoreStat.STAT_ALL] += 10
        master5[CoreStat.ATTACK_PHYSICAL] += 7
        master5[CoreStat.ATTACK_SPELL] += 7
        
        self.append(ItemSetEnum.Master , [master1, master2, master3, master4, master5])

    def SetBlack(self):
        # Black 세트
        black1 = SpecVector()
        black2 = black1.copy()
        black3 = black2.copy()
        black4 = black3.copy()
        black5 = black4.copy()
        black5[CoreStat.STAT_ALL] += 5
        black5[CoreStat.ATTACK_PHYSICAL] += 3
        black5[CoreStat.ATTACK_SPELL] += 3

        self.append(ItemSetEnum.Black , [black1, black2, black3, black4, black5])
    
    def SetDream(self):
    # Dream 세트
        dream1 = SpecVector()
        dream1[CoreStat.ATTACK_PHYSICAL] += 7
        dream1[CoreStat.ATTACK_SPELL] += 7
        dream2 = dream1.copy()
        dream2[CoreStat.ATTACK_PHYSICAL] += 9  # 공격력 총 16 추가
        dream2[CoreStat.ATTACK_SPELL] += 9     # 마력 총 16 추가
        dream3 = dream2.copy()
        dream3[CoreStat.ATTACK_PHYSICAL] += 11  # 공격력 총 27 추가
        dream3[CoreStat.ATTACK_SPELL] += 11     # 마력 총 27 추가

        self.append(ItemSetEnum.LunarDream , [dream1, dream2, dream3])

    def SetPetit(self):
        # Petit 세트
        petit1 = SpecVector()
        petit1[CoreStat.ATTACK_PHYSICAL] += 8
        petit1[CoreStat.ATTACK_SPELL] += 8
        petit2 = petit1.copy()
        petit2[CoreStat.ATTACK_PHYSICAL] += 10  # 공격력 총 18 추가
        petit2[CoreStat.ATTACK_SPELL] += 10     # 마력 총 18 추가
        petit3 = petit2.copy()
        petit3[CoreStat.ATTACK_PHYSICAL] += 12  # 공격력 총 30 추가
        petit3[CoreStat.ATTACK_SPELL] += 12     # 마력 총 30 추가

        self.append(ItemSetEnum.LunarPetit , [petit1, petit2, petit3])


