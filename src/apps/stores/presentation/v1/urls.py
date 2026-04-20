from django.urls import path
from .views import StoreListView, MyStoresView

app_name = "stores_api"

urlpatterns = [
    path("", StoreListView.as_view(), name="store-list"),
    path("my/", MyStoresView.as_view(), name="my-stores"),
]
