from django.contrib import admin

# Register your models here.
from book_inventory_management.models import *
admin.site.register(BookInventoryDetail)
admin.site.register(BookBorrowDetail)