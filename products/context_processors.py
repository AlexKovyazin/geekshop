from basket.models import Basket


def basket(request):
    user_basket = []

    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)
    print(user_basket)
    return {'basket': user_basket}
