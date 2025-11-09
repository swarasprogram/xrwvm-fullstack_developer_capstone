from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class CarModel(models.Model):
    class CarType(models.TextChoices):
        SEDAN = "Sedan", "Sedan"
        SUV = "SUV", "SUV"
        WAGON = "Wagon", "Wagon"
        COUPE = "Coupe", "Coupe"
        TRUCK = "Truck", "Truck"
        HATCH = "Hatchback", "Hatchback"

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=CarType.choices, default=CarType.SEDAN)
    year = models.IntegerField()

    class Meta:
        unique_together = ("make", "name", "year")
        ordering = ["-year", "make__name", "name"]

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"
