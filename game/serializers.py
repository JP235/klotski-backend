from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from .models import *
from utils.move_delts_convert import delts_to_move, move_to_delts


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBlock
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameKlotski
        fields = "__all__"

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        
        try:
            # Propperly saving images from base64 canvas URI is hard
            # only for PUT requests, update img_curr
            img_name = f'{data["code"]}{instance["img_curr"].name}'
            data['img_curr'] = InMemoryUploadedFile(instance["img_curr"],None, img_name, None, None, None, None)
            
        except TypeError:
            # GET POST Request
            pass
        except KeyError:
            # POST Request
            pass

        return data
    def to_internal_value(self, data):
        data["img_curr"] = None
        data["img_win"] = None
        return super().to_internal_value(data)

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data_out = {}
        data_out["deltX"],data_out["deltY"] = move_to_delts(data["move"])
        data_out["targetBlock"] = GameBlock.objects.filter(id=data["block"])[0].name
        data_out["game"] = data["game"]

        return data_out

    def to_internal_value(self, data):
        move = delts_to_move(data["deltX"], data["deltY"])
        block = GameBlock.objects.filter(game=data["game"], name=data["targetBlock"])[0]
        game = GameKlotski.objects.filter(id=data["game"])[0]
        instance = {"move":move,"block":block, "game":game}
        # d = super().to_representation(instance)

        return instance