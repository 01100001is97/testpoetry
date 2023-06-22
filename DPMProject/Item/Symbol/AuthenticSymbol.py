from Item.ItemGroup import Symbol
from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat


class AuthenticSymbol(Symbol):
    _authXenonBasicStat = 144
    _authXenonLevelStat = 96
    _authDemonBasicStat = 6300
    _authDemonLevelStat = 4200
    _authBasicStat = 300
    _authLevelStat = 200
    _basicForce = 0
    _levelForce = 10
    _MaxLevel = 11
    
    def __init__(
            self, 
            requiredJobType: list[JobType], 
            symbolLevel:int,
    ):
        basicsv = SpecVector()
        levelsv = SpecVector()
        job = requiredJobType[0]
        self.ItemName = "어센틱 심볼"
        symbolLevel = min(symbolLevel, self._MaxLevel)

        if job == JobType.Xenon:
            basicsv[CoreStat.STAT_STR_FIXED] = self._authXenonBasicStat
            basicsv[CoreStat.STAT_DEX_FIXED] = self._authXenonBasicStat
            basicsv[CoreStat.STAT_LUK_FIXED] = self._authXenonBasicStat
            levelsv[CoreStat.STAT_STR_FIXED] = self._authXenonLevelStat
            levelsv[CoreStat.STAT_DEX_FIXED] = self._authXenonLevelStat
            levelsv[CoreStat.STAT_LUK_FIXED] = self._authXenonLevelStat
        elif job == JobType.DemonAvenger:
            basicsv[CoreStat.STAT_HP_FIXED] = self._authDemonBasicStat
            levelsv[CoreStat.STAT_HP_FIXED] = self._authDemonLevelStat
        elif job in [JobType.Worrior, JobType.Pirate]:
            basicsv[CoreStat.STAT_STR_FIXED] = self._authBasicStat
            levelsv[CoreStat.STAT_STR_FIXED] = self._authLevelStat
        elif job in [JobType.Bowman, JobType.DexPirate]:
            basicsv[CoreStat.STAT_DEX_FIXED] = self._authBasicStat
            levelsv[CoreStat.STAT_DEX_FIXED] = self._authLevelStat
        elif job == JobType.Magician:
            basicsv[CoreStat.STAT_INT_FIXED] = self._authBasicStat
            levelsv[CoreStat.STAT_INT_FIXED] = self._authLevelStat
        elif job == JobType.Theif:
            basicsv[CoreStat.STAT_LUK_FIXED] = self._authBasicStat
            levelsv[CoreStat.STAT_LUK_FIXED] = self._authLevelStat
        else:
            raise ValueError("어센틱심볼 직업 오류")

        self._symbolBasicStat = basicsv
        self._symbolLevelStat = levelsv

        Symbol.__init__(
            self,
            itemName=self.ItemName,
            requiredJobType=requiredJobType,
            Symbollevel=symbolLevel,
            basicForce=self._basicForce,
            symbolBasicStat=self._symbolBasicStat,
            symbolLevelStat=self._symbolLevelStat,
        )