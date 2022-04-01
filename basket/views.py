from django.http import JsonResponse, response
from django.shortcuts import get_object_or_404, render

from .basket import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        # try:
        #     product = Product.objects.get(id=product_id)
        # except:
        #     raise Http404
        basket.add(product=product, qty=product_qty)
        
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response
    
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
    
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        # print(product_id, product_qty, "naveen")
        basket.update(product=product_id, qty=product_qty)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        # print(basketqty, baskettotal, "check")
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response