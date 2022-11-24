from django.db import models

from authentication.models import Organization, PersonalUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    pharmacies = models.ManyToManyField(Organization, related_name="products")

    def __str__(self):
        return self.name


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "1", "Pending"
        PAID = "2", "Paid"
        FULFILLED = "3", "Fulfilled"

    status = models.CharField(choices=OrderStatus.choices, max_length=2)
    pharmacy = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(PersonalUser, on_delete=models.CASCADE, related_name="orders_bought")
    price = models.FloatField()

    def save(self, *args, **kwargs):
        if self.status == Order.OrderStatus.FULFILLED and self.id and Order.objects.get(id=self.id).exists() and \
                Order.objects.get(id=self.id).status != Order.OrderStatus.FULFILLED:
            for item in self.items.all():
                item: OrderEntry
                item.product.stock -= item.quantity
                item.product.save()
        if not self.price:
            self.price = sum([item.product.price * item.quantity for item in self.items.all()])
        super(Order, self).save(*args, **kwargs)


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderEntries")
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
