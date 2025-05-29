from django.shortcuts import render


def shopping_cart(request):
    """Render the shopping cart page"""
    return render(request, 'cart/cart.html')
