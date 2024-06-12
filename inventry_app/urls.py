from django . urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
# ...........suppliier urls.........
    
    path('supplier/', views.supplier, name="supplier_mast"),
    path('supplier/edit/<int:id>/', views.edit_supplier, name='edit_supplier'),
    path('supplier/delete/<int:id>/', views.delete_supplier, name='delete_supplier'),

#....... items ........

    path('items/', views.items, name="items"),
    path('items/edit_item/<int:id>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:id>/', views.delete_items, name='delete_items'),

#......Purchase............

    path('purchase/', views.purchase,name="temp_purchase"),
    path('purchase/price/', views.get_item_price,name="price"),
    path('purchase/purchase_details/', views.purchase_details,name="purchase_details"),
    
#...........sale.............

path('sale/',views.sale_mast,name="sale_mast"),
path('sale/sale-details',views.sale_details,name="sale_details"),

#...........report.............
path('purchase_report/',views.purchase_report, name="purchase_report"),
path('sale_report/',views.sale_report, name="sale_report"),
path('stock_report/',views.stock_report, name="stock_report"),


]
