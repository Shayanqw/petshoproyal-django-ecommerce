from home.models import Category
def cat(request):
    category = Category.objects.filter(sub_cat=False)
    return {'category':category}