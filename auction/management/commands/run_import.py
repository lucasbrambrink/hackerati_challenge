from django.core.management.base import BaseCommand, CommandError
from auction.scripts import ImportHandler

class Command(BaseCommand):
    help = 'Imports new items from craigslist'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id'][0]
        importer = ImportHandler(user_id)
        importer.perform_sync_from_craigslist()

        self.stdout.write('Successfully Imported')