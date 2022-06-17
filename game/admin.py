from django.contrib import admin
from .models import GameKlotski,GameBlock,Move

# Register your models here.

admin.site.register(GameKlotski)
admin.site.register(GameBlock)
admin.site.register(Move)

