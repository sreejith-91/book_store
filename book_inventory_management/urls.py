from django.urls import path

from book_inventory_management.views import *
app_name = "book_inventory_management"
urlpatterns = [
    path('view', BookListView.as_view(), name='book_list'),
]