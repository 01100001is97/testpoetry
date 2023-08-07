from enum import Enum
from Core.SpecElements import CoreStat

class JobTypeInfo(Enum):
    """JobType의 각 항목이 의미하는 열거

    Args:
        Enum (_type_): _description_
    """
    MainStat = 0
    SubStat = 1

class JobType(Enum):
    """직업별 주스텟, 부스텟

    Args:
        Enum (tuple(tuple(main stat),(sub stat))):
    """    
    # 히어로, 팔라딘, 다크나이트, 소울마스터, 미하일, 블래스터, 데몬슬레이어, 아란, 카이저, 아델, 제로
    Warrior = ((CoreStat.STAT_STR,),(CoreStat.STAT_DEX,))
    # 데벤
    DemonAvenger = ((CoreStat.STAT_HP,),)
    # 보우마스터, 신궁, 패스파인더, 윈드브레이커, 와일드헌터, 메르세데스, 카인
    Bowman = ((CoreStat.STAT_DEX,),(CoreStat.STAT_STR,))
    # 불독, 썬콜, 비숍, 플위, 배틀메이지, 에반, 루미너스, 일리움, 라라, 키네시스
    Magician = ((CoreStat.STAT_INT,),(CoreStat.STAT_LUK,))
    # 나이트로드, 나이트워커, 팬텀, 호영, 칼리
    Thief = ((CoreStat.STAT_LUK,),(CoreStat.STAT_DEX,))
    # 섀도어, 듀얼블레이드, 카데나
    MeleeTheif = ((CoreStat.STAT_LUK,),(CoreStat.STAT_DEX, CoreStat.STAT_STR))
    # 바이퍼, 캐논슈터, 스트라이커, 은월, 아크
    Pirate = ((CoreStat.STAT_STR,),(CoreStat.STAT_DEX,))
    # 캡틴, 메카닉, 엔버
    DexPirate = ((CoreStat.STAT_DEX,),(CoreStat.STAT_STR,))
    # 제논
    Xenon = ((CoreStat.STAT_STR, CoreStat.STAT_DEX, CoreStat.STAT_LUK),)
    

class JobGroup(Enum):
    """직업군

    Args:
        enum (_type_): 모험가, 시그너스 기사단, 레지스탕스, 데몬, 영웅, 노바, 레프, 아니마, 초월자, 프렌즈
    """    
    Adventurer = "모험가"
    CygnusKnights = "시그너스 기사단"
    Resistance = "레지스탕스"
    Demon = "데몬"
    Heros = "영웅"
    Nova = "노바"
    Flora = "레프"
    Anima = "아니마"
    Overlord = "초월자"
    Friends = "프렌즈"


class JobNameInfo(Enum):
    name = 0
    type = 1
    group = 2

class JobName(Enum):
    """직업 상세 정보

    Args:
        enum(tuple) :(이름, 직업 계열, 직업군)
    """

    # 모험가 전사
    Hero = ("히어로", JobType.Warrior, JobGroup.Adventurer)
    Paladin = ("팔라딘", JobType.Warrior, JobGroup.Adventurer)
    DarkKnight = ("다크나이트", JobType.Warrior, JobGroup.Adventurer)

    # 모험가 궁수
    BowMaster = ("보우마스터", JobType.Bowman, JobGroup.Adventurer)
    Marksman = ("신궁", JobType.Bowman, JobGroup.Adventurer)
    PathFinder = ("패스파인더", JobType.Bowman, JobGroup.Adventurer)

    # 모험가 법사
    ArchmageFP = ("아크메이지(불,독)", JobType.Magician, JobGroup.Adventurer)
    ArchmageTC = ("아크메이지(얼음,번개)", JobType.Magician, JobGroup.Adventurer)
    Bishop = ("비숍", JobType.Magician, JobGroup.Adventurer)

    # 모험가 도적
    NightLord = ("나이트로드", JobType.Thief, JobGroup.Adventurer)
    Shadower = ("섀도어", JobType.Thief, JobGroup.Adventurer)
    DualBlade = ("듀얼 블레이드", JobType.MeleeTheif, JobGroup.Adventurer)
    
    # 모험가 해적
    Viper = ("바이퍼", JobType.Pirate, JobGroup.Adventurer)
    Captain = ("캡틴", JobType.DexPirate, JobGroup.Adventurer)
    CannonShooter = ("캐논슈터", JobType.Pirate, JobGroup.Adventurer)

    # 시그너스 기사단
    Mikhail = ("미하일", JobType.Warrior, JobGroup.CygnusKnights)
    SoulMaster = ("소울마스터", JobType.Warrior, JobGroup.CygnusKnights)
    FlameWizard = ("플레임위자드", JobType.Magician, JobGroup.CygnusKnights)
    WindBreaker = ("윈드브레이커", JobType.Bowman, JobGroup.CygnusKnights)
    NightWalker = ("나이트워커", JobType.Thief, JobGroup.CygnusKnights)
    Striker = ("스트라이커", JobType.Pirate, JobGroup.CygnusKnights)

    # 레지스탕스
    BattleMage = ("배틀메이지", JobType.Magician, JobGroup.Resistance)
    WildHunter = ("와일드헌터", JobType.Bowman, JobGroup.Resistance)
    Mechanic = ("메카닉", JobType.DexPirate, JobGroup.Resistance)
    Blaster = ("블래스터", JobType.Warrior, JobGroup.Resistance)
    Xenon = ("제논", JobType.Xenon, JobGroup.Resistance)

    # 데몬
    DemonSlayer = ("데몬슬레이어", JobType.Warrior, JobGroup.Demon)
    DemonAvenger = ("데몬어벤져", JobType.DemonAvenger, JobGroup.Demon)

    # 영웅
    Aran = ("아란", JobType.Warrior, JobGroup.Heros)
    Mercedes = ("메르세데스", JobType.Bowman, JobGroup.Heros)
    Evan = ("에반", JobType.Magician, JobGroup.Heros)
    Luminous = ("루미너스", JobType.Magician, JobGroup.Heros)
    Phantom = ("팬텀", JobType.Thief, JobGroup.Heros)
    Eunwol = ("은월", JobType.Pirate, JobGroup.Heros)
    
    # 노바
    Kaiser = ("카이저", JobType.Warrior, JobGroup.Nova)
    AngelicBuster = ("엔젤릭버스터", JobType.DexPirate, JobGroup.Nova)
    Cadena = ("카데나", JobType.MeleeTheif, JobGroup.Nova)
    Kain = ("카인", JobType.Bowman, JobGroup.Nova)

    # 레프
    Illium = ("일리움", JobType.Magician, JobGroup.Flora)
    Ark = ("아크", JobType.Pirate, JobGroup.Flora)
    Adele = ("아델", JobType.Warrior, JobGroup.Flora)
    Kali = ("칼리", JobType.Thief, JobGroup.Flora)


    # 아니마
    Hoyoung = ("호영", JobType.Thief, JobGroup.Anima)
    Lara = ("라라", JobType.Magician, JobGroup.Anima)

    # 초월자
    Zero = ("제로", JobType.Warrior, JobGroup.Overlord)

    # 프렌즈
    Kinesis = ("키네시스", JobType.Magician, JobGroup.Friends)

    # 메엠
    MapleM = ("메이플M", None, None)


class JobConstant(Enum):
    ArchmageFP = 1.2
    ArchmageTC = 1.2
    Bishop = 1.2
    FlameWizard = 1.2
    Xenon = 0.875


def GetMainStatList(jobtype:JobType):
    return [e for e in jobtype.value[JobTypeInfo.MainStat.value]]

def GetSubStatList(jobtype:JobType):
    return [e for e in jobtype.value[JobTypeInfo.SubStat.value]]
