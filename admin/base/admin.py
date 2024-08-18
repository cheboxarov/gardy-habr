from django.contrib import admin
from .models import Users, Timers, Payments, Categories, Orders, Prices


admin.site.register(Users)
admin.site.register(Timers)
admin.site.register(Payments)
admin.site.register(Categories)
admin.site.register(Orders)
admin.site.register(Prices)

# Register your models here.
