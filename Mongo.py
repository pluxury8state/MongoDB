import csv
import re
from pprint import pprint
import pymongo


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    artists_list = []
    with open(csv_file, encoding='utf8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:
            artists_list.append(row)

    #art_col - коллекция

    Dbase = db.art_col.insert_many(artists_list)

    pprint(Dbase.inserted_ids)




def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """

    sorted_database = db.art_col.find().sort('Цена', -1)
    for i in sorted_database:
        print(i)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """

    regex = re.compile('укажите регулярное выражение для поиска. ' \
                       'Обратите внимание, что в строке могут быть специальные символы, их нужно экранировать')


if __name__ == '__main__':

    # a = (read_data('artists.csv', 21))

    client = pymongo.MongoClient("mongodb+srv://Oleg:segere61@claster1.o4pxn.mongodb.net/Music?retryWrites=true&w=majority")

    music_artists_db = client['m_artists']#база данных

    # read_data('artists.csv', music_artists_db) #передал данные из csv в БД

    find_cheapest(music_artists_db)# тут почему-то происходит кривая сортировка


