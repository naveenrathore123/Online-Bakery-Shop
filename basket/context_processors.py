# This file is running every time, because we are registered this file in the setting.py file. 
from .basket import Basket

def basket(request):
    return {'basket': Basket(request)} 