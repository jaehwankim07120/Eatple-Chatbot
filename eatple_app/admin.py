'''
    Author : Ben Kim

    @NOTE
    @BUG
    @TODO
 
'''
# Django Library
from django.contrib import admin

# Models
from .models import DefaultImage
from .models import UserManual, PartnerManual
from .models import UserIntro, PartnerIntro
from .models import Store, Menu
from .models import Category, SubCategory
from .models import Order
from .models import User, UserFlags
from .models import Partner

class PersonAdmin(admin.ModelAdmin):
    pass

# Main Models
admin.site.register(Partner)
admin.site.register(User)
admin.site.register(UserFlags)

admin.site.register(Store)
admin.site.register(Menu)

# Defulat Images
admin.site.register(DefaultImage)

# Order
admin.site.register(Order)

# Menu Category-SubCategory
admin.site.register(Category)
admin.site.register(SubCategory)

# Manual
admin.site.register(UserManual)
admin.site.register(PartnerManual)

# Intro
admin.site.register(UserIntro)
admin.site.register(PartnerIntro)