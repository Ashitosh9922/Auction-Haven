from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("category/", views.categories, name="categories"),
    path("category/<str:category>/", views.category, name="category"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("your_listings/", views.your_listings, name="your_listings"),
    path("won_listings/", views.won_listings, name="won_listings"),
    path("watch_list/", views.watch_list, name="watch_list"),
    path("listing/<int:listing_id>/", views.view_listing, name="listing"),
    path("listing/<int:listing_id>/watch/", views.watch, name="watch"),
    path("listing/<int:listing_id>/close/", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/bid/", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment/", views.comment, name="comment"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.password_reset_success, name='password_reset_success'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/password/', views.edit_password, name='edit_password'),
    path('admin-dashboard/', views.admin_view, name='admin_view'),
    path("admin-dashboard/manage-users", views.manage_users, name="manage_users"),
    path("admin-dashboard/manage-lisitngs", views.manage_listings, name="manage_listings"),
    path('deactivate_listing/<int:listing_id>/', views.deactivate_listing, name='deactivate_listing'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path("admin-dashboard/reports", views.reports, name="reports"),
    path('forbidden/', views.forbidden_view, name='forbidden'),
    # Include API URLs
    path('api/', include('auctions.api_urls')),
    

]





