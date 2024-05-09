import mysql.connector
connexion=mysql.connector.connect(host="localhost",user="root",passwd="",database="Users")
cursor=connexion.cursor()
query="SELECT * FROM `UserData` "
cursor.execute(query)
result=cursor.fetchall()
print(result[0][9])