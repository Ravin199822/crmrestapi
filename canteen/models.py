from django.db import models


# Create your models here.


class Users(models.Model):
    enrollment_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    passwords = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "users"


class Items(models.Model):
    ITEM_CATEGORY = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    )
    NO_OF_ITEMS = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    category = models.CharField(max_length=40, choices=ITEM_CATEGORY, default="breakfast")
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    desc = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "items"


class UserItem(models.Model):
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    toal_amount = models.CharField(max_length=500, default=0, null=True)

    def __str__(self):
        return f"{self.user}----{self.items}"

    class Meta:
        unique_together = ['user', 'items',]

    def user_details(self):
        return f"{self.user.name}---{self.user.contact_no}"


class Payment(models.Model):
    user_items = models.ForeignKey(UserItem, on_delete=models.CASCADE, default=None)
    payment_status = models.CharField(max_length=10, default="false")
    order_status = models.CharField(max_length=10, default="unserved")

    def __str__(self):
        return f"{self.user_items}----{self.payment_status}---{self.order_status}"

    class Meta:
        db_table = "payment"
