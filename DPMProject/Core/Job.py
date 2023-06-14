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
    Worrior = ((CoreStat.STAT_STR,),(CoreStat.STAT_DEX,))
    # 데벤
    DemonAvenger = ((CoreStat.STAT_HP,),)
    # 보우마스터, 신궁, 패스파인더, 윈드브레이커, 와일드헌터, 메르세데스, 카인
    Bowman = ((CoreStat.STAT_DEX,),(CoreStat.STAT_STR,))
    # 불독, 썬콜, 비숍, 플위, 배틀메이지, 에반, 루미너스, 일리움, 라라, 키네시스
    Magician = ((CoreStat.STAT_INT,),(CoreStat.STAT_LUK,))
    # 나이트로드, 나이트워커, 팬텀, 호영, 칼리
    Theif = ((CoreStat.STAT_LUK,),(CoreStat.STAT_DEX,))
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

class JobName(Enum):
    """직업 상세 정보

    Args:
        enum (이름, 직업 계열, 직업군, (주스텟1, 주스텟 2, ...), (부스텟1, 부스텟2, ...), (무기1, 무기2, ...), (보조 무기1, 보조 무기2, ...)): 직업 고유 정보
    """    
    # 정보 수정이 조금 필요할듯. JobType의 변화로 인한 
    # 모험가 전사
    Hero = ("히어로", JobType.Worrior, JobGroup.Adventurer, (CoreStat.STAT_STR), (CoreStat.STAT_DEX),(),())
    Paladin = ("팔라딘", JobType.Worrior, JobGroup.Adventurer, (CoreStat.STAT_STR), (CoreStat.STAT_DEX),(),())
    DarkNight = ("다크나이트", JobType.Worrior, JobGroup.Adventurer, (CoreStat.STAT_STR), (CoreStat.STAT_DEX),(),())

    # 모험가 궁수
    BowMaster = ("보우마스터", JobType.Bowman, JobGroup.Adventurer, (CoreStat.STAT_DEX), (CoreStat.STAT_STR),(),())
    MarsMan = ("신궁", JobType.Bowman, JobGroup.Adventurer, (CoreStat.STAT_DEX), (CoreStat.STAT_STR),(),())
    PathFinder = ("패스파인더", JobType.Bowman, JobGroup.Adventurer, (CoreStat.STAT_DEX), (CoreStat.STAT_STR),(),())

    # 모험가 법사
    ArchmageFP = ("아크메이지(불,독)", JobType.Magician, JobGroup.Adventurer, (CoreStat.STAT_INT), (CoreStat.STAT_LUK),(),())
    ArchmageTC = ("아크메이지(얼음,번개)", JobType.Magician, JobGroup.Adventurer, (CoreStat.STAT_INT), (CoreStat.STAT_LUK),(),())
    Bishop = ("비숍", JobType.Magician, JobGroup.Adventurer, (CoreStat.STAT_INT), (CoreStat.STAT_LUK),(),())

    # 모험가 도적
    NightLord = ("나이트로드", JobType.Theif, JobGroup.Adventurer, (CoreStat.STAT_LUK), (CoreStat.STAT_DEX),(),())
    Shadower = ("섀도어", JobType.Theif, JobGroup.Adventurer, (CoreStat.STAT_LUK), (CoreStat.STAT_DEX, CoreStat.STAT_STR),(),())
    DualBlade = ("듀얼 블레이드", JobType.Theif, JobGroup.Adventurer, (CoreStat.STAT_LUK), (CoreStat.STAT_DEX, CoreStat.STAT_STR),(),())
    
    # 모험가 해적

    # 시그너스 기사단

    # 레지스탕스

    # 데몬

    # 영웅
    Mercedes = ("메르세데스", JobType.Bowman, JobGroup.Heros, (CoreStat.STAT_DEX), (CoreStat.STAT_STR),(),())

    # 노바

    # 레프

    # 아니마

    # 초월자

    # 프렌즈
