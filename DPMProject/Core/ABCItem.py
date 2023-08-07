from Core.SpecElements import SpecVector, CoreStat
from Core.Job import JobType
from Core.Server import GameServer

from abc import ABC, abstractmethod
from enum import Enum
    

class ItemEnchantType(Enum):
    """아이템 강화 구성 요소 나열

    Args:
        Enum (bool):\n
            Upgrade: 주문서 작\n
            BonusOption: 추가 옵션\n
            StarForce: 스타포스\n
            PotentialAbility: 윗잠\n
            AdditionalAbility: 에디셔널 잠재\n
            SoulWeapon: 소울
    """

    Upgrade = 0                     # 주문서 작
    BonusOption = 1                 # 추옵  
    StarForce = 2                   # 스타포스
    PotentialAbility = 3            # 잠재능력
    AdditionalPotentialAbility = 4  # 에디셔널 잠재능력
    SoulWeapon = 5                  # 소울

class ItemType(Enum):
    """아이템의 분류

    Args:
        Enum (int):\n
        Weapon: 무기류\n
        Armor: 방어구\n
        Accessory: 장신구\n
        Symbol: 심볼\n
        PetItem: 펫 장비\n
        CharacterTitle: 칭호
    """    
    Armor = 0 
    Weapon = 1
    Accessory = 2
    Symbol = 3
    PetItem = 4
    CharacterTitle = 5
    CashCody = 6

class ItemInfo(Enum):
    """ItemParts에서 각 항목이 나타내는 정보 나열
    """
    ItemName = 0
    ItemGroup = 1
    ItemUpgradeType = 2

class ItemParts(Enum):
    """착용 가능한 아이템의 유형을 묘사

    Args:
        Enum (tuple): ("부위 이름", 아이템 유형:(방어구, 장신구, 무기), [아이템 업그레이드 요소])\n
        Ring: 반지 아이템을 나타냅니다.\n
        Pocket: 포켓 아이템을 나타냅니다.\n
        Pendant: 팬던트 아이템을 나타냅니다.\n
        Weapon: 무기 아이템을 나타냅니다.\n
        Belt: 벨트 아이템을 나타냅니다.\n
        Cap: 모자 아이템을 나타냅니다.\n
        ForeHead: 이마 아이템을 나타냅니다.\n
        EyeAccessory: 눈장식 아이템을 나타냅니다.\n
        Clothes: 옷 아이템을 나타냅니다.\n
        Pants: 바지 아이템을 나타냅니다.\n
        Shoes: 신발 아이템을 나타냅니다.\n
        EarAccessory: 귀 장식 아이템을 나타냅니다.\n
        Shoulder: 어깨 장식 아이템을 나타냅니다.\n
        Gloves: 장갑 아이템을 나타냅니다.\n
        Emblem: 엠블렘 아이템을 나타냅니다.\n
        Badge: 배지 아이템을 나타냅니다.\n
        Medal: 메달 아이템을 나타냅니다.\n
        SubWeapon: 보조 무기 아이템을 나타냅니다.\n
        Cape: 망토 아이템을 나타냅니다.\n
        Heart: 하트 아이템을 나타냅니다.\n
        Symbol: 심볼 아이템을 나타냅니다.\n
        PetAccessory: 펫 악세사리 아이템을 나타냅니다.\n
        CharacterTitle: 캐릭터 칭호 아이템을 나타냅니다.\n
        Shield: 방패 아이템을 나타냅니다.\n
        Blade: 블레이드 아이템을 나타냅니다.\n
        CashWeapon: 캐시 무기\n
        CashArmor: 캐시 방어구\n
    """    
    Ring = (
        "Ring",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )
    
    Pocket = (
        "Pocket",
        ItemType.Accessory,
        [ItemEnchantType.BonusOption]
    )
    
    Pendant = (
        "Pendant",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )
    
    Weapon = (
        "Weapon",
        ItemType.Weapon,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility, ItemEnchantType.SoulWeapon]
    )
    
    Belt = (
        "Belt",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )
    
    Cap = (
        "Cap",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    ForeHead = (
        "ForeHead",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    EyeAccessory = (
        "EyeAccessory",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Clothes = (
        "Clothes",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Pants = (
        "Pants",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Shoes = (
        "Shoes",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    EarAccessory = (
        "EarAccessory",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Shoulder = (
        "Shoulder",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Gloves = (
        "Gloves",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Emblem = (
        "Emblem",
        ItemType.Weapon,
        [ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Badge = (
        "Badge",
        ItemType.Accessory,
        []
    )

    Medal = (
        "Medal",
        ItemType.Accessory,
        []
    )

    SubWeapon = (
        "SubWeapon",
        ItemType.Weapon,
        [ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Cape = (
        "Cape",
        ItemType.Armor,
        [ItemEnchantType.Upgrade, ItemEnchantType.BonusOption, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Heart = (
        "Heart",
        ItemType.Accessory,
        [ItemEnchantType.Upgrade, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    Symbol = (
        "Symbol",
        ItemType.Symbol,
        []
    )

    PetAccessory = (
        "PetAccessory",
        ItemType.PetItem,
        [ItemEnchantType.Upgrade]
    )

    CharacterTitle = (
        "CharacterTitle",
        ItemType.CharacterTitle,
        []
    )

    # 마법사, 전사, 도적
    Shield = (
        "Shield",
        ItemType.Weapon,
        [ItemEnchantType.Upgrade, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )

    # 듀얼 블레이드 전용
    Blade = (
        "Blade",
        ItemType.Weapon,
        [ItemEnchantType.Upgrade, ItemEnchantType.StarForce, ItemEnchantType.PotentialAbility, ItemEnchantType.AdditionalPotentialAbility]
    )
    CashWeapon = (
        "CashWeapon",
        ItemType.CashCody,
        []
    )

    CashArmor = (
        "CashArmor",
        ItemType.CashCody,
        []
    )

class ABCItem(ABC):
    """아이템 추상 클래스

    Args:
        ABC (_type_): _description_\n
        ItemName: 아이템 이름\n
        RequiredLevel: 착용 레벨\n
        RequiredJobType: 착용 직업\n
        ItemBasicStat: 아이템 기본 능력치\n
        ItemPart: 장비 분류
        ServerOption: 서버(본섭/리부트)
    Raises:
        TypeError: 입력으로 인스턴스를 받지 못한 경우\n
        ValueError: 레벨 범위를 초과한 경우
    """

    ItemName: str
    RequiredLevel: int
    RequiredJobType: list[JobType]
    ItemBasicStat: SpecVector
    ItemPart: ItemParts
    ServerOption: GameServer
    

    def __init__(
            self,
            itemName: str,
            requiredLevel: int,
            requiredJobType: list[JobType],
            itemBasicStat: SpecVector,
            itemPart: ItemParts,
            server = GameServer.NormalServer
    ):
        # 아이템의 이름
        if not isinstance(itemName, str):
            raise TypeError("인스턴스가 아님")
        self.ItemName = itemName

        #아이템 착용 레벨
        if not isinstance(requiredLevel, int):
            raise TypeError("인스턴스가 아님")

        if (requiredLevel < 0) or (requiredLevel > 300):
            raise ValueError("레벨 범위는 1~300")        

        self.RequiredLevel = requiredLevel

        # 착용 직업 제한
        if not isinstance(requiredJobType, list) and requiredJobType is not None:
            raise TypeError("인스턴스가 아님")  
        
        for job in requiredJobType:
            if job not in [JobType.Warrior,
                                    JobType.Bowman,
                                    JobType.Magician,
                                    JobType.Thief,
                                    JobType.Pirate]:
                raise ValueError("장비 아이템 요구 직업조건은 전사, 궁수, 법사, 도적, 해적으로 한정함")
          
        self.RequiredJobType = requiredJobType

        # 아이템 기본 스텟
        if not isinstance(itemBasicStat, SpecVector):
            raise TypeError("인스턴스가 아님")  
        self.ItemBasicStat = itemBasicStat
        
        # 아이템 착용 부위
        if not isinstance(itemPart, ItemParts):
            raise TypeError("인스턴스가 아님")  
        self.ItemPart = itemPart

        if not isinstance(server, GameServer) and server is not None:
            raise TypeError("인스턴스가 아님")  
        self.ServerOption = server


    @abstractmethod
    def TotalSpec(self) -> tuple[SpecVector, int]:
        pass
