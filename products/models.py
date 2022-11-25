from django.db import models

from authentication.models import Organization, PersonalUser
from documents.models import Document


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

    status = models.CharField(choices=OrderStatus.choices, max_length=2, default=OrderStatus.PENDING)
    pharmacy = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(PersonalUser, on_delete=models.CASCADE, related_name="orders_bought")
    price = models.FloatField()
    invoice = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="order", null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.status == Order.OrderStatus.FULFILLED and self.id and Order.objects.get(id=self.id).exists() and \
                Order.objects.get(id=self.id).status != Order.OrderStatus.FULFILLED:
            for item in self.items.all():
                item: OrderItem
                item.product.stock -= item.quantity
                item.product.save()
        if not self.price:
            self.price = sum([item.product.price * item.quantity for item in self.items.all()])
        if self.razorpay_payment_id and self.status == Order.OrderStatus.PENDING:
            if Order.objects.filter(razorpay_payment_id=self.razorpay_payment_id).exists():
                raise Exception("Payment already exists")
            # Validate payment
            import razorpay
            client = razorpay.Client(auth=("rzp_test_lIBdvX0gfiR05C", "v7sda9dLwW5clna5Xo0oUc5V"))
            payment = client.payment.fetch(self.razorpay_payment_id)
            if payment['amount'] != int(self.price * 100):
                raise Exception("Invalid payment amount")
            if payment['status'] != "authorized":
                raise Exception("Payment not authorized")
            self.status = Order.OrderStatus.PAID
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def create_order(buyer, product_quantities, pharmacy) -> "Order":
        order_entries = OrderItem.objects.bulk_create(
            [OrderItem(product=Product.objects.get(id=product_id), quantity=quantity) for
             product_id, quantity in product_quantities])
        order = Order.objects.create(pharmacy=pharmacy, buyer=buyer)
        order.items.add(*order_entries)
        order.save()
        return order


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderItems")
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
