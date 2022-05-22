from django.contrib import admin

from .models import Subscription, User



class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
    list_filter = ('pub_date',)


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
