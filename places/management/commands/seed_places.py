import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from places import models as place_models


class Command(BaseCommand):
    help = "This command creates many places"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="how many places do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        seeder.add_entity(
            place_models.Place,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "viewfinder": lambda x: random.choice(all_users),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for pk in created_clean:
            place = place_models.Place.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                place_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    place=place,
                    file=f"place_photos/{random.randint(1, 40)}.jpg",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} places created!"))
