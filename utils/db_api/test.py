
from ...loader import db as d
sql = """
SELECT * FROM Smatrtphone WHERE user_id = ?
"""


result = d.execute(sql, parameters=(1712716612,), fetchall=True)

print(result)