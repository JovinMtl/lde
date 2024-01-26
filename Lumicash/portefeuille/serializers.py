from rest_framework import serializers

from .models import PorteFeuilleClient, LumiClientRequeste


class PorteFeuilleSeria(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PorteFeuilleClient
        fields = '__all__'

class RequesteLumiSeria(serializers.ModelSerializer):
    class Meta:
        model = LumiClientRequeste
        fields = '__all__'