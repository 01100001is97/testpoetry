from Item.ItemGroup import AuthenticSymbol
from Core.Job import JobType

authsymbollist = []

CerniumSymbol_int_11 = AuthenticSymbol([JobType.Magician], symbolLevel=11)
authsymbollist.append(CerniumSymbol_int_11)

ArcsSymbol_int_7 = AuthenticSymbol([JobType.Magician], symbolLevel=7)
authsymbollist.append(ArcsSymbol_int_7)

AuthenticSymbolPreset = authsymbollist
"""
for symbol in authsymbollist:
    stat, _ = symbol.TotalSpec()
    stat.Show()
    """