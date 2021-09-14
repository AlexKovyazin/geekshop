from basket.models import Basket


def basket(request):
    user_basket = []
    total_sum = 0
    total_quantity = 0

    if request.user.is_authenticated:
        user_basket = Basket.objects.select_related('user').filter(user=request.user)

        for item in user_basket:
            total_sum += item.sum()
            total_quantity += item.quantity

    return {
        'basket': user_basket,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
