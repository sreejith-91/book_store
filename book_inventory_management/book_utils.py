from book_inventory_management.models import BookInventoryDetail, BookBorrowDetail


def get_book_details(slug=None, book_id=None):
    result = None
    if book_id:
        result = BookInventoryDetail.objects.get(pk=book_id)
    elif slug:
        result = BookInventoryDetail.objects.get(slug=slug)
    else:
        result = BookInventoryDetail.objects.filter(status=True)
    return result


def get_book_borrow_details(user=None):
    if user:
        result = BookBorrowDetail.objects.filter(borrowed_by=user)
    else:
        result = BookBorrowDetail.objects.all()
    return result

