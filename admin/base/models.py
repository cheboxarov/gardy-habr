from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    portfolio = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )

    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self):
        return self.name


class Orders(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, to_field='user_id', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    deadline = models.CharField(blank=True, null=True)
    deadline_hours = models.IntegerField(blank=True, null=True)
    price = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"{self.user} - {self.category} ({self.status})"



class Payments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    is_paid = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments'


class Prices(models.Model):
    price = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category')

    class Meta:
        managed = False
        db_table = 'prices'

    def __str__(self):
        return f"{self.price} (Category: {self.category})"


class Timers(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    discount_applied = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timers'

    def __str__(self):
        return f"{self.order} - {self.start_time} - {self.end_time} ({self.discount_applied})"


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, blank=True, null=True)
    username = models.CharField(blank=True, null=True)
    full_name = models.CharField(blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)
    promo = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username

