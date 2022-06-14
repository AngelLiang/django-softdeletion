from django.db import models
from django.db.models import Sum

from django_softdeletion import SoftDeletionModelMixin
from django_softdeletion import UnSoftDeletedManager


class Customer(SoftDeletionModelMixin, models.Model):
    name = models.CharField('姓名', max_length=255)
    phone = models.CharField('联系电话', max_length=255)

    def __str__(self):
        return self.name


class ProductManager(UnSoftDeletedManager, models.Manager):
    pass


class Product(SoftDeletionModelMixin, models.Model):
    name = models.CharField('名称', max_length=255)
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

    objects = ProductManager()


class OrderTemplate(SoftDeletionModelMixin, models.Model):
    order_date = models.DateField('订单日期')

    def __str__(self):
        return f'[{self.id}]{self.order_date}'


class Order(OrderTemplate):
    title = models.CharField('标题', max_length=255, default='')
    amount = models.DecimalField(
        '总金额', max_digits=11, decimal_places=2, blank=True, default=0)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='客户')

    def update_amount(self):
        amount = self.orderitem_set.aggregate(Sum('amount'))['amount__sum']
        if amount is not None:
            self.amount = amount
            self.save(update_fields=['amount'])


class OrderItem(SoftDeletionModelMixin, models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='订单', db_constraint=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='产品', db_constraint=False)

    quantity = models.PositiveSmallIntegerField('数量')
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)
    amount = models.DecimalField(
        '总价', max_digits=11, decimal_places=2, null=True, default=0)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        self.order.update_amount()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_amount()
