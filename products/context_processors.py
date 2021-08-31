from basket.models import Basket


def basket(request):
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user_id=request.user)
        return {'basket': user_basket}
