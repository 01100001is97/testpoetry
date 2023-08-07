from Core.SpecElements import CoreStat, CreateSpecVector
from enum import Enum
from Core.Job import JobName

# 유니온 시스템이 GMS에서 Legion인듯. C 유니온이랑 헷갈려서 비슷한 이름으로 네이밍한듯

class LegionGrade(Enum):
    SS = 0
    SSS = 1

class LegionOption(Enum):
    """유니온 시스템의 옵션을 저장하는 열거형

    Args:
        Enum (tuple): 0: SS등급 옵션, 1: SSS등급 옵션
    """
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
    """유니온 대원효과를 나타내는 클래스(직업, 등급, 등급별 옵션)

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
    """
    Job: JobName
    Grade: LegionGrade
    Option: LegionOption

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
            self.Option = LegionOption.Str
        elif job in [
            JobName.BowMaster,
            JobName.AngelicBuster,
            JobName.WindBreaker,
            JobName.Kain,
            JobName.PathFinder
        ]:
            self.Option = LegionOption.Dex
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
            self.Option = LegionOption.Int
        elif job in [
            JobName.NightWalker,
            JobName.DualBlade,
            JobName.Shadower,
            JobName.Cadena,
            JobName.Kali,
            JobName.Hoyoung
        ]:
            self.Option = LegionOption.Luk
        elif job == JobName.Xenon:
            self.Option = LegionOption.Xenon
        elif job in [
            JobName.Mikhail,
            JobName.SoulMaster
        ]:
            self.Option = LegionOption.Hp
        elif job == JobName.DarkKnight:
            self.Option = LegionOption.HpPercent
        elif job == JobName.ArchmageFP:
            self.Option = LegionOption.MpPercent
        elif job in [
            JobName.NightLord,
            JobName.Marksman
        ]:
            self.Option = LegionOption.CritPercent
        elif job == JobName.Eunwol:
            self.Option = LegionOption.CritDamage
        elif job == JobName.Captain:
            self.Option = LegionOption.SummonDuration
        elif job == JobName.Aran:
            self.Option = LegionOption.Aran
        elif job == JobName.Evan:
            self.Option = LegionOption.Evan
        elif job == JobName.Mercedes:
            self.Option = LegionOption.CooldownPercent
        elif job == JobName.Phantom:
            self.Option = LegionOption.Phantom
        elif job == JobName.Blaster:
            self.Option = LegionOption.IgnoreGuard
        elif job == JobName.DemonSlayer:
            self.Option = LegionOption.DemonSlayer
        elif job == JobName.DemonAvenger:
            self.Option = LegionOption.BossDamage
        elif job == JobName.WildHunter:
            self.Option = LegionOption.WildHunter
        elif job == JobName.Mechanic:
            self.Option = LegionOption.BuffDuration
        elif job == JobName.Zero:
            self.Option = LegionOption.Zero
        elif job == JobName.MapleM:
            self.Option = LegionOption.MapleM
        else:
            raise ValueError(f"Unrecognized job: {job}")


# 유니온 8500기준 (42캐릭 합 8500), 대원은 37명. 아래 목록을 취사선택할 것.
LEGION_8500_MAX_MEMBER = 37 

class Legion(Enum):
    """유니온 대원효과 중 등급과 효과를 나열한 열거형

    Args:
        Enum (LegionMember): 0: 직업 이름 열거형, 1: 등급
    """
    HeroSS = LegionMember(JobName.Hero, LegionGrade.SS)
    PaladinSS = LegionMember(JobName.Paladin, LegionGrade.SS)
    DarkKnightSS = LegionMember(JobName.DarkKnight, LegionGrade.SS)

    BowMasterSS = LegionMember(JobName.BowMaster, LegionGrade.SS)
    MarksmanSS = LegionMember(JobName.Marksman, LegionGrade.SS)
    PathFinderSS = LegionMember(JobName.PathFinder, LegionGrade.SS)
    PathFinderSSS = LegionMember(JobName.PathFinder, LegionGrade.SSS)

    ArchmageFPSS = LegionMember(JobName.ArchmageFP, LegionGrade.SS)
    ArchmageTCSS = LegionMember(JobName.ArchmageTC, LegionGrade.SS)
    ArchmageTCSSS = LegionMember(JobName.ArchmageTC, LegionGrade.SSS)
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
    HoyoungSSS = LegionMember(JobName.Hoyoung, LegionGrade.SSS)
    LaraSS = LegionMember(JobName.Lara, LegionGrade.SS)

    ZeroSS = LegionMember(JobName.Zero, LegionGrade.SS)

    KinesisSS = LegionMember(JobName.Kinesis, LegionGrade.SS)

    MapleM = LegionMember(JobName.MapleM, LegionGrade.SS)

# SSS 3개 가정 - 메카닉, 메르세데스, 은월
Union8500_archmageTC = [
    # 크확
    Legion.MarksmanSS,
    Legion.NightLordSS,
    # 벞지
    Legion.MechanicSSS,
    # 쿨감
    Legion.MercedesSSS,
    # 보공, 데미지류
    Legion.DemonAvengerSS,
    Legion.WildHunterSS,
    # 방어율 무시
    Legion.BlasterSS,
    # 크리티컬 데미지
    Legion.EunwolSSS,
    # 공마
    Legion.MapleM,
    # 소환수 지속
    Legion.CaptainSS,
    # Int
    Legion.ArchmageTCSSS,
    Legion.BishopSS,
    Legion.BattleMageSS,
    Legion.LuminousSS,
    Legion.FlameWizardSS,
    Legion.KinesisSS,
    Legion.IlliumSS,
    # Luk
    Legion.NightWalkerSS,
    Legion.ShadowerSS,
    Legion.DualBladeSS,
    Legion.CadenaSS,
    Legion.HoyoungSS,
    Legion.XenonSS
]


Union8500_PathFinder = [
    # 크확
    Legion.MarksmanSS,
    Legion.NightLordSS,
    # 벞지
    Legion.MechanicSSS,
    # 쿨감
    Legion.MercedesSSS,
    # 보공, 데미지류
    Legion.DemonAvengerSS,
    Legion.WildHunterSS,
    # 방어율 무시
    Legion.BlasterSS,
    # 크리티컬 데미지
    Legion.EunwolSSS,
    # 공마
    Legion.MapleM,
    # 소환수 지속
    Legion.CaptainSS,
    # Dex
    Legion.BowMasterSS,
    Legion.WindBreakerSS,
    Legion.KainSS,
    Legion.PathFinderSSS,
    # Str
    Legion.ViperSS,
    Legion.StrikerSS,
    Legion.AdeleSS,
    Legion.ArkSS,
    Legion.KaiserSS,
    Legion.CannonShooterSS,
    Legion.PaladinSS,
    Legion.HeroSS
]

Union8500_Hoyoung = [
    # 크확
    Legion.MarksmanSS,
    Legion.NightLordSS,
    # 벞지
    Legion.MechanicSSS,
    # 쿨감
    Legion.MercedesSSS,
    # 보공, 데미지류
    Legion.DemonAvengerSS,
    Legion.WildHunterSS,
    # 방어율 무시
    Legion.BlasterSS,
    # 크리티컬 데미지
    Legion.EunwolSSS,
    # 공마
    Legion.MapleM,
    # 소환수 지속
    Legion.CaptainSS,
    # 럭
    Legion.NightWalkerSS,
    Legion.DualBladeSS,
    Legion.ShadowerSS,
    Legion.CadenaSS,
    Legion.KaliSS,
    Legion.HoyoungSSS,
    # 덱
    Legion.BowMasterSS,
    Legion.AngelicBusterSS,
    Legion.WindBreakerSS,
    Legion.KainSS,
    Legion.PathFinderSS
]
