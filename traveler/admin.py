from django.contrib import admin

from traveler.models import Person, Message, Comment, Country, City, Trip, Tag, Like

class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'date_joined')
    raw_id_fields = ('country', 'cities_add')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    raw_id_fields = ('country', )
    list_select_related = ('country', )

class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'date_start', 'date_end', 'open_flag')
    raw_id_fields = ('city', 'persons')
    list_select_related = ('city', )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'time')
    raw_id_fields = ('from_person', 'to_person')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'city', 'comment_id', 'time')
    raw_id_fields = ('city', 'comment_id', 'person')
    list_select_related = ('city', 'comment_id')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'time')
    list_select_related = ('content_type', )
    raw_id_fields = ('person', )
    list_filter = ('content_type', )

class TagAdmin(admin.ModelAdmin):
    list_display = ('text', 'person', 'content_type', 'object_id', 'time')
    list_select_related = ('content_type', 'person')
    raw_id_fields = ('person', )
    list_filter = ('content_type', )

admin.site.register(Person, PersonAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country)
admin.site.register(City, CityAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
