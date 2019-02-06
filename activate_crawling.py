import crawls
import sql_handler
from datetime import date

date =  str(date.today()).replace("-","")
f = open("./failure_report/"+date+".txt", "w")

chosun_crawling_results = crawls.chosun()
print("")
donga_crawling_results = crawls.donga()
print("")

for result in chosun_crawling_results:
    f.write(result + '\n')
f.write('\n')

for result in donga_crawling_results:
    f.write(result + '\n')
f.write('\n')

sql_handler.converts_db_into_text_file()
