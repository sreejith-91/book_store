from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from user_access.models import User


class BookInventoryDetail(models.Model):
    book_name = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    total_book_count = models.IntegerField(blank=True, null=True)
    book_borrowed = models.IntegerField(blank=True, null=True)
    book_available = models.IntegerField(blank=True, null=True)
    creation_timestamp = models.DateTimeField(_('Creation timestamp'), null=True, blank=True,
                                              auto_now=True)
    slug = models.SlugField(max_length=255, auto_created=True, editable=False)
    status = models.BooleanField(default=True)


class BookBorrowDetail(models.Model):
    book = models.ForeignKey(BookInventoryDetail, on_delete=models.CASCADE,
                             related_name="book_borrow_rel",
                             null=True,
                             blank=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="book_borrow_rel",
                                    null=True,
                                    blank=True)
    borrowed_on = models.DateTimeField(_('Creation timestamp'), null=True, blank=True,
                                       auto_now=True)
