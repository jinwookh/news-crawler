import crawls
import sql_handler
from datetime import date

CHOSUN_START_QUOTE = "CHOSUN CRAWLING STARTS!"
DONGA_START_QUOTE = "DONGA CRAWLING STARTS!"
KHAN_START_QUOTE = "KHAN CRAWLING STARTS!"
MUNHWA_START_QUOTE = "MUNHWA CRAWLING STARTS!"
KMIB_START_QUOTE = "KMIB CRAWLING STARTS!"
SEOUL_START_QUOTE = "SEOUL CRAWLING STARTS!"
MK_START_QUOTE = "MK CRAWLING STARTS!"

date =  str(date.today()).replace("-","")
f = open("./failure_report/"+date+".txt", "w")

print(CHOSUN_START_QUOTE)
chosun_crawling_results = crawls.chosun()
for result in chosun_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(DONGA_START_QUOTE)
donga_crawling_results = crawls.donga()
for result in donga_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(KHAN_START_QUOTE)
khan_crawling_results = crawls.khan()
for result in khan_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(MUNHWA_START_QUOTE)
munhwa_crawling_results = crawls.munhwa()
for result in munhwa_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(KMIB_START_QUOTE)
kmib_crawling_results = crawls.kmib()
for result in kmib_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(SEOUL_START_QUOTE)
seoul_crawling_results = crawls.seoul()
for result in seoul_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

print(MK_START_QUOTE)
mk_crawling_results = crawls.mk()
for result in mk_crawling_results:
    print(result)
    f.write(result + '\n')
print("")

sql_handler.converts_db_into_text_file()

f.close()
