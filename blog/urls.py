from django.urls import include, path
from . import views

urlpatterns=[
    path('add_record',views.add_record, name='add_record'),
    path('<int:id>', views.post_record, name='post_record'),
    path('<int:id>', views.post_record, name='add_a'),
    path('',views.post_list, name='post_list'),
]
