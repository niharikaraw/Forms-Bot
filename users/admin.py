from django.contrib import admin

from users.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Campaign)
admin.site.register(Bots)
admin.site.register(Questions)
admin.site.register(Options)
admin.site.register(Responses)
