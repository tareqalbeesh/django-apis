from django.urls import path
from . import views
urlpatterns = [path('menu-items/', views.MenuItemView.as_view()),
               path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
               path('groups/manager/users', views.ManagerView.as_view()),
               path('groups/manager/users/<int:pk>',
                    views.SingleManagerView.as_view()),
               path('groups/delivery-crew/users',
                    views.DeliveryCrewView.as_view()),
               path('groups/delivery-crew/users/<int:pk>',
                    views.SingleDeliveryCrewView.as_view()),
               path('cart/menu-items/', views.CartView.as_view()),
               path('orders/', views.OrderView.as_view()),
               path('orders/<int:pk>', views.SingleOrderView.as_view()),

               ]
