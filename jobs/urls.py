from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', job_landing_page, name='job_landing_page'),
    path('profile/',user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', dashboard, name='admin_dashboard'),
    path('applicant-dashboard/', dashboard, name='applicant_dashboard'),
    path('create_job_advertisement/', create_job_advertisement, name='create_job_advertisement'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),  # Make sure this is present


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

