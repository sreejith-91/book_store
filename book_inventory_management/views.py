import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import View

from book_inventory_management.book_utils import get_book_details, get_book_borrow_details
from book_inventory_management.models import BookInventoryDetail, BookBorrowDetail


@method_decorator(login_required, name='dispatch')
class BookListView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['book_detail'] = get_book_details()
        context['data_html'] = render_to_string('ajax/book_list.html', request=self.request, context=context)
        if self.request.user.is_superuser:
            context['borrow_detail'] = get_book_borrow_details()
        else:
            context['borrow_detail'] = get_book_borrow_details(user=self.request.user)
        context['borrowed_list'] = render_to_string('ajax/borrowed_list.html', request=self.request, context=context)

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(BookListView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UpdateInventory(View):
    def post(self, request):
        data = {'status': True}
        book_data = {}
        if request.POST.get('slug_val'):
            book_obj = get_book_details(book_id=request.POST.get('slug_val'))
            borrowed_count = book_obj.book_borrowed
            if borrowed_count != book_obj.total_book_count:
                try:
                    with transaction.atomic():
                        borrowed_count += 1
                        book_obj.book_borrowed = borrowed_count
                        book_obj.book_available = book_obj.total_book_count - borrowed_count
                        book_obj.save()
                        BookBorrowDetail.objects.create(
                            borrowed_by=request.user,
                            book=book_obj
                        )
                        book_data['book_detail'] = get_book_details()
                        data['data_html'] = render_to_string('ajax/book_list.html', request=request, context=book_data)
                        if self.request.user.is_superuser:
                            book_data['borrow_detail'] = get_book_borrow_details()
                        else:
                            book_data['borrow_detail'] = get_book_borrow_details(user=self.request.user)
                        data['borrowed_list'] = render_to_string('ajax/borrowed_list.html', request=request,
                                                                 context=book_data)

                except:
                    data['status'] = False
                    data['message'] = 'Something went wrong'
            else:
                data['status'] = False
                data['message'] = 'No book left'
        return HttpResponse(json.dumps(data), content_type="application/json")
