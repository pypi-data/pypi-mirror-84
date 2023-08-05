import os
import click
from keep import cli, utils


@click.command('run', short_help='Executes a saved command.',
               context_settings=dict(ignore_unknown_options=True))
@click.argument('pattern', required=False)
@click.argument('arguments', nargs=-1, type=click.UNPROCESSED)
@click.option('--safe', is_flag=True, help='Ignore missing arguments')
@click.option('-n', '--no-confirm', is_flag=True, help='Don\'t ask confirm before running')
@cli.pass_context
def cli(ctx, pattern, arguments, safe, no_confirm):
    """Executes a saved command."""

    if not pattern:
        pattern = "(.*?s)"
    matches = utils.grep_commands(pattern)
    if matches:
        selected = utils.select_command(matches)
        if selected >= 0:
            cmd, desc = matches[selected]
            pcmd = utils.create_pcmd(cmd)
            raw_params, params, defaults = utils.get_params_in_pcmd(pcmd)

            arguments = list(arguments)
            kargs = {}
            for r, p, d in zip(raw_params, params, defaults):
                if arguments:
                    val = arguments.pop(0)
                    click.echo("{}: {}".format(p, val))
                    kargs[r] = val
                elif safe:
                    if d:
                        kargs[r] = d
                else:
                    p_default = d if d else None
                    val = click.prompt("Enter value for '{}'".format(p), default=p_default)
                    kargs[r] = val
            click.echo("\n")

            final_cmd = utils.substitute_pcmd(pcmd, kargs, safe)

            if no_confirm:
                isconfirmed = True
            else:
                command = "$ {} :: {}".format(final_cmd, desc)
                isconfirmed = click.confirm("Execute\n\t{}\n\n?".format(command), default=True)

            if isconfirmed:
                os.system(final_cmd)

    elif matches == []:
        click.echo('No saved commands matches the pattern {}'.format(pattern))
    else:
        click.echo("No commands to run, Add one by 'keep new'. ")
