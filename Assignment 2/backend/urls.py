from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.urls import path
from .views.users import *
from .views.item import *
from .views.purchase_header import *
from .views.sell_header import *
from .views.purchase_detail import *
from .views.sell_detail import *
from .views.report import *
from rest_framework.urlpatterns import format_suffix_patterns


schema_view = get_schema_view(
    openapi.Info(
        title="Stock Warehouse API",
        default_version='v1',
        description="Test Katekima Backend Developer",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    # user
    path('api/user/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user', UserRegistrationView.as_view(), name='user_register'),
    path('api/user/<int:pk>', UserEditView.as_view(), name='user_update'),

    # item
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<str:code>/", ItemDetailView.as_view(), name="item-detail"),
    path("items", ItemCreateView.as_view(), name="item-create"),
    path("items/<str:code>", ItemUpdateDeleteAPIView.as_view(), name="item-update-delete"),

    # purchase header
    path("purchase/", PurchaseHeaderListView.as_view(), name="purchase-list"),
    path("purchase/<str:code>/", PurchaseHeaderDetailView.as_view(), name="purchase-detail"),
    path("purchase", PurchaseHeaderCreateView.as_view(), name="purchase-create"),
    path("purchase/<str:code>", PurchaseHeaderUpdateDeleteAPIView.as_view(), name="purchase-update-delete"),

    # Sell header
    path("sell/", SellHeaderListView.as_view(), name="sell-list"),
    path("sell/<str:code>/", SellHeaderDetailView.as_view(), name="sell-detail"),
    path("sell", SellHeaderCreateView.as_view(), name="sell-create"),
    path("sell/<str:code>", SellHeaderUpdateDeleteAPIView.as_view(), name="sell-update-delete"),

    # purchase detail
    path("purchase/<str:header_code>/details/", PurchaseDetailListView.as_view(), name="purchase-detail-list"),
    path("purchase/<str:header_code>/details", PurchaseDetailCreateView.as_view(), name="purchase-detail-create"),

    # sell detail
    path("sell/<str:header_code>/details/", SellDetailListView.as_view(), name="sell-detail-list"),
    path("sell/<str:header_code>/details", SellDetailCreateView.as_view(), name="sell-detail-create"),


    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

report_urlpatterns = [
    path('report/<str:item_code>/', ItemReportView.as_view(), name='item_report'),
]

urlpatterns += format_suffix_patterns(report_urlpatterns, allowed=["json", "pdf"])