from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from django.contrib.auth import views as auth_views

schema_view = get_swagger_view(title='Malaria Detection App')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('malaria.urls', namespace='malaria')),
    path('api/', include('malaria_api.urls', namespace='malaria_api')),
    path('api/auth/', include('authentication.urls', namespace='authentication')),
    path('swagger/', schema_view),
    path('swagger/accounts', include('rest_framework.urls')),
    path('predict/', include('mlApi.api.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
