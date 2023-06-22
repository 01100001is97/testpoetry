from Item.ItemGroup import Symbol
from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat

class ArcaneSymbol(Symbol):
    _ArcaneXenonBasicStat = 96
    _ArcaneXenonLevelStat = 48
    _ArcaneDemonBasicStat = 2100
    _ArcaneDemonLevelStat = 4200
    _ArcaneBasicStat = 200
    _ArcaneLevelStat = 100
    _basicForce = 20
    _levelForce = 10
    _MaxLevel = 20
    def __init__(
            self, 
            requiredJobType: list[JobType], 
            symbollevel:int,
    ):
        basicsv = SpecVector()
        levelsv = SpecVector()
        # 아케인심볼 jobtype은 1개값만 받음.
        job = requiredJobType[0]
        self.ItemName = "아케인 심볼"
        symbollevel = min(symbollevel, self._MaxLevel)

        if job == JobType.Xenon:
            basicsv[CoreStat.STAT_STR_FIXED] = self._ArcaneXenonBasicStat
            basicsv[CoreStat.STAT_DEX_FIXED] = self._ArcaneXenonBasicStat
            basicsv[CoreStat.STAT_LUK_FIXED] = self._ArcaneXenonBasicStat
            levelsv[CoreStat.STAT_STR_FIXED] = self._ArcaneXenonLevelStat
            levelsv[CoreStat.STAT_DEX_FIXED] = self._ArcaneXenonLevelStat
            levelsv[CoreStat.STAT_LUK_FIXED] = self._ArcaneXenonLevelStat
        elif job == JobType.DemonAvenger:
            basicsv[CoreStat.STAT_HP_FIXED] = self._ArcaneDemonBasicStat
            levelsv[CoreStat.STAT_HP_FIXED] = self._ArcaneDemonLevelStat
        elif job in [JobType.Worrior, JobType.Pirate]:
            basicsv[CoreStat.STAT_STR_FIXED] = self._ArcaneBasicStat
            levelsv[CoreStat.STAT_STR_FIXED] = self._ArcaneLevelStat
        elif job in [JobType.Bowman, JobType.DexPirate]:
            basicsv[CoreStat.STAT_DEX_FIXED] = self._ArcaneBasicStat
            levelsv[CoreStat.STAT_DEX_FIXED] = self._ArcaneLevelStat
        elif job == JobType.Magician:
            basicsv[CoreStat.STAT_INT_FIXED] = self._ArcaneBasicStat
            levelsv[CoreStat.STAT_INT_FIXED] = self._ArcaneLevelStat
        elif job == JobType.Theif:
            basicsv[CoreStat.STAT_LUK_FIXED] = self._ArcaneBasicStat
            levelsv[CoreStat.STAT_LUK_FIXED] = self._ArcaneLevelStat
        else:
            raise ValueError("아케인심볼 직업 오류")

        self._symbolBasicStat = basicsv
        self._symbolLevelStat = levelsv

    
        Symbol.__init__(
            self,
            itemName=self.ItemName,
            requiredJobType=requiredJobType,
            Symbollevel=symbollevel,
            basicForce=self._basicForce,
            symbolBasicStat=self._symbolBasicStat,
            symbolLevelStat=self._symbolLevelStat,
        )

