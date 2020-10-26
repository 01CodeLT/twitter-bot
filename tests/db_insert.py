import sys
from src.db import DB

rows = DB.selectAll('''SELECT * FROM followers WHERE parent_account = ? AND followed = 0;''', ('VisitLancashire',))
print(rows)