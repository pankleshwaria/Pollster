from django.contrib import admin
from .models import Questions, Choices


admin.site.site_title = "Pollster Admin Area"
admin.site.site_header = "Pollster Admin"
admin.site.index_title = "Welcome to Pollster admin area"


admin.site.register(Questions)
admin.site.register(Choices)
