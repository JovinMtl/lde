from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.db.models.query import QuerySet.DoesNotExist
from datetime import datetime

from ..serializers import RequeSeria
from ..models import Requeste, PorteFeuille, Recharge

from ..lumi.client_Lumi import LumiRequest 
from ..lumi.login import UserBrowising
from .code_transanction import GenerateCode




class RequeWithdrwawViewSet(viewsets.ViewSet):
    """This is for Managing the Requestes"""
    company_portefeuille = PorteFeuille.objects.get(\
        owner_username='muteule')
  
    def list(self, request):
        """For listing all available requestes"""
        queryset = Requeste.objects.filter(state_progress__lte=1)
        # queryset = Requeste.objects.all()
        serializer_class = RequeSeria(queryset, many=True)
        return Response(serializer_class.data)
    
    def create(self, request):
        """For creating new requestes"""
        data_sent = request.data
        link = "no link"
        user_agent = request.META.get('HTTP_USER_AGENT')
        username = data_sent['username']
        user_password = data_sent['password']
        auth = authenticate(request, username=username,\
                             password=user_password)
        if not data_sent['amount_to_deb'] and (data_sent['amount_to_send'] and auth):
            #requesting to get fund
            user = User.objects.get(username=username)
            print(f"You last logged in at: {auth}")
            new_request = Requeste.objects.create(user_id=user)
            new_request.amount_to_send = data_sent['amount_to_send']
            new_request.receiver_number = data_sent['receiver_number']
            # new_request.user_id = user
            new_request.user_username = user.username
            new_request.state_progress = 1
            url = f"http://127.0.0.1:8002/jov/api/reque//{new_request.id}/approve/"
            new_request.link_to_activate = url
            request_serializer = RequeSeria(new_request, context={'request': request})
            if request_serializer.is_valid:
                print("You are ready to go")
                new_request.save()
                return Response(request_serializer.data)

            print(f"Your request is about:\n{new_request.amount_t_cred}")
            return JsonResponse({"You are authenticated": username})
        if data_sent['amount_to_deb'] and auth:
            #user wants to upload to Lde
            #requesting to withdraw to lumicash
            # lumi = LumiRequest()
            code = GenerateCode()
            code_transaction = code.generate('recharge')
            amount_to_deb = data_sent['amount_to_deb']
            print(f"You are about to use code:  {code_transaction}")
            new_recharge = Recharge.objects.create(\
                owner=auth, phone=data_sent['number_to_deb'],\
                amount=amount_to_deb,
                code_transaction=code_transaction)
            lumi = UserBrowising(\
                amount_to_send=amount_to_deb\
                    ,user_to_pay=data_sent['number_to_deb'],
                    code_transaction=code_transaction)
            response = lumi.askFund()
            # print(f"From Lumicash : {response.json()}")
            if response.status_code == 200:
                new_recharge.save()
                link = response.json().get('link_activate')
                benefitor_portefeuille = PorteFeuille.objects.get(\
                    owner=auth)
                # print(f"\nCelui ci: {benefitor_portefeuille} aura argent\n")
                
            return JsonResponse({f"Hello '{username.upper()}', Your request is waiting for your \
approval. please copythe link below and paste it in the browser to finish":\
                                  link })
    
    def _retranche(self, source, destination, amount, pay_method=1):
        """THis function retrieves the amount """
        if pay_method == 1:
            #lumicash
            if int(source.lumicash) >= int(amount):
                print(f"La source au Debut: {source.lumicash}")
                source.lumicash -= int(amount)
                destination.lumicash += int(amount)
                source.save()
                destination.save()
                print(f"La source a la Fin: {source.lumicash}")
                response = {
                    'code_status': 200,
                    'source' : source,
                    'destination': destination,
                }
                return response
            else:
                return 201
        if pay_method == 2:
            #paypal
            source.paypal -= amount
        if pay_method == 3:
            #enoti
            source.enoti -= amount
        #saving the state of compte
        source.save()
        response = {
                    'code_returned': 200,
                    'amount_found': source.lumicash,
                    'amount_retrieve': amount
                }
        return response
    
    @action(methods=['get'], detail=True)
    def approve(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({"You need to authenticate": "first"})
        obj = Requeste.objects.get(pk=pk)
        if obj.state_progress > 1 :
            return JsonResponse({"THis link has expired": "Please"})
        sender = obj.user_username
        try:
            sender_portefeuille = \
            PorteFeuille.objects.get(owner_username=sender)
            company_portefeuille = \
            PorteFeuille.objects.get(owner_username='muteule')
        except PorteFeuille.DoesNotExist:
            return JsonResponse({f"{sender}":f"n'a pas de portefeuille"})
        else:
            print(f"The portefeuille found: {sender_portefeuille}")
            #hageze ko tuyakura kuri portefeuille yiwe
        response_retranche = self._retranche(sender_portefeuille,\
                                              obj.amount_to_send,\
                                            company_portefeuille,\
                                                  obj.pay_method,\
                                            )
        if response_retranche == 200:
            print(f"La reponse est : {response_retranche}")
            return JsonResponse({f"Le solde de {sender}":"a ete touche"})
        elif response_retranche == 201:
            return JsonResponse({f"{sender}":"n'a pas de balance suffisant"})
        obj.date_approved = datetime.now()
        obj.state_progress = 2
        obj.approved_by = str(request.user)
        lumi = LumiRequest(obj.receiver_number, obj.amount_to_send)
        transfer_response = lumi.mySolde('transfer')
        if transfer_response.status_code == 200:
            obj.save()
        obj_serializer = RequeSeria(obj)
        if obj_serializer.is_valid:
            print(f"The user who activates is : {request.user.is_authenticated}")
            print(f"From Lumicash: {transfer_response}")
            return Response(obj_serializer.data)
        print(f"The obj to work on is : {pk}")
        return JsonResponse({"Hello": "username"})
    
    @action(methods=['post'], detail=False)
    def answer(self, request):
        """Receive the feedback from the server after the 
        approval of fund payment made by the owner.
        
        will receive the phone number sent to debit, the amount, and
        the status code(25 if it were successfully).
        The we call the self._retranche() function to do accordingly in
        the local Portefeuille."""

        data_sent = request.POST
        phone = data_sent['phone_number']
        code_transaction = data_sent['code_transaction']
        amount = data_sent['amount']
        try:
            obj = Recharge.objects.get(code_transaction=code_transaction)
        except Recharge.DoesNotExist:
            return JsonResponse({"The Transaction code ":"Does match"})
        else:
            benefitor_portefeuille = PorteFeuille.objects.get(\
                owner=obj.owner)
            operation = self._retranche(self.company_portefeuille,\
                            benefitor_portefeuille, obj.amount)
            if operation['code_status'] == 200:
                print(f"{operation['source'].owner} diminue :\
{operation['source'].lumicash}")
                print(f"{operation['destination'].owner} augmente  :\
{operation['destination'].lumicash}")

            # print("The approval feedback has come from Lumicash")
            print(f"{phone}, code: {code_transaction}")
        return JsonResponse({"Server 1":"has received a reply"})
          



def check_len_REST(func):
    """I want to chech the arguments of the function that
    their username is longer than 6 caracters"""
    def inner(*args, **kwargs):
        result = HttpResponse("Maybe your password is short")
        if len (args[1].data['password']) > 6:
            result = func(*args, **kwargs)
            print(f"The username is : {args[1].data}\n\n\
                  and Result: {result}")
            return result
        else:
            print(f"The length of password is \
                  {len(args[1].data['username'])}")
            return result
    return inner



class ManageUser(APIView):
    """This is for retrieving and creating users"""
    def get(self, request):
        """THis is to view the users we have"""
        data = User.objects.all()
        data = UserSeriazer(data, many=True)
        return Response(data.data)

    @check_len_REST
    def post(self, request):
        """This is when we want to add a new user"""
        sent_data = request.POST
        username = sent_data['username']
        password = sent_data['password']
        new_user = User.objects.create(username=username)
        new_user.set_password(password)
        new_portefeuille = PorteFeuille.objects.create(\
            owner = new_user)
        new_portefeuille.owner_username = new_user.username
        new_user_seriazer = UserSeriazer(new_user)
        new_porte_seriazer = PorteSeria(new_portefeuille)
        if new_user_seriazer.is_valid and new_porte_seriazer.is_valid:
            new_user.save()
            new_portefeuille.save()
            print("All is Okay")
            data = {
                'user': new_user_seriazer.data,
                'portefeuille': new_porte_seriazer.data,
            }
        return Response(data)
        
 