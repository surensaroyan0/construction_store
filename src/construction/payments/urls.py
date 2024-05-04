from django.urls import path

from .views import CreateCheckoutSessionView, SuccessView, CancelView

urlpatterns = [
    path('product/<int:id>/', CreateCheckoutSessionView.as_view(), name='product_detail'),
    path('create-checkout-session/<id>/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('cancel/', CancelView.as_view(), name="cancel"),
    path('success/', SuccessView.as_view(), name="success")
]
