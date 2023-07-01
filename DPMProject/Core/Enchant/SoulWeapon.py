from Core.ABCItem import ABCItem, ItemParts
from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat
from enum import Enum
from Core.Server import GameServer
class SoulEnchantOption(Enum):
    """소울 웨폰 옵션 종류 열거

    Args:
        Enum (int): 
        AttackSpell         :공마 3퍼\n
        CriticalPercentage  :크확 12퍼\n
        BossDamage          :보공 7퍼\n
        IgnoreGuard         :방무 7퍼\n
        Ephenia             :에피네아 소울, HP 180 증가.

    """    
    AttackPercentage = (CoreStat.ATTACK_PHYSICAL_PERCENTAGE, 3)
    SpellPercentage = (CoreStat.ATTACK_SPELL_PERCENTAGE, 3)
    CriticalPercentage = (CoreStat.CRITICAL_PERCENTAGE, 12)
    BossDamage = (CoreStat.DAMAGE_PERCENTAGE_BOSS, 7)
    IgnoreGuard = (CoreStat.IGNORE_GUARD_PERCENTAGE, 7)
    Ephenia = (CoreStat.STAT_HP, 180)
    souloption = 0
    soulvalue = 1

class SoulWeapon(ABCItem):
    """소울 웨폰 기능 묘사, 소울 액티브 스킬은 묘사하지 않음.

    Args:
        ABCItem (_type_): 
        
    Raises:
        TypeError: 소울의 옵션이 누락될 경우
    """    
    EnchantOption: SoulEnchantOption
    SoulWeaponOption: SpecVector

    def __init__(
            self, 
            itemName: str,
            requiredLevel: int,
            requiredJobType: list[JobType],
            itemBasicStat: SpecVector,
            itemPart: ItemParts,
            enchant: SoulEnchantOption,
            server = GameServer.NormalServer
            ):
        ABCItem.__init__(
            self = self,
            itemName=itemName,
            requiredJobType=requiredJobType,
            requiredLevel=requiredLevel,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            server=server
        )

        if not isinstance(enchant, SoulEnchantOption) and enchant is not None:
            raise TypeError("소울 옵션 누락")
        self.EnchantOption = enchant

        if not self.ItemPart == ItemParts.Weapon:
            raise AttributeError("소울 웨폰은 무기에만 적용됨")
        
        # 소울 웨폰 게이지에 의한 공마 20 획득 - 캐릭터의 스펙에 합산하기: 아이템 강화 로직 검증과정에서 직관성 떨어짐
        SoulWeaponATK_SPELLOption = SpecVector()
        #SoulWeaponATK_SPELLOption[CoreStat.ATTACK_PHYSICAL] = 20
        #SoulWeaponATK_SPELLOption[CoreStat.ATTACK_SPELL] = 20

        # 소울 옵션에 해당하는 옵션을 부여함
        successflag = False        
        for stat in CoreStat:
            if stat == self.EnchantOption.value[SoulEnchantOption.souloption.value]:
                SoulWeaponATK_SPELLOption[stat] = self.EnchantOption.value[SoulEnchantOption.soulvalue.value]
                successflag = True
                break

        if successflag == False:
            raise IndexError("스펙 벡터에 값이 할당되지 않았음")
        
        self.SoulWeaponOption = SoulWeaponATK_SPELLOption
    
    def TotalSpec(self) -> tuple[SpecVector, int]:
        result =SpecVector()
        result = self.SoulWeaponOption
        return result, 0
        
