import crawls
import sql_handler
from datetime import date

date =  str(date.today()).replace("-","")
f = open("./failure_report/"+date+".txt", "w")

chosun_crawling_results = crawls.chosun()
print("")
donga_crawling_results = crawls.donga()
print("")
khan_crawling_results = crawls.khan()
print("")
munhwa_crawling_results = crawls.munhwa()
print("")
kmib_crawling_results = crawls.kmib()
print("")

for result in chosun_crawling_results:
    f.write(result + '\n')
f.write('\n')

for result in donga_crawling_results:
    f.write(result + '\n')
f.write('\n')

for result in khan_crawling_results:
    f.write(result + '\n')
f.write('\n')

for result in munhwa_crawling_results:
    f.write(result + '\n')
f.write('\n')

for result in kmib_crawling_Results:
    f.write(result + '\n')
f.write('\n')

sql_handler.converts_db_into_text_file()

f.close()
