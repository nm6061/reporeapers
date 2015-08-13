from django.core.management.base import BaseCommand
from optparse import make_option

from app import database as db
from app import utilities as utils
from app.models import ReaperResult

QUERY = '''
    SELECT u.login, p.name, p.language,
        rr.score, rr.architecture, rr.community, rr.continuous_integration,
        rr.documentation, rr.history, rr.license, rr.management, rr.unit_test,
        rr.state, rr.recorded_at
    FROM projects p
        JOIN reaper_results rr ON rr.project_id = p.id
        JOIN users u ON u.id = p.owner_id
    WHERE run_id <> 1;
'''

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-c', type='str', action='store', dest='config',
            default='config.log', help='Path to reaper config.log file.'
        ),
    )
    help = (
        'Replicates reporeaper.reaper_results table into a SQLite database.'
    )

    def handle(self, *args, **options):
        with open(options.get('config')) as file_:
            configuration = utils.read(file_)

        database = db.Database(configuration['options']['datasource'])
        try:
            database.connect()

            results = list()
            for item in database.get(QUERY):
                result = ReaperResult()

                result.owner = item[0]
                result.name = item[1]
                result.language = item[2]
                result.score = item[3]
                result.architecture = item[4]
                result.community = item[5]
                result.continuous_integration = item[6]
                result.documentation = item[7]
                result.history = item[8]
                result.license = item[9]
                result.management = item[10]
                result.unit_test = item[11]
                result.state = item[12]
                result.created_at = item[13]

                results.append(result)

            ReaperResult.objects.bulk_create(results)
        finally:
            database.disconnect()