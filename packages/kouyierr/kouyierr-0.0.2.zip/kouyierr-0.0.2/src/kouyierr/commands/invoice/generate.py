''' Invoice generator module.

    Parameters:
        year (int): Year of the invoice, default=current
        month (int): Month of the invoice, default=current
        company_config (str): Company config file
        invoice_config (str): Invoice config file
        template (str): Template file path
'''
import calendar
import sys
import datetime
import logging
import os
import time
import click
from jinja2 import Environment, FileSystemLoader
import pdfkit
from rich import print as rprint
from rich.console import Console
import yaml

from kouyierr.commands import global_options


class Generator:
    ''' Invoice generator class '''
    def __init__(self):
        logging.basicConfig(format='%(message)s')
        logging.getLogger(__package__).setLevel(logging.INFO)
        self._logger = logging.getLogger(__name__)

    def load_config(self, year: int, month: int, company_config: str, invoice_config:str) -> dict():
        ''' Build dict config based on local YAML files '''
        try:
            global_config = yaml.load(open(company_config), Loader=yaml.FullLoader)
            invoice_config = yaml.load(open(invoice_config), Loader=yaml.FullLoader)
            config = {**global_config, **invoice_config} # merge both dict()
            # static tax compute (to avoid Jinja2 complex filter use)
            config['invoice_total_ht'] = 0
            for invoice_item in invoice_config['invoice_items']:
                config['invoice_total_ht'] += (invoice_item['quantity'] * invoice_item['unit_price'])
            # static items generation, yes we're lazy
            config['title'] = f"{config['customer_name']} | {year}{month}"
            config['invoice_id'] = f"{year}{month}_{config['customer_id']}"
            # retrieve last day of month, aka golden day
            config['generated_date'] = f'{calendar.monthrange(year, month)[1]}/{month}/{year}'
            invoice_due_date = datetime.datetime.strptime(config['generated_date'], '%d/%m/%Y') + datetime.timedelta(days=30)
            config['invoice_due_date'] = f'{invoice_due_date.day}/{invoice_due_date.month}/{invoice_due_date.year}'
            return config
        except Exception as exception:
            self._logger.error("Error loading invoice file: %s", exception)
            sys.exit(1)

    def load_template(self, template: str):
        ''' Load Jinja2 template and attach a custom filter for currency format '''
        try:
            template_file = os.path.basename(template)
            template_path = os.path.dirname(template)
            env = Environment(loader=FileSystemLoader(template_path))
            env.filters['format_currency'] = self.format_currency
            return env.get_template(template_file)
        except Exception as exception:
            self._logger.error(exception)
            sys.exit(1)

    @staticmethod
    def format_currency(value):
        ''' Allow currency format with thousand separator and float double digit'''
        return "{:,.2f}".format(value).replace(',', ' ')


@click.command(help='Generate a new invoice based on definition file and company template')
@global_options
@click.option('--year', required=False, type=int, default=datetime.datetime.now().year,
    help='Year of the invoice, default=current')
@click.option('--month', required=False, type=int, default=datetime.datetime.now().month,
    help='Month of the invoice, default=current')
@click.option('--company_config', '--company', required=True, type=str, help='Company config file')
@click.option('--invoice_config', '--invoice', required=True, type=str, help='Invoice config file')
@click.option('--template', required=True, type=str, help='Template file path')
def generate(year: int, month: int, company_config: str, invoice_config: str, template: str):
    ''' Generate a new invoice based on definition file and company template '''
    start_time = time.time()
    invoice_generator = Generator()
    rprint("[bold green]Starting invoice generation[/bold green] lucky :bear: ...")
    config = invoice_generator.load_config(
        year=year,
        month=month,
        company_config=os.path.abspath(company_config),
        invoice_config=os.path.abspath(invoice_config)
    )
    rprint("[bold yellow]Following configuration has been loaded:[/bold yellow]")
    console = Console()
    console.log(config)
    template = invoice_generator.load_template(os.path.abspath(template))
    output_from_parsed_template = template.render(config)
    html_file_path = os.path.join(os.getcwd(), f"{year}{month}_{config['customer_id']}.html")
    pdf_file_path = os.path.join(os.getcwd(), f"{year}{month}_{config['customer_id']}.pdf")
    pdfkit_options = { 'quiet': '' }
    with open(html_file_path, "w") as file_stream:
        file_stream.write(output_from_parsed_template)
        rprint(f"[blue]HTML file {html_file_path} has been generated![/blue]")
    pdfkit.from_string(
        input=output_from_parsed_template,
        output_path=pdf_file_path,
        options=pdfkit_options
    )
    rprint(f"[blue]PDF file {pdf_file_path} has been generated![/blue]")
    elapsed_time = round(time.time() - start_time, 2)
    rprint(f"[bold green]Invoice generation complete[/bold green] in {elapsed_time}s :thumbs_up:")
