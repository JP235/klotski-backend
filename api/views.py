from django.forms import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from game.serializers import *
from game.models import *
from utils.image_gud_utils import get_ContentFile_from_b64_image


class UserAPIView(generics.RetrieveAPIView):
    """User API View"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    """Register API View"""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """"""
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(generics.GenericAPIView):
    """Login API View"""
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            },
            status=status.HTTP_200_OK,
        )


class GameKlotskiList(generics.ListAPIView):
    """
    API endpoint to view games by logged-in user
    """

    serializer_class = GameSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return self.request.user.owned.all()

class GameKlotskiListOpen(generics.ListAPIView):
    serializer_class = GameSerializer
    def get_queryset(self):
        return GameKlotski.objects.filter(private=False, solved=False)


class GameView(APIView):
    """
    Main game view
    """

    game_serializer = GameSerializer
    block_serializer = BlockSerializer
    move_serializer = MoveSerializer

    def get(self, request, game_code=None, game_pk=None):
        if game_code:
            game = GameKlotski.get_by_code(game_code)
        elif game_pk:
            game = GameKlotski.get_by_id(game_pk)

        if game.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        blocks = game.game_blocks.all()
        moves = game.moves.all()
        game_serial = self.game_serializer(game)
        block_serial = self.block_serializer(blocks, many=True)
        move_serial = self.move_serializer(moves, many=True)

        return_data = {
            "game": game_serial.data,
            "blocks": block_serial.data,
            "moves": move_serial.data,
        }

        return Response(return_data, status=status.HTTP_200_OK)

    def put(self, request, game_code=None, game_pk=None):
        data_game = request.data["game"]
        if data_game["code"] == "classic":
            return self.post(request)

        # # Propperly saving images from base64 canvas URI is hard
        data_game["img_curr"] = get_ContentFile_from_b64_image(data_game["img_curr"])
        data_game["img_win"] = get_ContentFile_from_b64_image(data_game["img_win"])

        game_serial = self.game_serializer(data=data_game)
        blocks_serial = self.block_serializer(data=request.data["blocks"], many=True)
        moves_serial = self.move_serializer(data=request.data["moves"], many=True)

        if (
            game_serial.is_valid()
            and blocks_serial.is_valid()
            and moves_serial.is_valid()
        ):
            game = GameKlotski.get_by_code(game_serial.data.get("code"))
            if game.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            ### TODO: Wrap in try/except and revert moves if error
            game.number_of_moves = game_serial.data.get("number_of_moves")
            game.img_curr = game_serial.data.get("img_curr")
            for block in blocks_serial.data:
                bl = GameBlock.objects.filter(game=block["game"], name=block["name"])[0]
                bl.move(block["x"], block["y"])

            game_moves = game.moves.all()

            game.save(update_fields=["number_of_moves", "img_curr"])
            game_moves.delete()
            moves_serial.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            # print()
            # print("game_serial.errors", game_serial.errors)
            # print()
            # print("blocks_serial.errors", blocks_serial.errors)
            # print()
            # print("moves_serial.errors", moves_serial.errors)
            # print()
            return Response(game_serial.errors,status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, game_code=None, game_pk=None):
        data_game = request.data["game"]

        # Propperly saving images from base64 canvas URI is hard
        data_game["img_curr"] = get_ContentFile_from_b64_image(data_game["img_curr"])
        data_game["img_win"] = get_ContentFile_from_b64_image(data_game["img_win"])

        game_serial = self.game_serializer(data=data_game)
        blocks_serial = self.block_serializer(data=request.data["blocks"], many=True)

        if game_serial.is_valid() and blocks_serial.is_valid():
            new_game = GameKlotski(
                owner = request.user,
                cols = game_serial.data.get("cols"),
                rows = game_serial.data.get("rows"),
                img_curr = InMemoryUploadedFile(data_game["img_curr"], None, None, None, None, None),
                img_win = InMemoryUploadedFile(data_game["img_win"], None, None, None, None, None),)

            new_game.set_win_condition(
                game_serial.data.get("win_block_x"), game_serial.data.get("win_block_y")
            )
            for block in blocks_serial.data:
                new_block = GameBlock(
                    name=block["name"],
                    h=block["h"],
                    l=block["l"],
                    x=block["x"],
                    y=block["y"],
                )
                new_block.add_to_game(game=new_game, new=True)

            return Response(
                data={"game": self.game_serializer(new_game).data,},
                status=status.HTTP_201_CREATED,
            )
        else:
            # print()
            print("game_serial.errors", game_serial.errors)
            # print()
            print("blocks_serial.errors", blocks_serial.errors)
            # print()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, game_code=None, game_pk=None):
        if game_code:
            game = GameKlotski.get_by_code(game_code)
        elif game_pk:
            game = GameKlotski.get_by_id(game_pk)

        if game.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # print("DELETE", game.code)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
