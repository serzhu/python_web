from django.urls import path
from . import views


app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='quotes'),
    path('<int:page>', views.main, name='quotes_paginate'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<int:author_id>', views.author_info, name='author_info'),
    path('tag/<int:tag_id>', views.quotes_by_tag, name='quotes_by_tag'),
    path('tag/<int:tag_id>/<int:page>', views.quotes_by_tag, name='quotes_by_tag_paginate'),

]