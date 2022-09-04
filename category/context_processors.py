from .models import Category

def allCats(request):

    cats=Category.objects.all().prefetch_related("product_set")
    return {
        'cats':cats
    }