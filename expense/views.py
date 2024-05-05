from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserModel, Expense
from .serializers import ExpenseSerializer  # Import your ExpenseSerializer

from datetime import datetime
import pytz

from django.conf import settings


import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import requests

from .llmmodel import LLMModel
import json
import time


from .transaction_retriever import pdf_extract


def sendmail(user):
    msg = MIMEMultipart()
    fromaddr = "prathamtestmail10@gmail.com"
    msg['Subject'] = "Budget Limit Exceeded Notification"
    msg['From'] = fromaddr

    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromaddr, "ondgozytpbtlfscu")

    with open('warning-sign.png', 'rb') as f:
        img_data = f.read()

    image = MIMEImage(img_data, name='limit_exceeded.png')
    msg.attach(image)

    current_date = datetime.now().strftime("%Y-%m-%d")
    mail_content = f"""
    <html>
    <body>
        <p><strong>Subject:</strong> Budget Limit Exceeded Notification</p>

        <p>Dear {user.first_name} {user.last_name},</p>

        <p>I hope this message finds you well. We appreciate your continued use of our services and would like to bring to your attention that your budget limit has been exceeded.</p>

        <p><strong>As of {current_date}, your account has surpassed the allocated budget limit of {user.budget}. This may have occurred due to increased usage or additional services that were not accounted for in the initial budget planning.</strong></p>

        <p>To ensure that your services remain uninterrupted, we kindly request that you review your current usage and take necessary actions to bring your account back within the allocated budget.</p>

        <p>We understand that budget management is crucial, and we are here to support you in optimizing your usage and ensuring a seamless experience with our services.</p>

        <p>Thank you for your prompt attention to this matter. We value your partnership and look forward to continuing to serve you.</p>

        <p>Best regards,</p>
        <p>XDesire Team</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(mail_content, 'html'))

    toaddr = [user.email]
    msg['To'] = ", ".join(toaddr)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)

    s.quit()


class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = UserModel.objects.get(username=username, password=password)
            return JsonResponse({"response": "Login successful"}, status=200)
        except Exception as e:
            return JsonResponse({"response": "Invalid credentials"}, status=401)

class RegistrationView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            password = request.data.get('password')
            email = request.data.get('email')
            user = UserModel.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            return JsonResponse({"response": "User has been registered successfully"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"response": str(e)}, status=401)

class ExpenseCreateView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            print(request.body)

            username = request.data.get('username')
            user = UserModel.objects.get(username=username)
            amount = int(request.data.get('amount'))
            text = request.data.get('text')
            transtype = request.data.get('transtype')
            category = request.data.get('category')
            subcategory = request.data.get('subcategory')
            payment_mode = request.data.get('payment_mode')
            

            currmonth =user.currmonth

            current_date = datetime.now()
            current_month_str = int(current_date.strftime("%m"))

            if current_month_str != currmonth:
                user.currmonth = current_month_str
                user.currexpense = 0
                user.save()

            if transtype == "Expense" :
                currexpense = user.currexpense-amount
                user.currexpense = currexpense
                user.save()

            expense = Expense.objects.create(user=user, amount=amount, text=text, category=category, subcategory=subcategory, transtype=transtype, payment_mode=payment_mode)
            expense.save()

            print("expense = ", expense)

            return Response({"response": "Transaction created successfully", "id": expense.id}, status=200)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class ExpenseUpdateView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            id = request.data.get('id')

            username = request.data.get('username')
            user = UserModel.objects.get(username=username)
            amount = int(request.data.get('amount'))
            text = request.data.get('text')
            transtype = request.data.get('transtype')
            category = request.data.get('category')
            subcategory = request.data.get('subcategory')
            payment_mode = request.data.get('payment_mode')

            expense = get_object_or_404(Expense, id=id, user=user)

            expense.amount = amount
            expense.text = text
            expense.transtype = transtype
            expense.category = category
            expense.subcategory = subcategory
            expense.payment_mode = payment_mode

            expense.save()

            return Response({"response": "Transaction updated successfully"}, status=200)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)


class ExpenseDeleteView(APIView):
    @method_decorator(csrf_exempt)
    def delete(self, request, id, *args, **kwargs):
        try:
            expense_instance = Expense.objects.get(id=id)
            expense_instance.delete()
            return Response({"response": "Transaction deleted successfully"}, status=200)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class ExpenseListView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username)

            print(request.data)

            if request.data['type'] != '':
                transtype = request.data['type']


                expenses = Expense.objects.filter(user=user, transtype=transtype)

                

                if expenses:

                    if request.data['sortby'] != '':
                        sortby = request.data.get('sortby')
                        expenses = expenses.order_by(sortby)

                    serializer = ExpenseSerializer(expenses, many=True)
                    serialized_data = serializer.data

                    return Response({"response": serialized_data}, status=status.HTTP_200_OK)
                else:
                    return Response({"response": "No such transactions found."}, status=status.HTTP_404_NOT_FOUND)

            expenses = Expense.objects.filter(user=user)

            print(expenses)

            if expenses:
                if request.data['sortby'] != '':
                    sortby = request.data.get('sortby')
                    expenses = expenses.order_by(sortby)

                serializer = ExpenseSerializer(expenses, many=True)
                serialized_data = serializer.data

            print(serialized_data)

            return Response({"response": serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

        
class ExpenseSpecificExpenseView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')
            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username)

            expenses = Expense.objects.filter(user=user, id=id)
            if expenses:
                serializer = ExpenseSerializer(expenses, many=True)
                serialized_data = serializer.data
            return Response({"response": serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)


class GraphDataView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username)  
            expenses = Expense.objects.filter(user=user)
            sortby = 'date'
            expenses = expenses.order_by(sortby)
            serializer = ExpenseSerializer(expenses, many=True)
            serialized_data = serializer.data

            graphdata = []

            minval = 0
            maxval = 0
            pre = 0

            for data in serialized_data:
                pre+=data['amount']
                minval = min(minval, pre)
                maxval = max(maxval, pre)

                datetime_obj = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

                # Format the datetime object as a string in "YYYY-MM-DD HH:mm:ss" format
                formatted_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


                graphdata.append({
                    "date": formatted_str,
                    "amount": pre
                })

            return Response({"response": graphdata, "minval": minval, "maxval": maxval}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class GraphDateDataView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username)  
            
            specific_date_str = request.data.get('date')
            minval = 0
            maxval = 0
            pre = 0

            if not specific_date_str:
                return Response({"response": "No date selected", "minval": minval, "maxval": maxval}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            timestamp_utc = datetime.strptime(specific_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Define the target timezone (e.g., India Standard Time, IST)
            target_timezone = pytz.timezone('Asia/Kolkata')

            # Convert the UTC datetime object to the target timezone
            timestamp_adjusted = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(target_timezone)

            # Format the adjusted datetime object as a string
            timestamp_adjusted_str = timestamp_adjusted.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            print(timestamp_adjusted_str)
            specific_date = datetime.strptime(timestamp_adjusted_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            expenses = Expense.objects.filter(user=user, date__date=specific_date.date())

            serializer = ExpenseSerializer(expenses, many=True)
            serialized_data = serializer.data

            graphdata = []


            for data in serialized_data:
                pre+=data['amount']
                minval = min(minval, pre)
                maxval = max(maxval, pre)


                datetime_obj = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

                formatted_str = datetime_obj.strftime("%H:%M:%S")


                graphdata.append({
                    "date": formatted_str,
                    "amount": pre
                })

            return Response({"response": graphdata, "minval": minval, "maxval": maxval}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class UpdateBudgetView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            budget = request.data.get('budget') 
            user = get_object_or_404(UserModel, username=username) 
            user.budget = budget
            user.save()
            return Response({"response": "Budget updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class RetriveMonthlyExpenseView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try: 
            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username) 
            expenses = Expense.objects.filter(transtype='Expense')

            currexpense = 0
            current_date = datetime.now()
            current_month_str = int(current_date.strftime("%m"))

            for e in expenses:
                month_str = int(e.date.strftime("%m"))
                if month_str == current_month_str :
                    currexpense+=e.amount
            
            user.currmonth = current_month_str
            user.currexpense = currexpense
            user.save()

            if user.currexpense > user.budget :
                sendmail(user)
            return Response({"currexpense": user.currexpense, "budget": user.budget}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

            
class UpdateBudgetView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            username = request.data.get('username')
            budget = request.data.get('budget') 
            user = get_object_or_404(UserModel, username=username) 
            user.budget = budget
            user.save()
            return Response({"response": "Budget updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class Categorize(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')  

            print("username = ", username)

            llmmodel = LLMModel(str(username))

            print("username = ", username)
            start_time = time.time() 


            expsentence = request.data.get('expsentence')     

            print(expsentence)    
            json_string = llmmodel(expsentence)
            
            end_time = time.time()

            time_taken = end_time -start_time

            print("Time taken: ",time.strftime("%H:%M:%S", time.gmtime(time_taken)))

            response = json.loads(json_string)

            filtered_contributions = [contribution for contribution in response['contributions'] if not any(key.startswith('You') for key in contribution.keys())]

            response['contributions'] = filtered_contributions




            print("categorize: ",response)

            return Response({"response": response}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)


class GetDebts(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username) 

            debts = {}

            for key in user.debts.keys():
                debts[key] = []
                for data in user.debts[key] :
                    trans = Expense.objects.get(id=data["transid"], user=user)
                    debts[key].append({"contri": data["contri"], "date": str(trans.date).split(".")[0], "text": trans.text, "id": trans.id})



            return Response({"response": debts}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)

class UpdateDebts(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')
            update = request.data.get('update')
            user = get_object_or_404(UserModel, username=username) 

            contributor = request.data.get('contributor')
            contri = request.data.get('contri')

            print(contri)

            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


            if update == "True" :
                for debt in user.debts.get(contributor, []):
                    if debt.get("transid") == contri["transid"]:
                        debt["contri"] = contri["contri"]
                        break
            else: 
                if contributor not in user.debts: 
                    user.debts[contributor] = [contri]
                else :
                    user.debts[contributor].append(contri)

                    
            user.save()

            return Response({"response": user.debts}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)


class GetCategories(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username) 
            expenses = Expense.objects.filter(user=user)
            
            categories = set()

            for expense in expenses:
                categories.add(expense.category)

            return Response({"response": list(categories)}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)
class CategoryData(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username) 

            category = request.data.get('category')

            expenses = Expense.objects.filter(user=user, category=category)

            totalamount = 0

            subcagegoriesratio = {}

            if expenses:

                serializer = ExpenseSerializer(expenses, many=True)
                serialized_data = serializer.data

                for data in serialized_data :
                    subcagegoriesratio[data["subcategory"]] = data["amount"]
                    totalamount += data["amount"]

            for key in subcagegoriesratio.keys() :
                subcagegoriesratio[key]=subcagegoriesratio[key]/totalamount*100
            


            return Response({"response": subcagegoriesratio}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"response": str(e)}, status=401)


class PDFExtract(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:

            username = request.data.get('username')
            user = get_object_or_404(UserModel, username=username) 

            uploaded_file = request.FILES.get("file")


            media_directory = os.path.join(settings.BASE_DIR,'static')
            os.makedirs(media_directory, exist_ok=True)

            file_path = os.path.join(media_directory, uploaded_file.name)
            print("File uploaded at ",file_path)

            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            data = pdf_extract(file_path) 

            print(data) 
        
            return Response({"response": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            print(e)
            return Response({"response": str(e)}, status=401)
