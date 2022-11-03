import pandas as pd

from django.core.management.base import BaseCommand

from main.models import User


class Command(BaseCommand):
    help = 'seed_dummy'

    def handle(self, *args, **options):
        print('seed_dummy')

        df = pd.read_csv("./main/data/dummy/user.csv")
        for i in range(len(df)):
            row = df.iloc[i, :]
            data = dict(row)
            if User.objects.filter(email=data["email"]).count() == 0:
                User.objects.create_superuser(**data)
