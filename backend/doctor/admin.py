from django.contrib import admin

from .models import Doctor, Day, Hour


admin.site.register(Doctor)
admin.site.register(Day)
admin.site.register(Hour)
