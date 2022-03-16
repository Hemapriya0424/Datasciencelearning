import requests
import pymysql
import sys
import csv
Con = pymysql.connect(host="127.0.0.1", user="root", password="", db="skillset", autocommit=True, charset='utf8')
Cursor = Con.cursor()
cur = Cursor.execute("select group_concat(skills) from UnionSkills")
rows = Cursor.fetchall()
for row in rows:
    row = list(row)
for i in row:
    row = i.split(',')
print(row)
for skill in row:
    query= "select * from projecttablefreelancer where skillset like '%"+str(skill)+"%'"
    Cursor = Con.cursor()
    Cursor.execute(query)
    rows = Cursor.fetchall()
    print(skill, len(rows))
    if len(rows):
        with open('skills_'+skill+'.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter =',')
            data_rows = []
            for data in rows:
                d = [str(i).replace('\n', '').strip() for i in data]
                d.append(skill)
                data_rows.append(d)
            # print(data_rows)
            try:
                writer.writerows(data_rows)
            except Exception as e:
                print(e)



