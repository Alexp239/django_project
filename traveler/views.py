from django.shortcuts import render, redirect
from django.http import Http404
from traveler.models import Person, Message, Comment, Country, City, Trip, Tag, Like
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Prefetch, F
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import TripForm

def add_variables(var, request):
    if request.user.is_authenticated():
        not_read_mes = Message.objects.filter(to_person=request.user, read_flag=False).count()
    else:
        not_read_mes = 0
    var.update([('user', request.user), ('count_mes', not_read_mes)])
    return var

def add_trip(request, city_id):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            city = City.objects.get(id = int(city_id))
            trip = Trip(name=name, date_end=date_end, date_start=date_start, city=city, open_flag=True)
            trip.save()
            trip.persons.add(request.user)
            return redirect('/city/%s/1/1/' % city.id)

    else:
        form = TripForm()
    return render(request, 'add_trip.html', {'form': form, 'city_id': city_id})

def add_tag_country(request, country_id):
    if request.method == 'POST':
        country_id = int(country_id)
        text = request.POST.get('tag', '')
        text = '#' + text
        country = Country.objects.get(id=country_id)
        try:
            country.tags.get(text=text)
        except:
            content_type_id = ContentType.objects.get_for_model(Country)
            tag = Tag(person=request.user, text=text, content_type=content_type_id, \
                                    time=timezone.now(), object_id=country_id)
            tag.save()
        return redirect('/country/%s/1/' % country_id)

def add_tag_city(request, city_id):
    if request.method == 'POST':
        city_id = int(city_id)
        text = request.POST.get('tag', '')
        text = '#' + text
        city = City.objects.get(id=city_id)
        try:
            city.tags.get(text=text)
        except:
            content_type_id = ContentType.objects.get_for_model(City)
            tag = Tag(person=request.user, text=text, content_type=content_type_id, \
                                    time=timezone.now(), object_id=city_id)
            tag.save()
        return redirect('/city/%s/1/1/' % city_id)

def add_tag_trip(request, trip_id):
    if request.method == 'POST':
        trip_id = int(trip_id)
        text = request.POST.get('tag', '')
        text = '#' + text
        trip = Trip.objects.get(id=trip_id)
        try:
            trip.tags.get(text=text)
        except:
            content_type_id = ContentType.objects.get_for_model(Trip)
            tag = Tag(person=request.user, text=text, content_type=content_type_id, \
                                    time=timezone.now(), object_id=trip_id)
            tag.save()
        return redirect('/city/%s/1/1/' % trip.city.id)

def add_tag_person(request, person_id):
    if request.method == 'POST':
        person_id = int(person_id)
        text = request.POST.get('tag', '')
        text = '#' + text
        person = Person.objects.get(id=person_id)
        try:
            person.tags.get(text=text)
        except:
            content_type_id = ContentType.objects.get_for_model(Person)
            tag = Tag(person=request.user, text=text, content_type=content_type_id, \
                                    time=timezone.now(), object_id=person_id)
            tag.save()
        return redirect('/profile/%s/' % person_id)

def update_add_cities(request, city_id):
    city = City.objects.get(id=city_id)
    if city in request.user.cities_add.all():
        request.user.cities_add.remove(city)
    else:
        request.user.cities_add.add(city)
    return redirect('/city/%s/1/1/' % city_id)

def update_trip_persons(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if request.user in trip.persons.all():
        trip.persons.remove(request.user)
    else:
        trip.persons.add(request.user)
    return redirect('/city/%s/1/1/' % trip.city.id)

def update_like_country(request, object_id):
    object_id = int(object_id)
    try:
        content_type_id = ContentType.objects.get_for_model(Country)
        l = Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=object_id).delete()
        Country.objects.filter(id=object_id).update(likes_count=F('likes_count') - 1)
    except:
        l = Like(person_id=request.user.id, content_type=content_type_id, object_id=object_id, time=timezone.now())
        Country.objects.filter(id=object_id).update(likes_count=F('likes_count') + 1)
        l.save()
    return redirect('/country/%s/1/' % object_id)


def update_like_city(request, object_id):
    object_id = int(object_id)
    try:
        content_type_id = ContentType.objects.get_for_model(City)
        l = Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=object_id).delete()
        City.objects.filter(id=object_id).update(likes_count=F('likes_count') - 1)
    except:
        l = Like(person_id=request.user.id, content_type=content_type_id, object_id=object_id, time=timezone.now())
        City.objects.filter(id=object_id).update(likes_count=F('likes_count') + 1)
        l.save()
    return redirect('/city/%s/1/1/' % object_id)

def update_like_person(request, object_id):
    object_id = int(object_id)
    try:
        content_type_id = ContentType.objects.get_for_model(Person)
        l = Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=object_id).delete()
    except:
        l = Like(person_id=request.user.id, content_type=content_type_id, object_id=object_id, time=timezone.now())
        l.save()
    return redirect('/profile/%s/' % object_id)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/main/')
            else:
                return redirect('/main/')
        else:
            return redirect('/main/')

def user_logout(request):
    logout(request)
    return redirect('/main/')

def add_message(request, person_id):
    if request.method == 'POST':
        text = request.POST.get('input_message', '')
        to_pers = Person.objects.get(id=person_id)
        mes = Message(from_person=request.user, to_person=to_pers, text=text, time=timezone.now())
        mes.save()
        return redirect('/messages/%s/' % person_id)

def add_comment(request, city_id, comment=None):
    if request.method == 'POST':
        text = request.POST.get('text_comment', '')
        city = City.objects.get(id=city_id)
        if comment != None:
            comment = Comment.objects.get(id=int(comment))
        com = Comment(text=text, person=request.user, city=city, time=timezone.now(), comment_id=comment)
        com.save()
        return redirect('/city/%s/1/1/' % city_id)

def profile(request, person_id):
    try:
        person = Person.objects.select_related('country').prefetch_related(Prefetch('cities_add', queryset=City.objects.only('name'))).get(id=person_id)
        try:
            content_type_id = ContentType.objects.get_for_model(Person)
            Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=person_id)
            is_liked = 1
        except:
            is_liked = 0
    except:
        raise Http404
    return render(
        request, 'profile.html', add_variables({'person': person, 'is_liked': is_liked}, request)
    )

def city(request, city_id, trips_page, comments_page):
    try:
        count_tr = 3
        count_com = 5
        offset_tr = (int(trips_page) - 1) * count_tr
        offset_com = (int(comments_page) - 1) * count_com

        city = City.objects.get(id = city_id)
        c_tp = ContentType.objects.get_for_model(City)
        tags = Tag.objects.filter(content_type=c_tp, object_id=city.id).only('text')
        comments = Comment.objects.filter(city=city.id).select_related('person')[offset_com:offset_com+count_com]

        trips = Trip.objects.filter(city=city.id)[offset_tr:offset_tr+count_tr]
        trips = trips.prefetch_related(Prefetch('persons', queryset=Person.objects.only('last_name', 'first_name')),\
                                Prefetch('tags', queryset=Tag.objects.only('text')))

        cnt_trips = Trip.objects.filter(city=city.id).count()
        cnt_comments = Comment.objects.filter(city=city.id).count()

        max_page_tr = int(ceil(float(cnt_trips) / count_tr))
        max_page_com = int(ceil(float(cnt_comments) / count_com))

        content_type_id = ContentType.objects.get_for_model(City)
        try:
            Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=city_id)
            is_liked = 1
        except:
            is_liked = 0
        is_city_add = 0
        if city in request.user.cities_add.all():
            is_city_add = 1

    except:
        raise Http404
    return render(
        request, 'city.html', add_variables({'city': city, 'tags': tags, 'comments': comments,
                        'trips': trips, 'max_page_trips': max_page_tr, 'trips_page': int(trips_page),
                        'max_page_comments': max_page_com, 'comments_page': int(comments_page),
                        'is_liked': is_liked, 'is_city_add': is_city_add}, request)
    )


def main(request):
    count = 10
    best_countries = Country.objects.all().order_by('-likes_count')[:count]
    best_cities = City.objects.all().order_by('-likes_count')[:count]
    best_tags = Tag.objects.all().values('text').annotate(count_tags=Count('text')).order_by('-count_tags')[:5]
    return render(request, 'main.html', add_variables({'countries': best_countries,
                            'cities': best_cities, 'tags': best_tags, 'req': request}, request))


def registration(request):
    return render(request, 'registration.html', {})


def messages(request, to_person_id):
    try:
        from_person_id = request.user.id
        to_person = Person.objects.get(id = to_person_id)
        messages = Message.objects.filter(Q(from_person_id = from_person_id,
                                            to_person_id = to_person_id) |
                                          Q(from_person_id = to_person_id,
                                            to_person_id = from_person_id))
        Message.objects.filter(from_person_id=to_person_id, to_person_id=from_person_id, read_flag = False).update(read_flag=True)
    except:
        raise Http404
    return render(
        request, 'messages.html', add_variables({'messages': messages,
                                   'from_person_id': int(from_person_id),
                                   'to_person_id' : int(to_person_id),
                                   'to_person': to_person}, request))

def dialogs(request):
    try:
        current_person_id = request.user.id
        messages = Message.objects.filter(Q(from_person_id = current_person_id) |
                    Q(to_person_id = current_person_id)).select_related('to_person', 'from_person')
        persons = []
        persons_id = []
        current_person_id = int(current_person_id)
        for mes in messages:
            if mes.from_person_id == current_person_id:
                pers_id = mes.to_person_id
                pers = mes.to_person
            else:
                pers_id = mes.from_person_id
                pers = mes.from_person
            if pers_id not in persons_id:
                persons_id.append(pers_id)
                persons.append((pers, mes))
    except:
        raise Http404
    return render(request, 'dialogs.html', add_variables({'persons': persons,
                        'current_person_id': current_person_id}, request))


def countries(request, page):
    count = 10
    offset = (int(page) - 1) * count
    cnt = Country.objects.count()
    max_page = int(ceil(float(cnt) / count))
    if (cnt == 0) or (offset < cnt):
        countries = Country.objects.all().only('name', 'likes_count')[offset:(offset + count)]
        countries = countries.prefetch_related(Prefetch('tags', queryset=Tag.objects.only('id'))).annotate(cnt_cities=Count('city'))
    else:
        raise Http404
    return render(
        request, 'countries.html', add_variables({'countries': countries, 'page': int(page),
                    'max_page': max_page}, request)
    )

def country(request, country_id, page):
    count = 10
    country = Country.objects.get(id = country_id)
    offset = (int(page) - 1) * count
    cnt = City.objects.filter(country = country_id).count()
    max_page = int(ceil(float(cnt) / count))
    content_type_id = ContentType.objects.get_for_model(Country)
    try:
        Like.objects.get(person_id=request.user.id, content_type=content_type_id, object_id=country_id)
        is_liked = 1
    except:
        is_liked = 0
    if (cnt == 0) or (offset < cnt):
        cities = City.objects.filter(country = country_id).only('name', 'likes_count')[offset:(offset + count)]
        cities = cities.prefetch_related(Prefetch('tags', queryset=Tag.objects.only('id'))).annotate(cnt_trips = Count('trip'))
    else:
        raise Http404
    return render(
        request, 'country.html', add_variables({'cities': cities, 'country': country,
                'page': int(page), 'max_page': max_page, 'is_liked': is_liked}, request)
    )
