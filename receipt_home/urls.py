from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'receipt_home'

urlpatterns = [
    path("", views.print_home, name="print_home"),
    path("history/", views.history_view, name="history_view"),
    path("add-product/", views.add_catalog, name="add_catalog"),    
    path("ajax/add-product/", views.add_catalog_ajax, name="add_catalog_ajax"),    
    path("ajax/add-drug/", views.add_drug_ajax, name="add_drug_ajax"),    
    path("ajax/update-drug/", views.update_drug_ajax, name="update_drug_ajax"),    
    path("ajax/delete-drug/", views.delete_drug_ajax, name="delete_drug_ajax"),    
    path("ajax/search-drug/", views.search_drug_ajax, name="search_drug_ajax"),    
    path("ajax/search-drug", views.search_drug_test_ajax, name="search_drug_test_ajax"),    
    path("ajax/export-and-print", views.export_and_print, name="export_and_print"),    
    path("ajax/search-drug-add-cart/", views.search_drug_prescription_ajax, name="search_drug_prescription_ajax"),    
    path("ajax/search-prescription/", views.search_prescription_ajax, name="search_prescription_ajax"),    
    path("ajax/search-drug-query/", views.search_textbox_drug_table_ajax, name="search_textbox_drug_table_ajax"),    
    path("ajax/history-table-ajax", views.history_table_ajax, name="history_table_ajax"),    
    path("ajax/export-table-xml-ajax", views.export_to_xml, name="export_to_xml"),    
    path("ajax/search-drug-table", views.search_drug_table_ajax, name="search_drug_table_ajax"),    
    path("ajax/search-textbox-drug-test-ajax", views.search_textbox_drug_test_ajax, name="search_textbox_drug_test_ajax"),    
    path("ajax/get-drugs-via-prescription-ajax/", views.get_drugs_via_prescription_ajax, name="get_drugs_via_prescription_ajax"),    
    path("ajax/delete-prescription-via-ajax/", views.delete_prescription_via_ajax, name="delete_prescription_via_ajax"),    
    path("ajax/get-drugs-via-prescription-ajax", views.search_drug_table_pagination_ajax, name="search_drug_table_pagination_ajax"),    

]