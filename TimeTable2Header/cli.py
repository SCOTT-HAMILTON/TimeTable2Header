import click
from TimeTable2Header.timetable2header import convert_excel_timetable2_c_header

@click.command()
@click.argument('input_excel_timetable', type=click.Path(exists=True))
def cli(input_excel_timetable):
    """Converts an excel spreadsheet of your school timetable to an header file to use with omega's agenda app, prints its output to stdout."""
    print(convert_excel_timetable2_c_header(
            input_excel_timetable))
