import csv
import math
import os
import subprocess

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import render_to_string
from multiprocessing import Pool
from optparse import make_option

from app import database as db
from app import utilities as utils
from app.models import ReaperResult

IGNORES_FILEPATH = os.path.join(settings.PROJECT_ROOT, 'app/data/ignores.csv')
PAGE_SIZE = 500
DATASET = None


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-x', action='store_true', dest='export',
            help='Export data from the database to CSV file.'
        ),
        make_option(
            '-c', type='str', action='store', dest='config',
            default='config.json', help='Path to reaper config.json file.'
        ),
        make_option(
            '-o', type='str', action='store', dest='output',
            default='.output',
            help=(
                'Absolute path to the directory where the generated HTML '
                'files are stored.'
            )
        ),
    )
    help = (
        'Generates static pages for all the Django templates in the project.'
    )

    def handle(self, *args, **options):
        output = options.get('output')
        with open(options.get('config')) as file_:
            configuration = utils.read(file_)

        global DATASET
        DATASET = self._get_dataset_(configuration['options']['datasource'])

        self._create_tree_(output)
        _debug_('Using {0} as the output directory.'.format(output))

        self.generate_contact(output)

        self._create_tree_(os.path.join(output, 'results'))
        self.generate_results(os.path.join(output, 'results'))

        if options.get('export', False):
            _debug_('Exporting data into CSVs')
            self._create_tree_(os.path.join(output, 'static/downloads'))
            self.generate_content(os.path.join(output, 'static/downloads'))

    def generate_contact(self, output, *args, **kwargs):
        template_name = 'app/contact.html'
        file_name = 'contact.html'

        context = {
            'year': datetime.now().year,
        }
        render_to_file(
            template_name, os.path.join(output, file_name), context
        )

    def generate_results(self, output, *args, **kwargs):
        template_name = 'app/index.html'

        num_results = len(DATASET)
        num_pages = math.ceil(num_results / PAGE_SIZE)
        _debug_('Processing {0} results across {1} pages'.format(
            num_results, num_pages
        ))
        context = {'pages': num_pages}

        with Pool(16) as pool:
            pool.starmap(
                _generate,
                [
                    (template_name, curr_page, context, output)
                    for curr_page in range(1, (num_pages + 1))
                ]
            )

    def generate_content(self, output, *args, **kwargs):
        template_name = 'app/content.csv'
        file_name = 'dataset.csv'
        context = {'results': DATASET}
        render_to_file(
            template_name, os.path.join(output, file_name), context
        )
        self._compress(os.path.join(output, file_name))

    def _compress(self, path):
        _debug_('Compressing {}'.format(path))

        subprocess.call(args=['gzip', path])

    def _get_ignores_(self):
        ignores = None
        with open(IGNORES_FILEPATH) as file_:
            reader = csv.reader(file_)
            ignores = set([row[0] for row in reader])
        return ignores

    def _get_dataset_(self, settings):
        _debug_('Populating dataset')

        ignores = self._get_ignores_()
        _debug_('{} repositories will be ignored'.format(len(ignores)))

        dataset = list()

        # Query: Results from reporeaper.reaper_results MySQL table
        query = '''
            SELECT u.login, p.name, p.language,
                rr.score, rr.architecture, rr.community,
                rr.continuous_integration, rr.documentation, rr.history,
                rr.license, rr.management, rr.unit_test, rr.state, rr.stars,
                rr.timestamp
            FROM projects p
                JOIN reaper_results rr ON rr.project_id = p.id
                JOIN users u ON u.id = p.owner_id
            ORDER BY timestamp DESC
        '''

        database = db.Database(settings)
        try:
            database.connect()

            for row in database.get(query):
                item = ReaperResult()

                item.owner = row[0]
                item.name = row[1]
                if '{}/{}'.format(item.owner, item.name) in ignores:
                    continue
                item.language = row[2]
                item.score = row[3]
                item.architecture = row[4]
                item.community = row[5]
                item.continuous_integration = row[6]
                item.documentation = row[7]
                item.history = row[8]
                item.license = row[9]
                item.management = row[10]
                item.unit_test = row[11]
                item.state = row[12]
                item.stars = row[13]
                item.timestamp = row[14]

                dataset.append(item)
        finally:
            database.disconnect()

        return dataset

    def _create_tree_(self, path):
        if not os.path.exists(path):
            _debug_('Creating {0}'.format(path))
            os.makedirs(path, exist_ok=True)


def _generate(template_name, curr_page, context, output):
    prev_page = curr_page - 1
    next_page = curr_page + 1 if curr_page < context['pages'] else 0

    begin = 1 if prev_page == 0 else prev_page * PAGE_SIZE + 1
    end = (
        curr_page * PAGE_SIZE
        if (curr_page * PAGE_SIZE) < len(DATASET) else len(DATASET)
    )

    context['results'] = DATASET[begin:(end + 1)]
    context['ppage'] = prev_page
    context['cpage'] = curr_page
    context['npage'] = next_page

    page_name = '{0}.html'.format(curr_page)
    render_to_file(
        template_name, os.path.join(output, page_name), context
    )


def render_to_file(template, destination, context=None):
    _debug_('Rendering {0}'.format(destination))
    with open(destination, 'w') as file_:
        file_.write(render_to_string(
            template, context_instance=Context(context)
        ))


def _debug_(text):
    if 'DEBUG' in os.environ:
        print('[DEBUG] {0}'.format(text))
