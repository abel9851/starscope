import random
from django.core.management.base import BaseCommand
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
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} places created!"))
