from LIS.LIS import LIS
db = LIS()
res = db.execQuery('use capstone_db')
res = db.execQuery('show tables')
db.disconnect()
print(res)