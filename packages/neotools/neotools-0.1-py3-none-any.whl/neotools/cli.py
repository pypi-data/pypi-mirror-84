import json
import logging
from enum import Enum
from functools import partial

import click

from neotools import commands

logger = logging.getLogger(__name__)

file_index_arg = partial(click.argument, 'file_index',
                         type=click.IntRange(1, 8))
applet_id_option = partial(click.option, '--applet-id', '-a', type=int)
format_option = partial(
    click.option, '--format', '-f', 'format_',
    help='Format for the file names. For example, "{name}-{space}-{date:%x}.txt" '
         'may produce "File 3-3-11/02/20.txt" depending on your locale. '
         'See more date formatting options at https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes')


@click.group()
@click.option('--verbose', '-v', default=False, is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    """
    For scripts that issue multiple commands, use the mode command to
    avoid repeated initialization.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    if verbose:
        logging.basicConfig(level=logging.DEBUG)


@cli.command('mode', help='Neo keyboard/comms mode. Mostly useful for scripting where the tool is called many times.')
@click.option('--keyboard', 'target_mode', flag_value='keyboard')
@click.option('--comms', 'target_mode', flag_value='comms')
def mode(target_mode):
    if target_mode is None:
        commands.get_mode()
    if target_mode == 'comms':
        commands.flip_to_communicator()
    elif target_mode == 'keyboard':
        commands.flip_to_keyboard()


@cli.group(help='Manage files for AlphaWord and other applets.')
def files():
    pass


@cli.group()
def applets():
    """ Inspect applets and manage their settings. """
    pass


@applets.command('list')
def applets_list():
    applets = commands.list_applets()
    print(json.dumps(applets, indent=2))


@applets.command('get-settings')
@click.argument('applet_id', type=int)
@click.argument('flag', type=int, nargs=-1)
def applet_get_settings(applet_id, flag):
    """
    List settings. Note that it is possible for the call to return
    different subsets of settings on multiple runs.

    The meaning of the flag depends on the applet and is not documented.
    The values that commonly give non-empty results are 0, 7, 15.
    """
    settings = commands.applet_read_settings(applet_id, flag)
    print(json.dumps(settings, indent=2, default=json_default))


@applets.command('set-settings')
@click.argument('applet_id', type=int)
@click.argument('ident', type=int)
@click.argument('value', nargs=-1)
def applet_set_settings(applet_id, ident, value):
    """
    To learn what settings are available for an applet, run get-settings.

    !!! Use this at your own risk - invalid settings may disrupt work of
    an applet or the device. There is validation for options and applet ids,
    but not for the open-ended values such as ranges and strings.

    The value depends on type of the setting: number for option id and applet id,
    string for passwords, and three numbers for the ranges.

    Examples:

    \b
    * Enable two-button on mode: applets set-settings 0 16400 4097
    * Set idle time to ten minutes: applets set-settings 0 16388 10 4 59
    * Set password for an AlphaWord file: applets set-settings 40960 32790 write2
    * Delete all AlphaWord files: applets set-settings 40960 32771 4097
    """
    commands.applet_write_settings(applet_id, ident, value)


@files.command("list")
@applet_id_option()
def list_all_files(applet_id):
    files = commands.list_files(applet_id)
    print(json.dumps(files, indent=2, default=json_default))


@files.command('read')
@applet_id_option()
@file_index_arg()
@click.option('--path', '-p', type=click.Path())
@format_option()
def read_file(file_index, applet_id, path, format_):
    commands.read_file(applet_id, file_index, path, format_)


@files.command('read-all')
@applet_id_option()
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False, writable=True), required=True)
@format_option()
def read_all_files(applet_id, path, format_):
    commands.read_all_files(applet_id, path, format_)


@files.command('write')
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
@file_index_arg()
def write_file(path, file_index):
    contents = open(path).read()
    commands.write_file(file_index, contents)


@files.command('clear')
@applet_id_option()
@file_index_arg()
def clear(applet_id, file_index):
    commands.clear_file(applet_id, file_index)


def json_default(val):
    if isinstance(val, Enum):
        return val.name
    elif isinstance(val, bytes):
        return str(val)[2:-1]
    elif isinstance(val, object) and hasattr(val, '__dict__'):
        return val.__dict__
    else:
        return str(val)
