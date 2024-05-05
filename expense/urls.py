
from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/createexpense/', ExpenseCreateView.as_view(), name='createexpense'),
    path('api/updateexpense/', ExpenseUpdateView.as_view(), name='updateexpense'),
    path('api/deleteexpense/<str:id>', ExpenseDeleteView.as_view(), name='deleteexpense'),
    path('api/listspecificexpense/', ExpenseSpecificExpenseView.as_view(), name='listspecificexpense'),
    path('api/listexpense/', ExpenseListView.as_view(), name='listexpense'),
    path('api/graphdata/', GraphDataView.as_view(), name='graphdata'),
    path('api/graphdatedata/', GraphDateDataView.as_view(), name='graphdatedata'),
    path('api/updatebudget/', UpdateBudgetView.as_view(), name='updatebudget'),
    path('api/monthlyexpense/', RetriveMonthlyExpenseView.as_view(), name='monthlyexpense'),
    path('api/categorize/', Categorize.as_view(), name='categorize'),
    path('api/getdebts/', GetDebts.as_view(), name='getdebts'),
    path('api/updatedebts/', UpdateDebts.as_view(), name='updatedebts'),
    path('api/getcategories/', GetCategories.as_view(), name='getcategories'),
    path('api/categorydata/', CategoryData.as_view(), name='categorydata'),
    path('api/pdfextract/', PDFExtract.as_view(), name='pdfextract'),
]
