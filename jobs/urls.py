from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', job_landing_page, name='job_landing_page'),
    path('profile/',user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('applicant-dashboard/', applicant_dashboard, name='applicant_dashboard'),
    path('create_job_advertisement/', create_job_advertisement, name='create_job_advertisement'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),  # Make sure this is present
    path('job/<int:job_id>/apply/', apply_for_job, name='apply_for_job'),
    path('job_list/', job_list, name='job_list'),
    path('applicant_job_list/', applicant_job_list, name='applicant_job_list'),
    path('applications/review/', review_applications, name='review_applications'),
    path('applications/<int:application_id>/approve/', approve_application, name='approve_application'),
    path('applications/<int:application_id>/reject/', reject_application, name='reject_application'),
    path('applied_jobs/',applied_jobs, name='applied_jobs'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

