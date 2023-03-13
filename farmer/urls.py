from django.urls import path 
from .import views 

urlpatterns = [
    path("StartFarm",views.StartFarm,name="StartFarm"),
    path("AddNewSeedFarm",views.AddNewSeedFarm,name="AddNewSeedFarm"),
    path("FramStatusUpdate/<str:pk>",views.FramStatusUpdate,name="FramStatusUpdate"),
    path("DeleteOpinion/<str:pk><str:hk>",views.DeleteOpinion,name="DeleteOpinion"),
    path("UpdateAnswer/<str:pk>",views.UpdateAnswer,name="UpdateAnswer"),
    path("FarmProducts",views.FarmProducts,name="FarmProducts"),
    path("ProductSignleView/<int:pk>",views.ProductSignleView,name="ProductSignleView"),
    path("FarmerMybooking",views.FarmerMybooking,name="FarmerMybooking"),
    path("MyProducts",views.MyProducts,name="MyProducts"),
    path("CancelOrderFarmer/<int:pk>",views.CancelOrderFarmer,name="CancelOrderFarmer"),
    path("DeleteOrderFarmer/<int:pk>",views.DeleteOrderFarmer,name="DeleteOrderFarmer"),
    path("CustomerView/<int:pk>",views.CustomerView,name="CustomerView"),
    path("MakePayment/<int:pk>",views.MakePayment,name="MakePayment"),
    path('MakePayment/paymenthandler', views.paymenthandler, name='MakePayment/paymenthandler'),
    path("Success",views.Success,name="Success")
    
    
]
