# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
from twccli.twcc.util import validate, isNone
from twccli.twcc.session import Session2
from twccli.twccli import pass_environment
from twccli.twcc.util import *

lang_encoding = """
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export PYTHONIOENCODING=UTF-8
"""

@click.command(help='Get exsisting information.')
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose mode.")
@pass_environment
def whoami(ctx, verbose):
    """Command line for whoami, print information of account and session

    :param verbose: Enables verbose mode
    :type verbose: bool
    """
    ctx.verbose = verbose
    ctx.log("Hi, {}, nice to meet you!".format(
        Session2._whoami()['display_name']))
    print(Session2())


@click.command(help='Configure the TWCC CLI.')
@click.option("-v", "--verbose", is_flag=True,
              help="Enable verbose mode.")
@click.option('-pcode', '--project-code', 'proj_code',
              help=" TWCC project code (e.g., GOV108009)")
@click.option('--apikey', 'apikey',
              help="TWCC API Key for CLI.")
@click.option('-rc', '--set-bashrc', 'rc', is_flag=True,
              help="Set bashrc parameters.")
@pass_environment
def init(ctx, apikey, proj_code, rc, verbose):
    """Constructor method

    :param apikey: TWCC API Key for CLI. It also can read $TWCC_API_KEY.
    :type apikey: string
    :param proj_code: TWCC project code (e.g., GOV108009)
    :type proj_code: string
    :param verbose: Enable verbose mode.
    :type verbose: bool
    :param rc_setting: Set bashrc parameters.
    :type rc_setting: bool
    """
    ctx.verbose = verbose
    if not Session2._isValidSession():
        if isNone(apikey):
            if 'TWCC_API_KEY' in os.environ:
                apikey = os.environ['TWCC_API_KEY']
        else:
            os.environ['TWCC_API_KEY'] = apikey

        if isNone(proj_code) and 'TWCC_PROJ_CODE' in os.environ:
            proj_code = os.environ['TWCC_PROJ_CODE']

        if isNone(apikey) or len(apikey) == 0:
            apikey = click.prompt('Please enter TWCC APIKEY', type=str)

        if isNone(proj_code) or len(proj_code) == 0:
            proj_code = click.prompt(
                'Please enter TWCC project code', type=str)

        if validate(apikey):
            proj_code = proj_code.upper()
            ctx.vlog("Receiving Project Code: %s", (proj_code))
            ctx.vlog("Receiving API Key: %s", (apikey))

            Session2(twcc_api_key=apikey, twcc_project_code=proj_code)

            click.echo(click.style("Hi! {}, welcome to TWCC!".format(
                Session2._whoami()['display_name']), fg='yellow'))

            if rc:
                click.echo("Add language setting to `.bashrc`.")

                open(os.environ["HOME"]+"/.bashrc", 'a').write(lang_encoding)
            else:
                click.echo("Please add encoding setting to your environment: \n {}".format(lang_encoding))

        else:
            raise ValueError("API Key is not validated.")
    else:
        ctx.log("load credential from {}".format(Session2()._getSessionFile()))
        print(Session2())

@click.command(help='Show this version.')
@pass_environment
def version(ctx):
    """Show TWCC-CLI version

    """
    from twccli.version import __version__
    ctx.log("This version is {}".format(__version__))


@click.group(help="Configure the TWCC CLI.")
def cli():
    pass


cli.add_command(whoami)
cli.add_command(init)
cli.add_command(version)



def main():
    cli()


if __name__ == "__main__":
    main()
