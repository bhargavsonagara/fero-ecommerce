from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class UserMixin(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_created_by_related",
                                   related_query_name="%(app_label)s_%(class)ss_created_by",
                                   editable=False)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="%(app_label)s_%(class)s_modified_by_related",
                                    related_query_name="%(app_label)s_%(class)ss_modified_by",
                                    editable=False)

    class Meta:
        abstract = True


class Customer(UserMixin, TimestampMixin, BaseModel):
    name = models.CharField(max_length=100, verbose_name="customer name")
    contact_number = models.CharField(max_length=20, verbose_name="contact number")
    email = models.EmailField(verbose_name="email address")

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]


class Product(UserMixin, TimestampMixin, BaseModel):
    name = models.CharField(max_length=100, verbose_name="product name")
    weight = models.DecimalField(decimal_places=2, max_digits=4)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class Order(UserMixin, TimestampMixin, BaseModel):
    order_number = models.CharField(max_length=20, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField()
    address = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.order_number and self.pk is None:
            last_order = Order.objects.all().order_by("-pk").first()
            last_pk = 0
            if last_order:
                last_pk = last_order.pk
            # ex:- ORD-00001
            self.order_number = "ORD-" + str(last_pk + 1).zfill(5)

        super(Order, self).save()

    class Meta:
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer']),
        ]


class OrderItem(UserMixin, TimestampMixin, BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order_items')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]
