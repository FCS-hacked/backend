from django.core.exceptions import BadRequest
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
    invoice = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="invoice_order",
                                   null=True, blank=True)
    prescription = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="prescription_order")
    razorpay_payment_id = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.prescription.signed_by_professional and not self.prescription.signed_by_hospital:
            raise BadRequest("Prescription must be signed by professional or hospital")
        if self.invoice and not self.invoice.signed_by_pharmacy:
            raise BadRequest("Invoice must be signed by pharmacy")

        if self.status == Order.OrderStatus.FULFILLED and self.id and \
                Order.objects.filter(id=self.id).exclude(status=Order.OrderStatus.FULFILLED).exists():
            for item in self.items.all():
                item: OrderItem
                item.product.stock -= item.quantity
                item.product.save()

        if self.razorpay_payment_id and self.status == Order.OrderStatus.PENDING:
            print("triggering payment")
            if Order.objects.filter(razorpay_payment_id=self.razorpay_payment_id).exists():
                raise BadRequest("Payment already exists")
            # Validate payment
            import razorpay
            client = razorpay.Client(auth=("rzp_test_lIBdvX0gfiR05C", "v7sda9dLwW5clna5Xo0oUc5V"))
            payment = client.payment.fetch(self.razorpay_payment_id)
            if payment['amount'] != int(self.price * 100):
                raise BadRequest("Invalid payment amount")
            if payment['status'] != "authorized":
                raise BadRequest("Payment not authorized")
            self.status = Order.OrderStatus.PAID

        if self.status == Order.OrderStatus.PAID and self.invoice:
            if not self.invoice.is_signed_by(self.pharmacy.custom_user):
                raise BadRequest("Invoice must be signed by pharmacy")
            self.status = Order.OrderStatus.FULFILLED
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def create_order(buyer, product_quantities, pharmacy_id, prescription_id) -> "Order":
        order_items = OrderItem.objects.bulk_create(
            [OrderItem(product=Product.objects.get(id=product_id), quantity=quantity) for
             product_id, quantity in product_quantities])
        order = Order.objects.create(
            pharmacy=Organization.objects.get(id=pharmacy_id),
            buyer=buyer,
            price=sum([item.product.price * item.quantity for item in order_items]),
            prescription=Document.objects.get(id=prescription_id)
        )
        order.items.set(order_items)
        return order


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderItems")
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
