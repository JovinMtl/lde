from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .serializers import PorteFeuilleSeria, RequesteLumiSeria
from .models import PorteFeuilleClient, LumiClientRequeste
from .response import Answer

import functools


# Create your views here.

def checki(func):
    """this function checks that if it is the owner of the ressource 
     that wishes to execute the action """
    result = HttpResponse("Hello world")

    @functools.wraps(func)
    def inner(*args, **kwargs):
        link = str(args[1])
        requester = str(args[1].user)
        # print(f"The link is {link}")
        try:
            id = int(link.split('/')[2])
        except ValueError:
            return HttpResponse("Your link is inappropriate")
            
        reque = LumiClientRequeste.objects.get(pk=id)
        result = HttpResponse(f"You must be: {reque.owner} : \
                              in order to have this ressource.\
                    <a>Want to login ?</a>")
        if reque.owner.owner_name == requester:
            result = func(*args, **kwargs)
            return result
        
        return result
    return inner



class Power(viewsets.ViewSet):
    """This class is responsible for moving fund in 
    different entries across 'PorteFeuileClient'
    """

    @action(detail=False, methods=['post','get'])
    def solde(self, request):
        """Is GET only"""
        data_sent = request.data
        req_user = data_sent['owner_name']
        req_user_pass = data_sent['password']
        user = authenticate(username=req_user, password=req_user_pass)
        print(f"You have sent: {data_sent}")
        print(f"\nYour status is : {user} with ID:{user.id}")
        if user:
            sender = PorteFeuilleClient.objects.get(pk=user.id)
            sender_serializer = PorteFeuilleSeria(sender)
            # receiver_number = data_sent['receiver_number']
            # receiver_obj = PorteFeuilleClient.objects.get(\
                # owner_phone_number__exact=receiver_number)
            # print(f"You are about to transfer to {receiver_obj}")
            if sender_serializer.is_valid:
                print(f"You are about to see your money")
                return Response(sender_serializer.data)

        id_sender = 4
        return JsonResponse({"The id Sent is :": id_sender})
    
    def _finish(self, source, destination, montant):
        if int(source.solde) >= int(montant):
            source.solde -= int(montant)
            destination.solde += int(montant)
            source.stage_progress = 2
            destination.stage_progress = 2
            source.save()
            destination.save()
            print(f"La source a le solde de : {source.solde}")
            return source.stage_progress
        elif int(montant) > int(source.solde):
            return 0

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        data_sent = request.data
        req_user = data_sent['owner_name']
        req_user_pass = data_sent['password']
        user = authenticate(username=req_user, password=req_user_pass)
        print(f"You have sent: {data_sent}")
        print(f"\nYour status is : {user} with ID:{user.id}")
        if user:
            sender = PorteFeuilleClient.objects.get(pk=user.id)
            receiver_number = data_sent['receiver_number']
            receiver = PorteFeuilleClient.objects.get(\
                owner_phone_number__exact=receiver_number)
            print(f"You are about to transfer to {receiver}")
            self._finish(sender, receiver, data_sent['amount_to_send'])
            sender_serializer = PorteFeuilleSeria(sender)
            receiver_serializer = PorteFeuilleSeria(receiver)
            if sender_serializer.is_valid and \
                receiver_serializer.is_valid:
                data = {
                    "sender": sender_serializer.data,
                    "receiver": receiver_serializer.data,
                }
                return Response(data)

        return JsonResponse({"You are about to Transfer :":"Funds"})
    
    
    @action(detail=False, methods=['post'])
    def give_not_owner(self, request):
        result = HttpResponse("Not knowing what to say")
        data_sent = request.data
        #preparing the destination to make request for approval
        number_to_retrieve = data_sent['debtor_number']
        amount_to_pay = int(data_sent['amount_to_pay'])
        #now authenticating the one who asks to be paid
        user_to_be_paid = data_sent['username']
        #get his password
        user_to_be_paid_password = data_sent['password']
        user_verified = authenticate(username=user_to_be_paid, \
                                     password=user_to_be_paid_password)
        if user_verified:
            user_to_pay = PorteFeuilleClient.objects.get(\
                owner_phone_number=number_to_retrieve)
            benefitor = PorteFeuilleClient.objects.get(\
                owner_name=user_to_be_paid)
            new_request = LumiClientRequeste.objects.create(\
                owner=user_to_pay, benefitor=benefitor)
            print(f"The user to pay is {user_to_pay}")
            new_request.amount_to_transact = amount_to_pay
            new_request.code_transaction = data_sent['code_transaction']
            new_request.link_activate = \
                f"http://127.0.0.1:8000/power/{new_request.id}/activate"
            new_request_serializer = RequesteLumiSeria(new_request)
            if new_request_serializer.is_valid:
                print(f"Your request is waiting for approval \
                      with code: {data_sent['code_transaction']}")
                new_request.save()
                return Response(new_request_serializer.data)

        else:
            return JsonResponse({f"The user : {user_to_be_paid}":\
                                 "is not matched"})
        return JsonResponse({"The user is not :":f"{user_verified}"})
    
    
    @action(detail=True, methods=['get'])
    @checki
    def activate(self, request, pk):
        docstring = f"When you click on one of these links to Activate, \
            Your Funds will move from you to the Benefitor account. \
                \nAre you sure you want to do this?"
        Power.__doc__ = docstring
        obj = LumiClientRequeste.objects.get(pk=pk)
        if obj:
            response = self._finish(obj.owner, \
                                    obj.benefitor, obj.amount_to_transact)
            print(f"La reponse de transaction est: {response}")
            if response == 2:
                obj.stage_progress = 2
                obj.save()
                answer = Answer(obj.owner.owner_phone_number,\
                                obj.amount_to_transact,
                                status_code=25,\
                                code_transaction=obj.code_transaction)
                feedback = answer.reply()
                if feedback == 25:
                    print("The confirmation answer has been sent")
                else:
                    print("The Reply wasn't sent")
            elif response == 0:
                return JsonResponse({"You do not have":"sufficient fund"})
            obj_serialiser = RequesteLumiSeria(obj)
            return redirect('home')
            # return Response(obj_serialiser.data)

        return HttpResponse("THe obj not found")



class ViewReque(APIView):
    """This is for your benefit"""
    def get(self, request):
        """This is for our benefit"""
        user_agent = request.META.get('HTTP_USER_AGENT')
        user = request.user
        user_reque = LumiClientRequeste.objects.filter(\
            owner__owner_name=user).filter(stage_progress__lte=1)
        reque_serializer = RequesteLumiSeria(user_reque, many=True)
        if user_reque and reque_serializer.is_valid:
            # print(f"You are right, {user} with : {user_reque}")
            docstring = "These awaiting Transactions \
                are AGAINST your benefit"
            ViewReque.__doc__ = docstring

            # print(f"You made this request from Terminal: {user_agent}")
            return Response(reque_serializer.data)
        if not user_reque:
            my_reque = LumiClientRequeste.objects.filter(\
                benefitor__owner_name=user)
            reque_serializer = RequesteLumiSeria(my_reque, many=True)
            docstring = "These awaiting Transactions are for your benefit"
            ViewReque.__doc__ = docstring
            if reque_serializer.is_valid:
                # print(f"You made this request from Terminal: {user_agent}")
                return Response(reque_serializer.data)

