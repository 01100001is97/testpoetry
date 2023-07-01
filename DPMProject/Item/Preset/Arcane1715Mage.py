from Item.Accessory.Ring import MeisterRing, GuardianAngelRing, EventRing, RingUpgradeChance, SeedRing
from Item.Accessory.Pendant import DominatorPendant, DayBreakPendant, PendantUpgradeChance
from Item.Accessory.Belt import EnragedZaqqumBelt, BeltUpgradeChance
from Item.Accessory.ForeHead import TwilightMark, ForeHeadUpgradeChance
from Item.Accessory.EyeAccessory import PapulatusMark, EyeAccessoryUpgradeChance
from Item.Accessory.EarAccessory import EstellaEarRings, MeisterEarRings, EarRingUpgradeChance
from Item.Accessory.Shoulder import ArcaneShadeMageShoulder, ShoulderUpgradeChance
from Item.Accessory.Pocket import PinkHolyCup
from Item.Accessory.Heart import FairyHeart, HeartUpgradeChance
from Item.Armor.Cap import HighnessDunwitchHat, CapUpgradeChance
from Item.Armor.Clothes import EagleEyeDunwitchRobe, ClothUpgradeChance
from Item.Armor.Pants import TricksterDunwitchPants, PantsUpgradeChance
from Item.Armor.Shoes import ArcaneShadeMageShoes, ShoesUpgradeChance
from Item.Armor.Gloves import ArcaneShadeMageGloves, GlovesUpgradeChance
from Item.Armor.Cape import ArcaneShadeMageCape, CapeUpgradeChance
from Item.Pet.LunarCristal import LunarDream, LunarPetit, PetAccessoryUpgradeChance
from Item.Weapons.Weapon import ArcaneShadeStaff, WeaponUpgradeChance
from Item.Weapons.SubWeapon import WhiteGoldBook
from Item.Weapons.Emblem import GoldMapleLeafEmblem
from Core.Enchant.Potential import PotentialOptionSlot, PotentialEnum, PotentialGrade
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Enchant.SoulWeapon import SoulEnchantOption
from Core.SpecElements import SpecVector
from Core.ABCItem import ItemParts
from Core.Enchant.BonusOption import BonusOptionSlot, BonusOptionGrade, BonusOptionEnum
from Item.ItemSlot import ItemSlot
from Item.Preset.Commons import VentusBadge, SevendaysMedal, ArcaneSymbols_int, AuthSymbols_int, Blacklabels, blacklabel_weapon, KOR


STAR_LEVEL = 17

# 공통 스텟류 잠재능력 : 주스텟 유니크 1줄, 에픽 1줄
PotentialInt9 = PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Unique, isadditional=False)
potentialInt6 = PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Epic, isadditional=False)
PotentialCrit8 = PotentialOptionSlot(option=PotentialEnum.CriticalDamage, grade=PotentialGrade.Legendary, isadditional=False)
POTENTIAL_OPTION_MAGICIAN = [potentialInt6, PotentialInt9]
POTENTIAL_OPTION_MAGICIAN_GLOVES = [PotentialCrit8, PotentialInt9]

# 공통 스텟류 에디 잠재: 에픽 주스텟 1줄 + 레어 공/마 1줄
APotentialInt_4 = PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Epic, isadditional=True)
APotentialSpell = PotentialOptionSlot(option=PotentialEnum.Spell, grade=PotentialGrade.Rare, isadditional=True)
APOTENTIAL_OPTION_MAGICIAN = [APotentialInt_4, APotentialSpell]

# 공통 잠재능력 수준: 올스텟 3추옵, 단일, 이중스텟(주, 부) 2추옵
BonusSlot = BonusOptionSlot()
BonusSlot.update({BonusOptionEnum.AllStatPercentage: BonusOptionGrade.third})
BonusSlot.update({BonusOptionEnum.IntSingleStat: BonusOptionGrade.second})
BonusSlot.update({BonusOptionEnum.IntLukDoubleStat: BonusOptionGrade.second})

# 공통 주문서 작 악세서리: 악세서리 스크롤, 방어구: 30퍼작
accessoryScroll = UpgradeScrolls().Accessory.SPELL

ItemPreset_1715_int = ItemSlot()

## 장신구 인스턴스 ##
# 마이스터링 17성 15퍼 에디 2줄
MeisterRing_1715_int = MeisterRing(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    upgrade_history=[accessoryScroll for _ in range(0, RingUpgradeChance.Meister.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Ring, item=MeisterRing_1715_int)

# 가엔링 17성 15퍼 에디 2줄
GuardianAngelRing_1715_int = GuardianAngelRing(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    upgrade_history=[accessoryScroll for _ in range(0, RingUpgradeChance.Guardian.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Ring, item=GuardianAngelRing_1715_int)

# 이벤트링 17성 15퍼 에디 2줄
EventRing_15_int = EventRing(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Ring, item=EventRing_15_int)

# 시드링은 Simulate.py에서 설정함.
ItemPreset_1715_int.AddItem(part=ItemParts.Ring, item=SeedRing())

# 성배는 2추 단일스텟, 2추 이중스텟, 2추 올스텟
HolyCup_int = PinkHolyCup(optionslot=BonusSlot)
ItemPreset_1715_int.AddItem(part=ItemParts.Pocket, item=HolyCup_int)

# 도미네이터 펜던트 17성 15퍼 에디 2줄
Dominator_1715_int = DominatorPendant(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[UpgradeScrolls().Accessory.Dominator for _ in range(0, PendantUpgradeChance.Dominator.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Pendant, item=Dominator_1715_int)

# 데이브레이크 펜던트 17성 15퍼 에디 2줄
DayBreak_1715_int = DayBreakPendant(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, PendantUpgradeChance.Daybreak.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Pendant, item=DayBreak_1715_int)

# 분노한 자쿰의 벨트 17성 15퍼 에디 2줄
EnragedBelt_1715_int = EnragedZaqqumBelt(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, BeltUpgradeChance.Zaqqum.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Belt, item=EnragedBelt_1715_int)

# 트와일라이트 마크 17성 15퍼 에디 2줄
TwilightMark_1715_int = TwilightMark(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, ForeHeadUpgradeChance.TwilightMark.value)],  # Assuming there's a ForeHeadUpgradeChance.TwilightMark constant
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.ForeHead, item=TwilightMark_1715_int)

# 파풀라투스 마크 17성 15퍼 에디 2줄
PapulatusMark_1715_int = PapulatusMark(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, EyeAccessoryUpgradeChance.PapulatusMark.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.EyeAccessory, item=PapulatusMark_1715_int)

# 에스텔라 이어링 17성 15퍼 에디 2줄
estella_1715_int = EstellaEarRings(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    upgrade_history=[accessoryScroll for _ in range(0, EarRingUpgradeChance.Estella.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.EarAccessory, item=estella_1715_int)

# 아케인셰이드 메이지숄더 17성 15퍼 에디 2줄 
ArcaneShadeMageShoulder_1715 = ArcaneShadeMageShoulder(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Accessory.SPELL for _ in range(0, ShoulderUpgradeChance.Arcane.value)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN,
)
ItemPreset_1715_int.AddItem(part=ItemParts.Shoulder, item=ArcaneShadeMageShoulder_1715)

# 뱃지, 훈장, 칭호
ItemPreset_1715_int.AddItem(part=ItemParts.Badge, item=VentusBadge)
ItemPreset_1715_int.AddItem(part=ItemParts.Medal, item=SevendaysMedal)

# 페어리 하트
fairy_int = FairyHeart(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    upgrade_history=[UpgradeScrolls().Heart.PieceSPELL30 for _ in range(0, HeartUpgradeChance.Fairy.value)],
    starforce=STAR_LEVEL,
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Heart, item=fairy_int)

## 방어구 인스턴스 ##
# 모자
dunwitchhat_1715 = HighnessDunwitchHat(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceINT30 for _ in range(0, CapUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Cap, item=dunwitchhat_1715)

# 상의
dunwitchrobe_1715 = EagleEyeDunwitchRobe(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceINT30 for _ in range(0, ClothUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Clothes, item=dunwitchrobe_1715)

# 하의
dunwitchpants_1715 = TricksterDunwitchPants(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceINT30 for _ in range(0, PantsUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Pants, item= dunwitchpants_1715)

# 신발
arcanemageshoes = ArcaneShadeMageShoes(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceINT30 for _ in range(0, ShoesUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Shoes, item=arcanemageshoes)

# 장갑
arcanemagegloves = ArcaneShadeMageGloves(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN_GLOVES,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceSPELL30 for _ in range(0, GlovesUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Gloves, item=arcanemagegloves)

# 망토
arcanemagecape = ArcaneShadeMageCape(
    potentialOptionList=POTENTIAL_OPTION_MAGICIAN,
    optionslot=BonusSlot,
    starforce=STAR_LEVEL,
    upgrade_history=[UpgradeScrolls().Armor.PieceINT30 for _ in range(0, CapeUpgradeChance)],
    additionalPotentialOptionList=APOTENTIAL_OPTION_MAGICIAN
)
ItemPreset_1715_int.AddItem(part=ItemParts.Cape, item=arcanemagecape)

## 무기류 인스턴스 ##
# 잠재능력 보마마
Poten_boss_legend = PotentialOptionSlot(option=PotentialEnum.BossDamage, grade=PotentialGrade.Legendary, isadditional=False)
Poten_Splpercent_unique1 = PotentialOptionSlot(option=PotentialEnum.SpellPercentage, grade=PotentialGrade.Unique, isadditional=False)
Poten_Splpercent_unique2 = PotentialOptionSlot(option=PotentialEnum.SpellPercentage, grade=PotentialGrade.Unique, isadditional=False)
weaponPotential_spell = []
#[Poten_boss_legend, Poten_Splpercent_unique1, Poten_Splpercent_unique2]

# 잠재능력 보보마
Poten_boss_unique = PotentialOptionSlot(option=PotentialEnum.BossDamage, grade=PotentialGrade.Unique, isadditional=False)
subweaponPoten_spell = []
#[Poten_boss_legend, Poten_boss_unique, Poten_Splpercent_unique1]

# 잠재능력 방마마
poten_ignore_legend = PotentialOptionSlot(option=PotentialEnum.IgnoreGuard, grade=PotentialGrade.Legendary, isadditional=False)
emblemPoten_Spell = []
#[poten_ignore_legend, Poten_Splpercent_unique1, Poten_Splpercent_unique2]

# 에디잠재능력 마마
APoten_Splpercent_unique = PotentialOptionSlot(option=PotentialEnum.SpellPercentage, grade=PotentialGrade.Unique, isadditional=True)
APoten_Splpercent_epic = PotentialOptionSlot(option=PotentialEnum.SpellPercentage, grade=PotentialGrade.Epic, isadditional=True)
weaponAPotential_spell = [APoten_Splpercent_unique, APoten_Splpercent_epic]

# 무기 추가옵션 마력2추 보공12 데미지 6
WeaponBonusSlot_Spell = BonusOptionSlot()
WeaponBonusSlot_Spell.update({BonusOptionEnum.AttackSpell: BonusOptionGrade.second})
WeaponBonusSlot_Spell.update({BonusOptionEnum.BossDamage: BonusOptionGrade.second})
WeaponBonusSlot_Spell.update({BonusOptionEnum.Damage: BonusOptionGrade.second})

# 18성 보마마 레유 스태프
arcanestaff = ArcaneShadeStaff(
    potentialOptionList= weaponPotential_spell,
    optionSlot=WeaponBonusSlot_Spell,
    upgrade_history=[UpgradeScrolls().Weapon.PieceINT15 for _ in range(0,WeaponUpgradeChance.Arcane.value)],
    starforce=STAR_LEVEL + 1,
    enchant= SoulEnchantOption.SpellPercentage,
    additionalPotentialOptionList= weaponAPotential_spell
)
ItemPreset_1715_int.AddItem(part=ItemParts.Weapon, item=arcanestaff)

# 보조무기 보보마 레유
# 백금의 서
whitegoldbook = WhiteGoldBook(
    potential=subweaponPoten_spell, 
    addPotential=weaponAPotential_spell
)
ItemPreset_1715_int.AddItem(part=ItemParts.SubWeapon, item=whitegoldbook)

# 엠블렘 방마마 레에
mapleleafemblem_spell = GoldMapleLeafEmblem(
    potential= emblemPoten_Spell,
    addPotential=weaponAPotential_spell
)
ItemPreset_1715_int.AddItem(part=ItemParts.Emblem, item=mapleleafemblem_spell)


# 캐시 아이템
ItemPreset_1715_int.AddItem(part=ItemParts.CashWeapon, item=blacklabel_weapon)
for item in Blacklabels:
    ItemPreset_1715_int.AddItem(part=ItemParts.CashArmor, item=item)

## 펫 장비 인스턴스 ##

lunarPetitAcc1 = LunarPetit([UpgradeScrolls().Accessory.PremiumSPELL for _ in range(0, PetAccessoryUpgradeChance.Petit.value)])
ItemPreset_1715_int.AddItem(part=ItemParts.PetAccessory, item=lunarPetitAcc1)

lunarDreamAcc1 = LunarDream([UpgradeScrolls().Accessory.SPELL for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])
ItemPreset_1715_int.AddItem(part=ItemParts.PetAccessory, item=lunarDreamAcc1)

lunarDreamAcc2 = LunarDream([UpgradeScrolls().Accessory.SPELL for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])
ItemPreset_1715_int.AddItem(part=ItemParts.PetAccessory, item=lunarDreamAcc2)

## 심볼 인스턴스 ##
for symbol in ArcaneSymbols_int + AuthSymbols_int:
    ItemPreset_1715_int.AddItem(part=ItemParts.Symbol, item=symbol)
# 칭호
ItemPreset_1715_int.AddItem(part=ItemParts.CharacterTitle, item=KOR)


if "__main__" == __name__:
    # 총정리
    TotalSpec = SpecVector()
    cooldown = 0
    for parts, itemlist in ItemPreset_1715_int.items():
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
    print(len(ItemPreset_1715_int))
