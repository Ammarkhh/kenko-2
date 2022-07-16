from django.contrib import admin
from django.contrib.auth.models import Group

from auths.models import User

# Removing the Group Permissions Admin

admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
