from Core.ABCItem import ItemParts, ABCItem
from typing import Dict, List

class ItemSlot(Dict[ItemParts, List[ABCItem]]):
    def __init__(self):
        super().__init__()

    def AddItem(self, part: ItemParts, item: ABCItem):
        if part in self:
            self[part].append(item)
        else:
            self[part] = [item]
    """
    def RemoveItem(self, part: ItemParts, item: ABCItem):
        if part in self and item in self[part]:
            self[part].remove(item)
            if not self[part]:  # If the list becomes empty after removing the item, delete the key as well
                del self[part]
        """
    
    def GetItem(self, part: ItemParts) -> List[ABCItem]:
        return self.get(part, [])
