from django.db import models
from django.dispatch import receiver


class Species(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    origin = models.CharField(max_length=255, blank=True, null=False)
    ph_min = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ph_max = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    temp_min = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    temp_max = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    adult_length = models.PositiveIntegerField(blank=True, null=True)
    schools = models.PositiveIntegerField(default=1)
    recommended_tank = models.PositiveIntegerField(null=True)
    photo = models.ImageField(upload_to="species_files/", blank=True, null=True)

    @property
    def fish_count(self):
        return self.myfish_set.filter(is_deceased=False).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Species"


class Tank(models.Model):
    class TankCapacityUnits(models.IntegerChoices):
        LITER = 1
        GALLON = 2

    name = models.CharField(max_length=255, null=True)
    capacity = models.PositiveIntegerField(null=False)
    unit = models.PositiveSmallIntegerField(
        choices=TankCapacityUnits.choices, default=TankCapacityUnits.GALLON
    )
    length = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        capacity = str(self.capacity)
        if self.unit and self.unit == self.TankCapacityUnits.LITER:
            capacity = capacity + " (l)"

        if self.unit and self.unit == self.TankCapacityUnits.GALLON:
            capacity = capacity + " (g)"

        if self.name:
            capacity = f"{self.name} - {capacity}"

        if self.length and self.width and self.height:
            return f"{capacity} - {self.length}L x {self.width}W x {self.height}H"

        return capacity

    @property
    def has_fish(self):
        return self.myfish_set.exists()

    @property
    def fish_count(self):
        return self.myfish_set.count()

    class Meta:
        ordering = ["capacity"]


class MyFish(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    species = models.ForeignKey(to=Species, on_delete=models.SET_NULL, null=True)
    date_bought = models.DateField(blank=True, null=True)
    store = models.CharField(max_length=255, blank=True, null=True)
    current_tank = models.ForeignKey(
        to=Tank, on_delete=models.SET_NULL, blank=True, null=True
    )
    is_deceased = models.BooleanField(blank=True, default=False)

    def __str__(self):
        if self.name and self.species:
            return f"{self.name} ({self.species})"

        if self.name:
            return str(self.name)

        if self.species:
            return str(self.species)

        return ""

    class Meta:
        ordering = ["name", "species__name"]
        verbose_name_plural = "My Fishes"


class TankTransferHistory(models.Model):
    date = models.DateField(auto_now_add=True, blank=False, null=False)
    tank = models.ForeignKey(to=Tank, on_delete=models.SET_NULL, null=True)
    fish = models.ForeignKey(to=MyFish, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.tank and self.fish:
            return f"{self.fish} transferred to {self.tank}"
        return str(self.date)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Transer History"


class TankLog(models.Model):
    date = models.DateField(blank=False, null=False)
    tank = models.ForeignKey(to=Tank, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=True)


@receiver(models.signals.post_save, sender=MyFish)
def transfer_fish_to_tank(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.current_tank != instance.current_tank:
            TankTransferHistory.objects.create(fish=instance, tank=obj.current_tank)
