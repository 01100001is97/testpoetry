from Item.Accessory.Ring import MeisterRing, GuardianAngelRing, EventRing, RingUpgradeChance, SeedRing
from Item.Accessory.Pendant import DominatorPendant, DayBreakPendant, PendantUpgradeChance
from Item.Accessory.Belt import EnragedZaqqumBelt, BeltUpgradeChance
from Item.Accessory.ForeHead import TwilightMark, ForeHeadUpgradeChance
from Item.Accessory.EyeAccessory import PapulatusMark, EyeAccessoryUpgradeChance
from Item.Accessory.EarAccessory import EstellaEarRings, MeisterEarRings, EarRingUpgradeChance
from Item.Accessory.Shoulder import ArcaneShadeThiefShoulder, ShoulderUpgradeChance
from Item.Accessory.Pocket import PinkHolyCup
from Item.Accessory.Heart import FairyHeart, HeartUpgradeChance
from Item.Armor.Cap import HighnessAssassinHood, CapUpgradeChance
from Item.Armor.Clothes import EagleEyeAssassinShirt, ClothUpgradeChance
from Item.Armor.Pants import TricksterAssassinPants, PantsUpgradeChance
from Item.Armor.Shoes import ArcaneShadeThiefShoes, ShoesUpgradeChance
from Item.Armor.Cape import ArcaneShadeThiefCape, CapeUpgradeChance
from Item.Armor.Gloves import ArcaneShadeThiefGloves, GlovesUpgradeChance

from Item.Pet.LunarCristal import LunarDream, LunarPetit, PetAccessoryUpgradeChance
from Item.Weapons.Weapon import ArcaneShadeBuchae, WeaponUpgradeChance
from Item.Weapons.SubWeapon import Sunchu
from Item.Weapons.Emblem import GoldMapleLeafEmblem
from Core.Enchant.Potential import PotentialOptionSlot, PotentialEnum, PotentialGrade
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Enchant.SoulWeapon import SoulEnchantOption
from Core.ABCItem import ItemParts
from Core.Enchant.BonusOption import BonusOptionSlot, BonusOptionGrade, BonusOptionEnum
from Core.SpecElements import SpecVector
from Item.ItemSlot import ItemSlot
from Item.Preset.Commons import VentusBadge, SevendaysMedal, ArcaneSymbols_luk, AuthSymbols_luk, Blacklabels, blacklabel_weapon, KOR

STAR_LEVEL = 17

# 공통 스텟류 잠재능력 : 주스텟 유니크 1줄, 에픽 1줄
PotentialLuk9 = PotentialOptionSlot(option=PotentialEnum.LukPercentage, grade=PotentialGrade.Unique, isadditional=False)
potentialLuk6 = PotentialOptionSlot(option=PotentialEnum.LukPercentage, grade=PotentialGrade.Epic, isadditional=False)
PotentialCrit8 = PotentialOptionSlot(option=PotentialEnum.CriticalDamage, grade=PotentialGrade.Legendary, isadditional=False)
POTENTIAL_OPTION_THIEF = [potentialLuk6, PotentialLuk9]
POTENTIAL_OPTION_THIEF_GLOVES = [PotentialCrit8, PotentialLuk9]

# 공통 스텟류 에디 잠재: 에픽 주스텟 1줄 + 레어 공/마 1줄
APotentialLuk_4 = PotentialOptionSlot(option=PotentialEnum.LukPercentage, grade=PotentialGrade.Epic, isadditional=True)
APotentialAttack = PotentialOptionSlot(option=PotentialEnum.Attack, grade=PotentialGrade.Rare, isadditional=True)
APOTENTIAL_OPTION_THIEF = [APotentialLuk_4, APotentialAttack]

# 공통 잠재능력 수준: 올스텟 3추옵, 단일, 이중스텟(주, 부) 2추옵
BonusSlot = BonusOptionSlot()
BonusSlot.update({BonusOptionEnum.AllStatPercentage: BonusOptionGrade.third})
BonusSlot.update({BonusOptionEnum.LukSingleStat: BonusOptionGrade.second})
BonusSlot.update({BonusOptionEnum.DexLukDoubleStat: BonusOptionGrade.second})

# 공통 주문서 작 악세서리: 악세서리 스크롤, 방어구: 30퍼작
accessoryScroll = UpgradeScrolls().Accessory.ATK

ItemPreset_1715_luk = ItemSlot()


# 단, 각각의 장비를 변경하려면 해당 장비 클래스와 인스턴스 생성자를 알아야 합니다. 
# 이를 알려주실 수 있나요? 아래의 예시에서는 'MeisterRing', 'GuardianAngelRing' 등의 클래스가 필요합니다. 
# 이 클래스들이 어떤 파라미터를 받는지 알려주시면 변경사항을 반영할 수 있습니다.

## 장신구 인스턴스 ##
# 마이스터링 17성 15퍼 에디 2줄
MeisterRing_1715_luk = MeisterRing(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    upgrade_history=[accessoryScroll for _ in range(0, RingUpgradeChance.Meister.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Ring, item=MeisterRing_1715_luk)

# 가엔링 17성 15퍼 에디 2줄
GuardianAngelRing_1715_luk = GuardianAngelRing(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    upgrade_history=[accessoryScroll for _ in range(0, RingUpgradeChance.Guardian.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Ring, item=GuardianAngelRing_1715_luk)

# 이벤트링 17성 15퍼 에디 2줄
EventRing_15_luk = EventRing(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Ring, item=EventRing_15_luk)

# 시드링은 Simulate.py에서 설정함.
ItemPreset_1715_luk.AddItem(part=ItemParts.Ring, item=SeedRing())

# 성배는 2추 단일스텟, 2추 이중스텟, 2추 올스텟
HolyCup_luk = PinkHolyCup(optionslot=BonusSlot)
ItemPreset_1715_luk.AddItem(part=ItemParts.Pocket, item=HolyCup_luk)

# 도미네이터 펜던트 17성 15퍼 에디 2줄
Dominator_1715_luk = DominatorPendant(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[UpgradeScrolls().Accessory.Dominator for _ in range(0, PendantUpgradeChance.Dominator.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Pendant, item=Dominator_1715_luk)

# 데이브레이크 펜던트 17성 15퍼 에디 2줄
DayBreak_1715_luk = DayBreakPendant(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, PendantUpgradeChance.Daybreak.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Pendant, item=DayBreak_1715_luk)

# 분노한 자쿰의 벨트 17성 15퍼 에디 2줄
EnragedBelt_1715_luk = EnragedZaqqumBelt(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, BeltUpgradeChance.Zaqqum.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Belt, item=EnragedBelt_1715_luk)

# 트와일라이트 마크 17성 15퍼 에디 2줄
TwilightMark_1715_luk = TwilightMark(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, ForeHeadUpgradeChance.TwilightMark.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.ForeHead, item=TwilightMark_1715_luk)

# 파풀라투스 마크 17성 15퍼 에디 2줄
PapulatusMark_1715_luk = PapulatusMark(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, EyeAccessoryUpgradeChance.PapulatusMark.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.EyeAccessory, item=PapulatusMark_1715_luk)

# 에스텔라 이어링 17성 15퍼 에디 2줄
estella_1715_luk = EstellaEarRings(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, EarRingUpgradeChance.Estella.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.EarAccessory, item=estella_1715_luk)



# 아케인셰이드 시프숄더 17성 15퍼 에디 2줄 
ArcaneShadeThiefShoulder_1715 = ArcaneShadeThiefShoulder(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Accessory.ATK for _ in range(0, ShoulderUpgradeChance.Arcane.value)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF,
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Shoulder, item=ArcaneShadeThiefShoulder_1715)

# 뱃지, 훈장, 칭호
ItemPreset_1715_luk.AddItem(part=ItemParts.Badge, item=VentusBadge)
ItemPreset_1715_luk.AddItem(part=ItemParts.Medal, item=SevendaysMedal)

# 페어리 하트
fairy_luk = FairyHeart(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    upgrade_history=[UpgradeScrolls().Heart.PieceATK30 for _ in range(0, HeartUpgradeChance.Fairy.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Heart, item=fairy_luk)

## 방어구 인스턴스 ##
# 모자
assassinehood_1715 = HighnessAssassinHood(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceLUK30 for _ in range(0, CapUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Cap, item=assassinehood_1715)

# 상의
eagleeyethiefrobe_1715 = EagleEyeAssassinShirt(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceLUK30 for _ in range(0, ClothUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Clothes, item=eagleeyethiefrobe_1715)

# 하의
tricksterthiefpants_1715 = TricksterAssassinPants(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceLUK30 for _ in range(0, PantsUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Pants, item=tricksterthiefpants_1715)

# 신발
arcanethiefshoes = ArcaneShadeThiefShoes(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceLUK30 for _ in range(0, ShoesUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Shoes, item=arcanethiefshoes)

# 장갑
arcanethiefgloves = ArcaneShadeThiefGloves(
    potentialOptionList=POTENTIAL_OPTION_THIEF_GLOVES,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceATK30 for _ in range(0, GlovesUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Gloves, item=arcanethiefgloves)

# 망토
arcanethiefcape = ArcaneShadeThiefCape(
    potentialOptionList=POTENTIAL_OPTION_THIEF,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceLUK30 for _ in range(0, CapeUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_THIEF
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Cape, item=arcanethiefcape)

## 무기류 인스턴스 ##
# 잠재능력 보마마
Poten_boss_legend = PotentialOptionSlot(option=PotentialEnum.BossDamage, grade=PotentialGrade.Legendary, isadditional=False)
Poten_Atkpercent_unique1 = PotentialOptionSlot(option=PotentialEnum.AttackPercentage, grade=PotentialGrade.Unique, isadditional=False)
Poten_Atkpercent_unique2 = PotentialOptionSlot(option=PotentialEnum.AttackPercentage, grade=PotentialGrade.Unique, isadditional=False)
weaponPotential_attack = []
#[Poten_boss_legend, Poten_Splpercent_unique1, Poten_Splpercent_unique2]

# 잠재능력 보보마
Poten_boss_unique = PotentialOptionSlot(option=PotentialEnum.BossDamage, grade=PotentialGrade.Unique, isadditional=False)
subweaponPoten_attack = []
#[Poten_boss_legend, Poten_boss_unique, Poten_Splpercent_unique1]

# 잠재능력 방마마
poten_ignore_legend = PotentialOptionSlot(option=PotentialEnum.IgnoreGuard, grade=PotentialGrade.Legendary, isadditional=False)
emblemPoten_Attack = []
#[poten_ignore_legend, Poten_Splpercent_unique1, Poten_Splpercent_unique2]

# 에디잠재능력 마마
APoten_Atkpercent_unique = PotentialOptionSlot(option=PotentialEnum.AttackPercentage, grade=PotentialGrade.Unique, isadditional=True)
APoten_Atkpercent_epic = PotentialOptionSlot(option=PotentialEnum.AttackPercentage, grade=PotentialGrade.Epic, isadditional=True)
weaponAPotential_attack = [APoten_Atkpercent_unique, APoten_Atkpercent_epic]

# 무기 추가옵션 마력2추 보공12 데미지 6
WeaponBonusSlot_Attack = BonusOptionSlot()
WeaponBonusSlot_Attack.update({BonusOptionEnum.AttackPhysical: BonusOptionGrade.second})
WeaponBonusSlot_Attack.update({BonusOptionEnum.BossDamage: BonusOptionGrade.second})
WeaponBonusSlot_Attack.update({BonusOptionEnum.Damage: BonusOptionGrade.second})


# 18성 보마마 레유 부채
arcanebochae = ArcaneShadeBuchae(
    potentialOptionList= weaponPotential_attack,
    optionSlot=WeaponBonusSlot_Attack,
    upgrade_history=[UpgradeScrolls().Weapon.PieceLUK15 for _ in range(0,WeaponUpgradeChance.Arcane.value)],
    starforce=STAR_LEVEL + 1,
    enchant= SoulEnchantOption.AttackPercentage,
    additionalPotentialOptionList= weaponAPotential_attack
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Weapon, item=arcanebochae)

whitegoldbook = Sunchu(
    potential=subweaponPoten_attack, 
    addPotential=weaponAPotential_attack
)
ItemPreset_1715_luk.AddItem(part=ItemParts.SubWeapon, item=whitegoldbook)


# 엠블렘 방마마 레에
mapleleafemblem_attack = GoldMapleLeafEmblem(
    potential= emblemPoten_Attack,
    addPotential=weaponAPotential_attack
)
ItemPreset_1715_luk.AddItem(part=ItemParts.Emblem, item=mapleleafemblem_attack)



# 캐시 아이템
ItemPreset_1715_luk.AddItem(part=ItemParts.CashWeapon, item=blacklabel_weapon)
for item in Blacklabels:
    ItemPreset_1715_luk.AddItem(part=ItemParts.CashArmor, item=item)

## 펫 장비 인스턴스 ##

lunarPetitAcc1 = LunarPetit([UpgradeScrolls().Accessory.PremiumATK for _ in range(0, PetAccessoryUpgradeChance.Petit.value)])
ItemPreset_1715_luk.AddItem(part=ItemParts.PetAccessory, item=lunarPetitAcc1)

lunarDreamAcc1 = LunarDream([UpgradeScrolls().Accessory.ATK for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])
ItemPreset_1715_luk.AddItem(part=ItemParts.PetAccessory, item=lunarDreamAcc1)

lunarDreamAcc2 = LunarDream([UpgradeScrolls().Accessory.ATK for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])
ItemPreset_1715_luk.AddItem(part=ItemParts.PetAccessory, item=lunarDreamAcc2)

## 심볼 인스턴스 ##
for symbol in ArcaneSymbols_luk + AuthSymbols_luk:
    ItemPreset_1715_luk.AddItem(part=ItemParts.Symbol, item=symbol)
# 칭호
ItemPreset_1715_luk.AddItem(part=ItemParts.CharacterTitle, item=KOR)



if "__main__" == __name__:
    # 총정리
    TotalSpec = SpecVector()
    cooldown = 0
    for parts, itemlist in ItemPreset_1715_luk.items():
        print("Parts: " + parts.name)
        for item in itemlist:
            spec, cool = item.TotalSpec()
            TotalSpec = TotalSpec + spec
            cooldown = cool
            print(item.ItemName + '\n')
            spec.Show()
            #TotalSpec.Show()

    print("--Total Spec--\n")
    TotalSpec.Arrange()
    TotalSpec.Show()
    print(len(ItemPreset_1715_luk))

