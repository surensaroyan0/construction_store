from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .api.product import ProductView, ProductDetailView
from .api.user import UserView
from .api.profile import ProfileDetailView
from .api.cart import CartView
from .api.about import AboutView
from .api.order import OrderView
from .api.payment_card import PaymentCardView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include("construction.payments.urls")),

    path('api/home/', ProductView.as_view(), name='home'),
    path('api/products/<str:category>/<str:subcategory>/', ProductDetailView.as_view(), name="get_by_filter"),

    path('api/user/login/', UserView.login, name="login"),
    path('api/user/register/', UserView.register, name="register"),
    path('api/user/logout/', UserView.log_out),
    path('api/user/<int:id>/delete/', UserView.delete, name="delete_profile"),
    path('api/user/forgot-password/', UserView.forgot_password, name="forgot_password"),
    path('api/user/confirm-code/', UserView.confirm_code, name="confirm_code"),
    path('api/user/change-password/', UserView.change_password, name="change_password"),

    path('api/user/profile/<int:id>/', ProfileDetailView.as_view(), name="profile"),

    path('api/cart/', CartView.as_view(), name="cart"),
    path('api/cart/delete/<int:product_id>/', CartView.delete, name="delete_product"),

    path('api/about/', AboutView.as_view(), name="about"),

    path('api/orders/', OrderView.as_view(), name="order"),

    path('api/payment-card/', PaymentCardView.as_view(), name="add_card")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
