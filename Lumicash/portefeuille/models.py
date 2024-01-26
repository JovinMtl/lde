from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class PorteFeuilleClient(models.Model):
    owner_name = models.CharField(max_length=15)
    owner_obj = models.ForeignKey(User, on_delete=models.CASCADE)
    #on phone number, we'll check the first 3 char starting if \
    #it's length is superior to 9 or 10
    owner_phone_number = models.CharField(max_length=15)
    solde = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.owner_phone_number} ==> {self.owner_obj} ==> \
            {self.solde}"

stages = (
    (1, 'PENDING'),
    (2, 'DONE'),
)

class LumiClientRequeste(models.Model):
    owner = models.ForeignKey(PorteFeuilleClient,\
                               on_delete=models.CASCADE,\
                            related_name='owned_lumi_client_requestes')
    benefitor = models.ForeignKey(PorteFeuilleClient,\
                               on_delete=models.CASCADE,\
                        related_name='benefiting_lumi_client_requestes')
    amount_to_transact = models.IntegerField(default=0)
    date_requested = models.DateTimeField(default=datetime.now())
    date_approved = models.DateTimeField(default=datetime.now())
    stage_progress = models.IntegerField(choices=stages, default=1)
    link_activate = models.URLField(\
        default="http://127.0.0.1:8000/power/log/")
    code_transaction = models.CharField(max_length=15,default="xx")
    
    class Meta:
        verbose_name = "IGisabo"
        verbose_name_plural = "IBisabo"
