import csv
import re
from pprint import pprint
import pymongo
from _datetime import datetime


def date_sort(db, first_date, second_date):
    fd = from_string_to_datetime(first_date)
    sd = from_string_to_datetime(second_date)
    sorted_database = db.art_col.find({'Дата':{'$lte': sd, '$gte': fd}}).sort('Дата', 1)
    for i in sorted_database:
        print(i)


def from_string_to_datetime(string_with_date):
    date_massive = ['2020']
    date_massive += string_with_date.split('.')
    true_massive = []
    for i in date_massive:
        true_massive.append(int(i))
    datetime_obj = datetime(true_massive[0], true_massive[2], true_massive[1])
    return datetime_obj


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    artists_list = []
    with open(csv_file, encoding='utf8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:
            artists_list.append(row)

        for person in artists_list:
            price = person['Цена']
            person['Цена'] = int(price)
            person['Дата'] = from_string_to_datetime(person['Дата'])

    #art_col - коллекция

    db.art_col.insert_many(artists_list)


def delete_data(db):
    db.art_col.drop()


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """

    sorted_database = db.art_col.find().sort('Цена', 1)
    for i in sorted_database:
        print(i)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """

    regex = re.compile(f'(.)*({name})(.)*')
    sorted_database = db.art_col.find({'Исполнитель': regex}).sort('Цена', 1)

    for i in sorted_database:
        print(i)

if __name__ == '__main__':

    client = pymongo.MongoClient()

    music_artists_db = client['m_artists']#база данных

    delete_data(music_artists_db)#удалить коллекцию из БД

    read_data('artists.csv', music_artists_db) #передал данные из csv в БД

    find_cheapest(music_artists_db)

    find_by_name('Th', music_artists_db)

    first_date = input('введите с какого числа нужно вести поиск(без года, через точку , сначала число , потом месяц):')

    second_date = input('введите по какое число нужно вести поиск(без года, через точку , сначала число , потом месяц):')

    date_sort(music_artists_db, first_date, second_date)
