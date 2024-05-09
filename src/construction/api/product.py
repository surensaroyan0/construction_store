from django.views import View
from django.views.generic import DeleteView
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from ..models.product import Product
from ..models.category import Category
from ..models.subcategory import Subcategory
from .authentication import auth


def category_subcategory():
    categories = [category.to_dict() for category in Category.objects.all()]
    subcategories = []
    for subcategory in Subcategory.objects.all():
        if "/" in subcategory.name:
            subcategory.name = subcategory.name.replace("/", "+")
        subcategories.append(subcategory.to_dict())
    return categories, subcategories


def context_func():
    categories, subcategories = category_subcategory()
    context = {
        "STATIC_URL": settings.STATIC_URL_PREFIX,
        "categories": categories,
        "subcategories": subcategories
    }
    return context


class ProductView(View):
    def get(self, request):
        is_auth, context = auth(request)
        context.update(context_func())

        products = Product.objects.all()
        products = [products[product].to_dict() for product in range(52)]
        context["products"] = products

        return render(request, "construction_store/home.html", context)

    def post(self, request):
        is_auth, context = auth(request)
        search_query = request.POST["search_query"]
        products = Product.objects.filter(name__icontains=search_query)
        context.update(context_func())

        if products:
            products = [product.to_dict() for product in products]
            context["products"] = products
        else:
            context["nothing_found"] = (f"Nothing was found for the request {search_query}\n"
                                        f"Try searching differently or shortening your query.")
        return render(request, "construction_store/home.html", context)


class ProductDetailView(DeleteView):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)
        context.update(context_func())
        category = kwargs.get('category')
        subcategory = kwargs.get('subcategory')
        if "+" in subcategory:
            subcategory = subcategory.replace("+", "/")

        category = get_object_or_404(Category, name=category)
        subcategory = get_object_or_404(Subcategory, category=category, name=subcategory)
        context["subcategory_name"] = subcategory.name
        products = Product.objects.filter(subcategory=subcategory)
        products = [product.to_dict() for product in products]

        if products:
            context["products"] = products
        else:
            context["nothing_found"] = (f"Nothing was found for the request {subcategory}\n"
                                        f"Try searching differently or shortening your query.")

        return render(request, "construction_store/home.html", context)
