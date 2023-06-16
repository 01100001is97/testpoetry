from Core.SpecElements import CoreStat, CreateSpecVector
from enum import Enum
from Core.Job import JobName

# 유니온 시스템이 GMS에서 Legion인듯. C 유니온이랑 헷갈려서 비슷한 이름으로 네이밍한듯

class LegionGrade(Enum):
    SS = 0
    SSS = 1

class LegionOption(Enum):
    Str = (CreateSpecVector([CoreStat.STAT_STR_FIXED], 80), CreateSpecVector([CoreStat.STAT_STR_FIXED], 100))
    Dex = (CreateSpecVector([CoreStat.STAT_DEX_FIXED], 80), CreateSpecVector([CoreStat.STAT_DEX_FIXED], 100))
    Int = (CreateSpecVector([CoreStat.STAT_INT_FIXED], 80), CreateSpecVector([CoreStat.STAT_INT_FIXED], 100))
    Luk = (CreateSpecVector([CoreStat.STAT_LUK_FIXED], 80), CreateSpecVector([CoreStat.STAT_LUK_FIXED], 100))
    Xenon = (CreateSpecVector([CoreStat.STAT_STR_FIXED, CoreStat.STAT_DEX_FIXED, CoreStat.STAT_LUK_FIXED], 40), 
            CreateSpecVector([CoreStat.STAT_STR_FIXED, CoreStat.STAT_DEX_FIXED, CoreStat.STAT_LUK_FIXED], 50))
   
    Hp = (CreateSpecVector([CoreStat.STAT_HP_FIXED], 2000), CreateSpecVector([CoreStat.STAT_HP_FIXED], 2500))
    HpPercent = (CreateSpecVector([CoreStat.STAT_HP_PERCENTAGE], 5), CreateSpecVector([CoreStat.STAT_HP_PERCENTAGE], 6))
    MpPercent = (CreateSpecVector([CoreStat.STAT_MP_PERCENTAGE], 5), CreateSpecVector([CoreStat.STAT_MP_PERCENTAGE], 6))
    CritPercent = (CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 4), CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 5))
    CritDamage = (CreateSpecVector([CoreStat.CRITICAL_DAMAGE], 5), CreateSpecVector([CoreStat.CRITICAL_DAMAGE], 6))
    SummonDuration = (10, 12)
    Aran = None
    Evan = None
    CooldownPercent = (5,6)
    Phantom = None
    IgnoreGuard = (CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 5), CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 6))
    BossDamage = (CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 4), CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 5))
    BuffDuration = (20, 25)
    Zero = None
    WildHunter = (16, 20)
    DemonSlayer = None
    MapleM = (CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 20), )


# 유니온 대원
class LegionMember:
    _Job: JobName
    _Grade: LegionGrade
    _Option: LegionOption

    def __init__(self, job:JobName, grade:LegionGrade):
        if not isinstance(job, JobName):
            raise ValueError("job must be an instance of JobName")
        if not isinstance(grade, LegionGrade):
            raise ValueError("grade must be an instance of LegionGrade")
        
        self.Job = job
        self.Grade = grade

        if job in [
            JobName.Viper,
            JobName.Striker,
            JobName.Adele,
            JobName.Ark,
            JobName.Kaiser,
            JobName.CannonShooter,
            JobName.Paladin,
            JobName.Hero
        ]:
            self._Option = LegionOption.Str
        elif job in [
            JobName.BowMaster,
            JobName.AngelicBuster,
            JobName.WindBreaker,
            JobName.Kain,
            JobName.PathFinder
        ]:
            self._Option = LegionOption.Dex
        elif job in [
            JobName.Lara,
            JobName.Luminous,
            JobName.BattleMage,
            JobName.Bishop,
            JobName.ArchmageTC,
            JobName.Illium,
            JobName.Kinesis,
            JobName.FlameWizard
        ]:
            self._Option = LegionOption.Int
        elif job in [
            JobName.NightWalker,
            JobName.DualBlade,
            JobName.Shadower,
            JobName.Cadena,
            JobName.Kali,
            JobName.Hoyoung
        ]:
            self._Option = LegionOption.Luk
        elif job == JobName.Xenon:
            self._Option = LegionOption.Xenon
        elif job in [
            JobName.Mikhail,
            JobName.SoulMaster
        ]:
            self._Option = LegionOption.Hp
        elif job == JobName.DarkKnight:
            self._Option = LegionOption.HpPercent
        elif job == JobName.ArchmageFP:
            self._Option = LegionOption.MpPercent
        elif job in [
            JobName.NightLord,
            JobName.Marksman
        ]:
            self._Option = LegionOption.CritPercent
        elif job == JobName.Eunwol:
            self._Option = LegionOption.CritDamage
        elif job == JobName.Captain:
            self._Option = LegionOption.SummonDuration
        elif job == JobName.Aran:
            self._Option = LegionOption.Aran
        elif job == JobName.Evan:
            self._Option = LegionOption.Evan
        elif job == JobName.Mercedes:
            self._Option = LegionOption.CooldownPercent
        elif job == JobName.Phantom:
            self._Option = LegionOption.Phantom
        elif job == JobName.Blaster:
            self._Option = LegionOption.IgnoreGuard
        elif job == JobName.DemonSlayer:
            self._Option = LegionOption.DemonSlayer
        elif job == JobName.DemonAvenger:
            self._Option = LegionOption.BossDamage
        elif job == JobName.WildHunter:
            self._Option = LegionOption.WildHunter
        elif job == JobName.Mechanic:
            self._Option = LegionOption.BuffDuration
        elif job == JobName.Zero:
            self._Option = LegionOption.Zero
        else:
            raise ValueError(f"Unrecognized job: {job}")


# 유니온 8500기준 (42캐릭 합 8500), 대원은 37명. 아래 목록을 취사선택할 것.
class Legion(Enum):

    HeroSS = LegionMember(JobName.Hero, LegionGrade.SS)
    PaladinSS = LegionMember(JobName.Paladin, LegionGrade.SS)
    DarkKnightSS = LegionMember(JobName.DarkKnight, LegionGrade.SS)

    BowMasterSS = LegionMember(JobName.BowMaster, LegionGrade.SS)
    MarksmanSS = LegionMember(JobName.Marksman, LegionGrade.SS)
    PathFinderSS = LegionMember(JobName.PathFinder, LegionGrade.SS)

    ArchmageFPSS = LegionMember(JobName.ArchmageFP, LegionGrade.SS)
    ArchmageTCSS = LegionMember(JobName.ArchmageTC, LegionGrade.SS)
    BishopSS = LegionMember(JobName.Bishop, LegionGrade.SS)

    NightLordSS = LegionMember(JobName.NightLord, LegionGrade.SS)
    ShadowerSS = LegionMember(JobName.Shadower, LegionGrade.SS)
    DualBladeSS = LegionMember(JobName.DualBlade, LegionGrade.SS)

    ViperSS = LegionMember(JobName.Viper, LegionGrade.SS)
    CaptainSS = LegionMember(JobName.Captain, LegionGrade.SS)
    CannonShooterSS = LegionMember(JobName.CannonShooter, LegionGrade.SS)

    MikhailSS = LegionMember(JobName.Mikhail, LegionGrade.SS)
    SoulMasterSS = LegionMember(JobName.SoulMaster, LegionGrade.SS)
    FlameWizardSS = LegionMember(JobName.FlameWizard, LegionGrade.SS)
    WindBreakerSS = LegionMember(JobName.WindBreaker, LegionGrade.SS)
    NightWalkerSS = LegionMember(JobName.NightWalker, LegionGrade.SS)
    StrikerSS = LegionMember(JobName.Striker, LegionGrade.SS)

    BattleMageSS = LegionMember(JobName.BattleMage, LegionGrade.SS)
    WildHunterSS = LegionMember(JobName.WildHunter, LegionGrade.SS)
    MechanicSS = LegionMember(JobName.Mechanic, LegionGrade.SS)
    MechanicSSS = LegionMember(JobName.Mechanic, LegionGrade.SSS)
    BlasterSS = LegionMember(JobName.Blaster, LegionGrade.SS)
    XenonSS = LegionMember(JobName.Xenon, LegionGrade.SS)

    DemonSlayerSS = LegionMember(JobName.DemonSlayer, LegionGrade.SS)
    DemonAvengerSS = LegionMember(JobName.DemonAvenger, LegionGrade.SS)

    AranSS = LegionMember(JobName.Aran, LegionGrade.SS)
    MercedesSS = LegionMember(JobName.Mercedes, LegionGrade.SS)
    MercedesSSS = LegionMember(JobName.Mercedes, LegionGrade.SSS)
    EvanSS = LegionMember(JobName.Evan, LegionGrade.SS)
    LuminousSS = LegionMember(JobName.Luminous, LegionGrade.SS)
    PhantomSS = LegionMember(JobName.Phantom, LegionGrade.SS)
    EunwolSS = LegionMember(JobName.Eunwol, LegionGrade.SS)
    EunwolSSS = LegionMember(JobName.Eunwol, LegionGrade.SSS)

    KaiserSS = LegionMember(JobName.Kaiser, LegionGrade.SS)
    AngelicBusterSS = LegionMember(JobName.AngelicBuster, LegionGrade.SS)
    CadenaSS = LegionMember(JobName.Cadena, LegionGrade.SS)
    KainSS = LegionMember(JobName.Kain, LegionGrade.SS)

    IlliumSS = LegionMember(JobName.Illium, LegionGrade.SS)
    ArkSS = LegionMember(JobName.Ark, LegionGrade.SS)
    AdeleSS = LegionMember(JobName.Adele, LegionGrade.SS)
    KaliSS = LegionMember(JobName.Kali, LegionGrade.SS)

    HoyoungSS = LegionMember(JobName.Hoyoung, LegionGrade.SS)
    LaraSS = LegionMember(JobName.Lara, LegionGrade.SS)

    ZeroSS = LegionMember(JobName.Zero, LegionGrade.SS)

    KinesisSS = LegionMember(JobName.Kinesis, LegionGrade.SS)
