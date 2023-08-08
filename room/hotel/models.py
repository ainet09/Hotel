from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"{self.guest_name} - {self.room.room_number} ({self.check_in_date} to {self.check_out_date})"
