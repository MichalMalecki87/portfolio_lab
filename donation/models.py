from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.options import Options

INSTITUTION_TYPES = ((1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna'))


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_inst = models.IntegerField(choices=INSTITUTION_TYPES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}, typu {self.get_type_inst_display()}'


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.DO_NOTHING)
    is_taken = models.BooleanField(default=False)

    class Meta:
        ordering = ('is_taken', 'id')

    def __str__(self):
        if not self.is_taken:
            taken = "jeszcze nieodebrany"
        else:
            taken = " już odebrany"
        return f"{self.quantity} worki, od {self.user.username}, {taken}."
