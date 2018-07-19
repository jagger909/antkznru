from django.contrib.auth.decorators import login_required
from django.urls import path

from categories.views import CategoriesEdit

urlpatterns = (
    path('', login_required(CategoriesEdit.as_view()), name="categories_edit"),
)
