import click
from TimeTable2Header.convert_timetable2header import convert_odf_timetable2_c_header

@click.command()
@click.argument('input_odf_timetable', type=click.Path(exists=True))
def cli(input_odf_timetable):
    """Converts an odf spreadsheet of your school timetable to an header file to use with omega's agenda app, prints its output to stdout."""
    print(convert_odf_timetable2_c_header(
            input_odf_timetable))
