import csv
import os

from django.http import HttpResponse
from django.core.files import File

from ..models.product import Product
from ..models.subcategory import Subcategorie


def view(request):
    subcategory = Subcategorie.objects.get(name="Ամրակցման պարագաներ")
    current_path = os.path.dirname(__file__)
    img_dir = os.path.join(current_path, 'img/6)շինանյութ/8)ամրակցման_պարագաներ')
    csv_path = os.path.join(current_path, 'csv/6)շինանյութ/8)ամրակցման_պարագաներ.csv')

    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 1

        for row in reader:
            product_name = row["Product Name"]
            product_price = int(row["Price"])
            quantity_available = int(float(row["Quantity Available"]))
            specifications = row["Specifications"]

            img_filename = f"{counter}.webp"
            img_path = os.path.join(img_dir, img_filename)

            product = Product.objects.create(
                subcategory=subcategory,
                name=product_name,
                price=product_price,
                quantity_available=quantity_available,
                specifications=specifications
            )

            with open(img_path, 'rb') as img_file:
                product.image.save(img_filename, File(img_file), save=True)
            counter += 1

    return HttpResponse("Adding data to the database has begun.")
