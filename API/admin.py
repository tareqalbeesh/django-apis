from django.contrib import admin
from . import models
# Register your models here.
admin.site.register([models.Cart, models.Category,
                    models.MenuItem, models.Order, models.OrderItem])
