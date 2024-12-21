from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe

from fish import models


@admin.register(models.MyFish)
class MyFishAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "current_tank"]

    def get_actions(self, request):
        # Kudos to https://lukeplant.me.uk/blog/posts/dynamically-generated-django-admin-actions/
        actions = super().get_actions(request)

        for tank in models.Tank.objects.all():

            def transfer_fish_to_tank_action(tank):
                def transfer_fish(modeladmin, request, queryset):
                    queryset.update(current_tank=tank)

                transfer_fish.short_description = f"Transfer fish to {tank}"
                transfer_fish.__name__ = f"transfer_fish_to_{tank.pk}"

                return transfer_fish

            action = transfer_fish_to_tank_action(tank)
            actions[action.__name__] = (
                action,
                action.__name__,
                action.short_description,
            )

        return actions


@admin.register(models.Species)
class SpeciesAdmin(admin.ModelAdmin):
    readonly_fields = ["show_photo"]
    list_display = ["name", "origin", "schools", "recommended_tank", "fish_count"]

    @admin.display(description="Photo")
    def show_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="400px"/>')


@admin.register(models.Tank)
class TankAdmin(admin.ModelAdmin):
    readonly_fields = ["fish_summary"]
    list_display = ["name", "capacity", "unit", "fish_count"]

    @admin.display(description="Species in aquarium")
    def fish_summary(self, obj):
        table = "<table><tr><th>Species</th><th>Quantity</th></tr>{body}</table>"
        body = ""
        summary = (
            obj.myfish_set.filter(is_deceased=False)
            .values("species__name")
            .annotate(count=Count("species"))
        )
        for s in summary.iterator():
            body = body + f"<tr><td>{s['species__name']}</td><td>{s['count']}</td></tr>"
        return mark_safe(table.format(body=body))


@admin.register(models.TankTransferHistory)
class TankTranferHistoryAdmin(admin.ModelAdmin):
    list_display = ["date", "tank", "fish"]
