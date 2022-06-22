import json
import logging

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save

from utils.game_board import make_game_board
from utils.constants import MOVES, UP, WIN_NAME
from utils.image_gud_utils import (
    file_path_curr,
    file_path_win,
    update_game_img,
    delete_game_img,
)

from utils.code_gen import generate_unique_code
from solver import *


class GameKlotski(models.Model):
    """
    Represents a game of Klotski
    """

    owner = models.ForeignKey(
        User, related_name="owned", on_delete=models.CASCADE, null=True
    )
    code = models.CharField(max_length=8, default=generate_unique_code)

    cols = models.IntegerField(default=4)
    rows = models.IntegerField(default=5)

    win_block_x = models.IntegerField(null=True, blank=True)
    win_block_y = models.IntegerField(null=True, blank=True)
    wcset = models.BooleanField(default=False)

    # img_curr = models.ImageField(upload_to=file_path_curr, null=True, blank=True)
    # img_win = models.ImageField(upload_to=file_path_win, null=True, blank=True)

    # dates
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solved = models.DateTimeField(null=True, blank=True)

    number_of_moves = models.IntegerField(default=0)
    auto_solved = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.code}\n {make_game_board(self, board_only=True)}"

    def get_all_blocks(self):
        """
        Gets all of the squares for this Game
        """
        return GameBlock.objects.filter(game=self)

    def get_moves(self):
        return self.moves.order_by("-id")
    

    def get_block_by_name(self, block_name):
        """
        Gets a block for a game by it's name
        """
        return GameBlock.objects.get(game=self, name=block_name)

    def get_win_block(self):
        """
        Gets a block for a game by it's name
        """
        return self.get_block_by_name(WIN_NAME)

    def get_block_by_pos(self, x, y):
        """
        Gets a block for a game in x and y pos
        """
        try:
            blocks = self.get_all_blocks()
            for block in blocks:
                if (x, y) in block.coords:
                    return block
            else:
                return None
        except ValueError:
            return None

    def set_win_condition(self, x, y):
        """
        Sets win condition
        """
        self.wcset = True
        self.win_block_x = x
        self.win_block_y = y

        self.save()

    def win_condition(self):
        if self.wcset:
            wb = self.get_win_block()
            if wb.x == self.win_block_x and wb.y == self.win_block_y:
                self.mark_solved()
                return True
        return False

    def mark_solved(self):
        """
        Sets a game to completed status 
        """
        print("Solved!", self.code)
        self.solved = timezone.now()
        self.save(update_fields=["solved"])

    def get_unfinished_games(self):
        return GameKlotski.objects.filter(game=self, solved=None)

    @staticmethod
    def get_all_unfinished_games():
        return GameKlotski.objects.filter(solved=None)

    @staticmethod
    def get_by_code(code):
        return GameKlotski.objects.get(code=code)

    @staticmethod
    def get_by_id(id):
        return GameKlotski.objects.get(pk=id)


# post_delete.connect(delete_game_img, sender=GameKlotski)
# pre_save.connect(update_game_img, sender=GameKlotski)


class GameBlock(models.Model):

    game = models.ForeignKey(
        GameKlotski,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="game_blocks",
    )
    name = models.CharField(max_length=2)

    # block height and lenght
    h = models.IntegerField()
    l = models.IntegerField()

    # upper left coord
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.coords}"

    @property
    def coords(self):
        return [
            (self.x + i // self.l, self.y + i % self.l) for i in range(self.h * self.l)
        ]

    def add_to_game(self, game, new=False):
        board_coords = [False for x in range(game.cols) for y in range(game.rows)]
        for c in self.coords:
            board_coords[c[0] * game.cols + c[1]] = True

        for block in game.get_all_blocks():
            for coord in block.coords:
                if board_coords[coord[0] * game.cols + coord[1]] == True:
                    raise ValueError(f"Block {self.name=} {self.pk=} overlaps")
                else:
                    board_coords[coord[0] * game.cols + coord[1]] = True

        self.game = game
        if new:
            self.save()
        else:
            self.save(update_fields=["game"])

    def move(self, x, y):
        """
        Move block
        """
        self.x = x
        self.y = y

        self.save(update_fields=["x", "y"])

        if self.game.win_condition():
            self.game.mark_solved()


class Move(models.Model):

    move = models.CharField(max_length=5, choices=MOVES, default=UP)

    game = models.ForeignKey(
        GameKlotski,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="moves",
    )
    block = models.ForeignKey(
        GameBlock,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="block_moves",
    )

    def __str__(self) -> str:
        return f"{self.game.code} - {self.block.name} {self.move} "

