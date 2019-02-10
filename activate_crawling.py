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


chosen_date = str(date(2019,1,1))


f = open("./failure_report/"+chosen_date+".txt", "w")

print(CHOSUN_START_QUOTE)
f.write(CHOSUN_START_QUOTE +'\n')
chosun_crawling_results = crawls.chosun(chosen_date)
for result in chosun_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(DONGA_START_QUOTE)
f.write(DONGA_START_QUOTE + '\n')
donga_crawling_results = crawls.donga(chosen_date)
for result in donga_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(KHAN_START_QUOTE)
f.write(KHAN_START_QUOTE+'\n')
khan_crawling_results = crawls.khan(chosen_date)
for result in khan_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(MUNHWA_START_QUOTE)
f.write(MUNHWA_START_QUOTE+'\n')
munhwa_crawling_results = crawls.munhwa(chosen_date)
for result in munhwa_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(KMIB_START_QUOTE)
f.write(KMIB_START_QUOTE+'\n')
kmib_crawling_results = crawls.kmib(chosen_date)
for result in kmib_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(SEOUL_START_QUOTE)
f.write(SEOUL_START_QUOTE+'\n')
seoul_crawling_results = crawls.seoul(chosen_date)
for result in seoul_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

print(MK_START_QUOTE)
f.write(MK_START_QUOTE+'\n')
mk_crawling_results = crawls.mk(chosen_date)
for result in mk_crawling_results:
    print(result)
    f.write(result + '\n')
print("")
f.write("\n")

sql_handler.converts_db_into_text_file()

f.close()
