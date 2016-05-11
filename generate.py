import random
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime
from django.db import models
from django.db.models import F
from traveler.models import Person, Message, Comment, Country, City, Trip, Tag, Like
from string import letters

mx = 1000

def gennumber(n):
    a = 0
    for i in range(n):
        a *= 10
        a += random.randint(0, 9)
    return a

def genstr(n):
    s = ''
    for i in range(n):
        s += random.choice(letters.lower())
    return s

def gentags_cities(n):
    persons = Person.objects.all()
    cities = City.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    c_tp = ContentType.objects.get_for_model(City)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    tags = []
    count = 0
    for i in range(n):
        count += 1
        tags.append(Tag(person=random.choice(persons), text='#'+random.choice(words),
                           content_type=c_tp, time=tm, object_id=random.choice(cities).id))
        if (count == mx):
            Tag.objects.bulk_create(tags)
            tags = []
            count = 0
    Tag.objects.bulk_create(tags)


def gentags_countries(n):
    persons = Person.objects.all()
    countries = Country.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    c_tp = ContentType.objects.get_for_model(Country)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    tags = []
    count = 0
    for i in range(n):
        count += 1
        tags.append(Tag(person=random.choice(persons), text='#'+random.choice(words),
                           content_type=c_tp, time=tm, object_id=random.choice(countries).id))
        if (count == mx):
            Tag.objects.bulk_create(tags)
            tags = []
            count = 0
    Tag.objects.bulk_create(tags)


def gentags_trips(n):
    persons = Person.objects.all()
    trips = Trip.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    c_tp = ContentType.objects.get_for_model(Trip)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    tags = []
    count = 0
    for i in range(n):
        count += 1
        tags.append(Tag(person=random.choice(persons), text='#'+random.choice(words),
                           content_type=c_tp, time=tm, object_id=random.choice(trips).id))
        if (count == mx):
            Tag.objects.bulk_create(tags)
            tags = []
            count = 0
    Tag.objects.bulk_create(tags)


def gentags_persons(n):
    persons = Person.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    c_tp = ContentType.objects.get_for_model(Person)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    tags = []
    count = 0
    for i in range(n):
        count += 1
        tags.append(Tag(person=random.choice(persons), text='#'+random.choice(words),
                           content_type=c_tp, time=tm, object_id=random.choice(persons).id))
        if (count == mx):
            Tag.objects.bulk_create(tags)
            tags = []
            count = 0
    Tag.objects.bulk_create(tags)


def genlikes_pers(n):
    persons = Person.objects.all()
    c_tp = ContentType.objects.get_for_model(Person)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    likes = []
    count = 0
    for i in range(n):
        count += 1
        likes.append(Like(person=random.choice(persons), content_type=c_tp,
                           time=tm, object_id=random.choice(persons).id))
        if count == mx:
            Like.objects.bulk_create(likes)
            likes = []
            count = 0
    Like.objects.bulk_create(likes)


def genlikes_cities(n):
    persons = Person.objects.all()
    cities_tmp = City.objects.all().values('id')
    cities = []
    for city in cities_tmp:
        cities.append(city['id'])
    cities_tmp = []
    cities_bulk = random.sample(cities, mx)
    c_tp = ContentType.objects.get_for_model(City)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    likes = []
    count = 0
    for i in range(n):
        city = cities_bulk[count]
        likes.append(Like(person=random.choice(persons), content_type=c_tp,
                           time=tm, object_id=city))
        count += 1
        if count == mx:
            Like.objects.bulk_create(likes)
            City.objects.filter(id__in=cities_bulk).update(likes_count=F('likes_count') + 1)
            cities_bulk = random.sample(cities, mx)
            likes = []
            count = 0
            print i + 1
    Like.objects.bulk_create(likes)

def genlikes_countries(n):
    persons = Person.objects.all()
    countries_tmp = Country.objects.all().values('id')
    countries = []
    for i in countries_tmp:
        countries.append(i['id'])

    countries_tmp = []
    c_tp = ContentType.objects.get_for_model(Country)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    likes = []
    count = 0
    countries_bulk = random.sample(countries, mx)
    for i in range(n):
        country = countries_bulk[count]
        count += 1
        likes.append(Like(person=random.choice(persons), content_type=c_tp,
                           time=tm, object_id=country))
        if count == mx:
            Like.objects.bulk_create(likes)
            Country.objects.filter(id__in=countries_bulk).update(likes_count=F('likes_count') + 1)
            countries_bulk = random.sample(countries, mx)
            likes = []
            count = 0
    Like.objects.bulk_create(likes)


def genlikes_comments(n):
    persons = Person.objects.all()
    comments = Comment.objects.all()
    c_tp = ContentType.objects.get_for_model(Comment)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    likes = []
    count = 0
    for i in range(n):
        count += 1
        likes.append(Like(person=random.choice(persons), content_type=c_tp,
                           time=tm, object_id=random.choice(comments).id))
        if count == mx:
            Like.objects.bulk_create(likes)
            likes = []
            count = 0
    Like.objects.bulk_create(likes)


def genlikes_messages(n):
    persons = Person.objects.all()
    messages = Message.objects.all()
    c_tp = ContentType.objects.get_for_model(Message)
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    likes = []
    count = 0
    for i in range(n):
        count += 1
        likes.append(Like(person=random.choice(persons), content_type=c_tp,
                           time=tm, object_id=random.choice(messages).id))
        if count == mx:
            Like.objects.bulk_create(likes)
            likes = []
            count = 0
    Like.objects.bulk_create(likes)


def gencomments(n, persons, cities):
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    comments = []
    all_comments = Comment.objects.all()
    count = 0
    for i in range(n):
        n_words = random.randint(1, 40)
        count += 1
        txt = ''
        for j in range(n_words):
            word = random.choice(words)[:-1]
            txt = txt + word + ' '
        pers = random.choice(persons)
        prev = Comment(text=txt, person=pers, city=random.choice(cities),
                                   time = tm)
        x = random.randint(0, 1)
        if x != 0:
            try:
                prev.comment_id = random.choice(all_comments)
                prev.city = prev.comment_id.city
            except:
                pass
        comments.append(prev)
        if count == mx:
            Comment.objects.bulk_create(comments)
            comments = []
            count = 0
    Comment.objects.bulk_create(comments)


def genmessages(n):
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    persons = Person.objects.all()
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    messages = []
    count = 0
    for i in range(n):
        count += 1
        txt = ''
        n_words = random.randint(1, 70)
        for j in range(n_words):
            word = random.choice(words)[:-1]
            txt = txt + word + ' '
        messages.append(Message(from_person=random.choice(persons),
                               to_person=random.choice(persons),
                               text=txt, time=tm))
        if count == mx:
            Message.objects.bulk_create(messages)
            count = 0
            messages = []
    Message.objects.bulk_create(messages)


def gentrips(n):
    cities = City.objects.all()
    persons = Person.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    trips = []
    count = 0
    tm = datetime.datetime.now()
    max_id = Trip.objects.aggregate(id=models.Max('id'))['id']
    for i in range(n):
        count += 1
        city = random.choice(cities)
        nm = random.choice(words)[:-1]
        x = random.randint(0, 1)
        cur = Trip(city=city, name=nm, date_start=tm,
                   date_end=tm, open_flag=x)
        trips.append(cur)
        if count == mx:
            Trip.objects.bulk_create(trips)
            count = 0
            trips = []
    Trip.objects.bulk_create(trips)
    trips = Trip.objects.filter(id__gt = max_id)
    count = 0
    arr = []
    for cur in trips:
        n_obj = random.randint(1, 10)
        cur_pers = random.sample(persons, n_obj)
        for i in range(n_obj):
            arr.append(cur.persons.through(trip=cur,
                                           person=cur_pers[i]))
            count += 1
            if count == mx:
                cur.persons.through.objects.bulk_create(arr)
                arr = []
                count = 0
    cur.persons.through.objects.bulk_create(arr)


def gentrips_to_city(city_id, n):
    city = City.objects.get(id=city_id)
    persons = Person.objects.all()
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    trips = []
    count = 0
    tm = datetime.datetime.now()
    max_id = Trip.objects.aggregate(id=models.Max('id'))['id']
    for i in range(n):
        count += 1
        nm = random.choice(words)[:-1]
        x = random.randint(0, 1)
        cur = Trip(city=city, name=nm, date_start=tm,
                   date_end=tm, open_flag=x)
        trips.append(cur)
        if count == mx:
            Trip.objects.bulk_create(trips)
            count = 0
            trips = []
    Trip.objects.bulk_create(trips)
    trips = Trip.objects.filter(id__gt = max_id)
    count = 0
    arr = []
    for cur in trips:
        n_obj = random.randint(1, 10)
        cur_pers = random.sample(persons, n_obj)
        for i in range(n_obj):
            arr.append(cur.persons.through(trip=cur,
                                           person=cur_pers[i]))
            count += 1
            if count == mx:
                cur.persons.through.objects.bulk_create(arr)
                arr = []
                count = 0
    cur.persons.through.objects.bulk_create(arr)


def genpersons(n):
    file_names = open('data/Generation/names.txt')
    file_surnames = open('data/Generation/surnames.txt')
    names = file_names.readlines()
    surnames = file_surnames.readlines()
    cities = City.objects.all()
    countries = Country.objects.all()
    count = 0
    tm = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    persons_arr = []
    for i in range(n):
        count += 1
        city = random.choice(cities).name
        country = random.choice(countries)
        tel = gennumber(8)
        user = genstr(8)
        mail = genstr(6) + '@mail.ru'
        first_nm = random.choice(names)[:-1]
        last_nm = random.choice(surnames)[:-1]
        passw = '123'

        cur = Person(username=user, first_name=first_nm, last_name=last_nm,
                              email=mail, vk_id='vk.com/' + user, password = passw,
                              phone=tel, country=country, city_from=city,
                              last_login = tm)
        #cur.set_password(passw)
        persons_arr.append(cur)
        if count == mx:
            Person.objects.bulk_create(persons_arr)
            count = 0
            persons_arr = []
    Person.objects.bulk_create(persons_arr)

    persons = Person.objects.all()
    persons_arr = Person.objects.filter(last_login = tm)
    arr = []
    count = 0
    for cur in persons_arr:
        n_obj = random.randint(0, 10)
        to_pers = random.sample(persons, n_obj)
        for i in range(n_obj):
            arr.append(cur.persons_add.through(from_person=cur,
                                               to_person=to_pers[i]))
            count += 1
            if count == mx:
                cur.persons_add.through.objects.bulk_create(arr)
                arr = []
                count = 0
    cur.persons_add.through.objects.bulk_create(arr)
    arr = []
    count = 0
    for cur in persons_arr:
        n_obj = random.randint(0, 10)
        cts = random.sample(cities, n_obj)
        for i in range(n_obj):
            arr.append(cur.cities_add.through(person=cur,
                                               city=cts[i]))
            count += 1
            if count == mx:
                cur.cities_add.through.objects.bulk_create(arr)
                arr = []
                count = 0
    cur.cities_add.through.objects.bulk_create(arr)


def gencities(n):
    file_cities = open('data/Generation/cities.txt')
    file_words = open('data/Generation/words.txt')
    cities = file_cities.readlines()
    words = file_words.readlines()
    countries = Country.objects.all()
    n_words = 20
    count = 0
    cities_arr = []
    for i in range(n):
        city = random.choice(cities)[:-1]
        country = random.choice(countries)
        descr = ''
        count += 1
        for j in range(n_words):
            word = random.choice(words)[:-1]
            descr = descr + word + ' '
        cities_arr.append(City(name=city, country=country, description=descr))
        if count == mx:
            City.objects.bulk_create(cities_arr)
            count = 0
            cities_arr = []
    City.objects.bulk_create(cities_arr)


def gencities_to_country(country_id, n):
    file_cities = open('data/Generation/cities.txt')
    file_words = open('data/Generation/words.txt')
    cities = file_cities.readlines()
    words = file_words.readlines()
    country = Country.objects.get(id=country_id)
    n_words = 20
    count = 0
    cities_arr = []
    for i in range(n):
        city = random.choice(cities)[:-1]
        descr = ''
        count += 1
        for j in range(n_words):
            word = random.choice(words)[:-1]
            descr = descr + word + ' '
        cities_arr.append(City(name=city, country=country, description=descr))
        if count == mx:
            City.objects.bulk_create(cities_arr)
            count = 0
            cities_arr = []
    City.objects.bulk_create(cities_arr)


def gencountries(n):
    file_countr = open('data/Generation/countries.txt')
    file_words = open('data/Generation/words.txt')

    countries = file_countr.readlines()
    words = file_words.readlines()

    n_words = 20
    count = 0
    countr_arr = []
    for i in range(n):
        count += 1
        country = random.choice(countries)[:-1]
        descr = ''
        for j in range(n_words):
            word = random.choice(words)[:-1]
            descr = descr + word + ' '
        countr_arr.append(Country(name=country, description=descr))
        if count == mx:
            Country.objects.bulk_create(countr_arr)
            count = 0
            countr_arr = []
    Country.objects.bulk_create(countr_arr)

def genpersontext():
    file_words = open('data/Generation/words.txt')
    words = file_words.readlines()
    txt = ''
    n_words = random.randint(1, 70)
    for j in range(n_words):
        word = random.choice(words)[:-1]
        txt = txt + word + ' '
    Person.objects.all().update(text = txt)


def gencomments_for_city(n, city_id):
    persons = Person.objects.all()
    cities = City.objects.get(id=city_id)
    cities = [cities]
    gencomments(n, persons, cities)


def genallcomm(n):
    persons = Person.objects.all()
    cities = City.objects.all()
    k = int(0.0001 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.001 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.005 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.01 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.02 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.05 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.1 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.2 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.3 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.4 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.4 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.4 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.3 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.3 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.5 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.5 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.5 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.5 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    k = int(0.5 * n)
    n -= k
    gencomments(k, persons, cities)
    print k
    gencomments(n, persons, cities)
    print n
