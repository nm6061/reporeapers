import sys

from django.core.management.base import BaseCommand
from django.db import connection
from optparse import make_option

from app import database as db
from app import utilities as utils

U_QUERY = '''
    SELECT *
    FROM users
    WHERE id IN (
        SELECT owner_id FROM projects WHERE id IN (
            SELECT project_id FROM reaper_results WHERE id IN (9, 10)
        )
    );
'''
IU_QUERY = '''
    INSERT INTO users VALUES ({0})
'''

P_QUERY = '''
    SELECT *
    FROM projects
    WHERE id IN (SELECT project_id FROM reaper_results WHERE id IN (9, 10));
'''
IP_QUERY = '''
    INSERT INTO projects VALUES ({0})
'''

RRU_QUERY = '''
    SELECT *
    FROM reaper_runs;
'''
IRRU_QUERY = '''
    INSERT INTO reaper_runs VALUES ({0})
'''

RRE_QUERY = '''
    SELECT *
    FROM reaper_results WHERE id IN (9, 10);
'''
IRRE_QUERY = '''
    INSERT INTO reaper_results VALUES ({0})
'''

TABLES = ['Users', 'Projects', 'Reaper Runs', 'Reaper Results']
S_QUERIES = [U_QUERY, P_QUERY, RRU_QUERY, RRE_QUERY]
I_QUERIES = [IU_QUERY, IP_QUERY, IRRU_QUERY, IRRE_QUERY]


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
            cursor = connection.cursor()

            for index in range(0, len(TABLES)):
                table = TABLES[index]
                sq = S_QUERIES[index]
                iq = I_QUERIES[index]

                print(table)
                results = database.get(sq)
                for (idx, result) in enumerate(results):
                    self._print_('{0}/{1}'.format(idx + 1, len(results)))
                    cursor.execute(
                        iq.format(','.join(['%s'] * len(result))), result
                    )
                print()
        finally:
            database.disconnect()

    def _print_(self, message):
        sys.stdout.write(message)
        sys.stdout.write('\r')
        sys.stdout.flush()
