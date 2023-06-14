from Item.ItemGroup import LunarPetit, LunarDream
from Core.Enchant.Scroll import UpgradeScrolls
from enum import Enum

class PetAccessoryUpgradeChance(Enum):
    Dream = 9
    Petit = 8




lunarPetitAcc1 = LunarPetit([UpgradeScrolls().Accessory.PremiumSPELL for _ in range(0, PetAccessoryUpgradeChance.Petit.value)])

lunarPetitAcc2 = LunarPetit([UpgradeScrolls().Accessory.PremiumSPELL for _ in range(0, PetAccessoryUpgradeChance.Petit.value)])

lunarPetitAcc3 = LunarPetit([UpgradeScrolls().Accessory.PremiumSPELL for _ in range(0, PetAccessoryUpgradeChance.Petit.value)])

lunarDreamAcc1 = LunarDream([UpgradeScrolls().Accessory.SPELL for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])

lunarDreamAcc2 = LunarDream([UpgradeScrolls().Accessory.SPELL for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])

lunarDreamAcc3 = LunarDream([UpgradeScrolls().Accessory.SPELL for _ in range(0, PetAccessoryUpgradeChance.Dream.value)])

