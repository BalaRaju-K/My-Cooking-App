from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination

class ReviewListPagination(PageNumberPagination):
    page_size = 2


class RecipeListPagination(CursorPagination, LimitOffsetPagination):
    page_size = 1
    #default_limit = 2

class DietListPagination(CursorPagination, LimitOffsetPagination):
    page_size = 3
    #default_limit = 3