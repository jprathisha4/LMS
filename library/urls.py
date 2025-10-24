from django.urls import path
# from django.views.generic import TemplateView
from . import views
# from library import views

# from .views import scan_barcode
from django.contrib.auth import views as auth_views
# from .views import CustomAdminLoginView




urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    # path('signup/', views.admin_signup, name='admin_signup'),
    path('login/', views.admin_login, name='admin_login'),
    #  path("login/", CustomAdminLoginView.as_view(), name="custom_admin_login"),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('dashboard/add_book/', views.add_book, name='add_book'),
    path('dashboard/view-books/', views.view_books, name='view_books'),
    path('dashboard/issue_book/', views.issue_book, name='issue_book'),
    path('dashboard/view_issued/', views.view_issued_books, name='view_issued_books'),
    path('dashboard/view_students/', views.view_students, name='view_students'),
    path('genre/<int:genre_id>/', views.genre_books_view, name='genre_books'),
    path('dashboard/add-genre/', views.add_genre, name='add_genre'),
    path('dashboard/genres/', views.view_genres, name='view_genres'),
    path('dashboard/genres/edit/<int:genre_id>/', views.edit_genre, name='edit_genre'),
    path('dashboard/genres/delete/<int:genre_id>/', views.delete_genre, name='delete_genre'),
    path('view-books/', views.view_books, name='view_books'),
    path('edit-book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('edit_donate_book/<int:book_id>/', views.edit_donate_book, name='edit_donate_book'),
    path('donate/', views.donate_book, name='donate_book'),
    path('dashboard/issue-book/', views.issue_book, name='issue_book'),
    path('ajax/search-books/', views.search_books_ajax, name='search_books_ajax'),
    path('genre/<int:genre_id>/book/<int:pk>/', views.book_detail, name='book_detail'),
    path('dashboard/view_issued_books/', views.view_issued_books, name='view_issued_books'),
    path('dashboard/issue/<int:pk>/toggle-status/', views.update_issue_status, name='update_issue_status'),
    path('dashboard/issue/<int:pk>/delete/', views.delete_issue_record, name='delete_issue_record'),
    
    path('student/issued-books/', views.student_issued_books, name='student_issued_books'),
    path('cancel/<int:issued_book_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('dashboard/send-reply/', views.send_reply, name='send_reply'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete_issue/<int:pk>/', views.delete_issue, name='delete_issue'),
   
    path("api/scan-lookup/", views.scan_lookup, name="scan_lookup"),
    path("api/issue-book/", views.issue_book_api, name="issue_book_api"),
   
    path('fetch-student/', views.fetch_student_by_barcode, name='fetch-student'),
    # path('mark-payment/', views.mark_payment_received, name='mark_payment_received'),
    path("issued/payment/", views.mark_payment_received, name="mark_payment_received"),

    path('cancel_reservation/<int:issued_book_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('canceled-orders/', views.view_canceled_orders, name='view_canceled_orders'),
    path('view-donated-books/', views.view_donated_books, name='view_donated_books'),
    path('dashboard/manage-footer/', views.manage_footer, name='manage_footer'),
    # path('dashboard/edit-library-settings/', views.edit_library_settings, name='edit_library_settings'),
    path('dashboard/settings/', views.edit_library_settings, name='edit_library_settings'),
    path('dashboard/edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('dashboard/send-reply/<int:query_id>/', views.send_reply, name='send_reply'),
    path('manage_course_department/', views.manage_course_department, name='manage_course_department'),
    path("course-department/edit/<int:pk>/", views.edit_course_department, name="edit_course_department"),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    # path('delete-department/<int:id>/', views.delete_department, name='delete_department'),
    path('delete-department/<int:dept_id>/', views.delete_department, name='delete_department'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('return_book/', views.return_book, name='return_book'),
    path('api/scan-lookup/', views.api_scan_lookup, name='api_scan_lookup'),
    path('api/check_issue/', views.api_check_issue, name='api_check_issue'),
    path('ajax/load-departments/', views.load_departments, name='ajax_load_departments'),
    path('check-expiry/', views.check_expiry_and_notify, name='check_expiry'),
    
    path("students/export/", views.export_students_excel, name="export_students_excel"),
    path("issued_books/export/", views.export_issued_books_view, name="export_issued_books_view"),
    path("donated-books/export/", views.export_donated_books, name="export_donated_books"),
 
    path("issued/<int:issued_id>/missing/", views.mark_missing, name="mark_missing"),



    path("dashboard/renew/<int:pk>/", views.admin_renew_book, name="admin_renew_book"),
    # path('holidays/', views.holiday_list, name='holiday_list'),
    # path('holidays/add/', views.add_holiday, name='add_holiday'),
    # path('holidays/delete/<int:pk>/', views.delete_holiday, name='delete_holiday'),
    path("holidays/", views.holiday_list, name="holiday_list"),
    path("holidays/edit/<int:pk>/", views.edit_holiday, name="edit_holiday"),
    path("holidays/delete/<int:pk>/", views.delete_holiday, name="delete_holiday"),
]






