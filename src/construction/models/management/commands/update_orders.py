from django.core.management.base import BaseCommand
from django.utils import timezone

from ...order import Order


class Command(BaseCommand):
    help = "Update order statuses"

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        orders = Order.objects.all()
        for order in orders:
            days_since_order = (current_time - order.order_date).days
            if days_since_order == 0:
                order.status = 1
            elif days_since_order == 1:
                order.status = 2
            elif days_since_order == 2:
                order.status = 3
            elif days_since_order == 3:
                order.status = 4
            elif days_since_order == 4:
                order.status = 5
            order.save()
