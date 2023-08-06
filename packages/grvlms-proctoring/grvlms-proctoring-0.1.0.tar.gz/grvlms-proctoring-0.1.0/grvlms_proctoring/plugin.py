import click
from glob import glob
import os

from grvlms.commands import config as config_cli
from grvlms import interactive
from grvlms import config as grvlms_config
from grvlms import env

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "CONTACT_US": "",
        "FAQ": "",
        "ONLINE_PROCTORING_RULES": "",
        "TECH_REQUIREMENTS": "",

        "CRYPTO_KEY": "",
        "EXAM_REGISTER_ENDPOINT": "",
        "EXAM_SPONSOR": "",
        "ORGANIZATION": "",
        "SECRET_KEY": "",
        "SECRET_KEY_ID": "",
        "SOFTWARE_DOWNLOAD_URL": "",
    }

}

hooks = {}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches

def ask_questions(config, defaults):
    interactive.ask(
        "Link contact us:", 
        "PROCTORING_CONTACT_US", 
        config, 
        {"PROCTORING_CONTACT_US": ""})
    interactive.ask(
        "Link FAQ:",
        "PROCTORING_FAQ",
        config,
        {"PROCTORING_FAQ": ""})
    interactive.ask(
        "Link online proctoring rules:",
        "PROCTORING_ONLINE_PROCTORING_RULES",
        config,
        {"PROCTORING_ONLINE_PROCTORING_RULES": ""})
    interactive.ask(
        "Link tech requirements:",
        "PROCTORING_TECH_REQUIREMENTS",
        config,
        {"PROCTORING_TECH_REQUIREMENTS": ""})
    interactive.ask(
        "SoftwareSecure crypto key:",
        "PROCTORING_CRYPTO_KEY",
        config,
        {"PROCTORING_CRYPTO_KEY": ""})
    interactive.ask(
        "Endpoint to SoftwareSecure:",
        "PROCTORING_EXAM_REGISTER_ENDPOINT",
        config,
        {"PROCTORING_EXAM_REGISTER_ENDPOINT": ""})
    interactive.ask(
        "SoftwareSecure sponsor:",
        "PROCTORING_EXAM_SPONSOR",
        config,
        {"PROCTORING_EXAM_SPONSOR": ""})
    interactive.ask(
        "SoftwareSecure organization:",
        "PROCTORING_ORGANIZATION",
        config,
        {"PROCTORING_ORGANIZATION": ""})
    interactive.ask(
        "SoftwareSecure secret key:",
        "PROCTORING_SECRET_KEY",
        config,
        {"PROCTORING_SECRET_KEY": ""})
    interactive.ask(
        "SoftwareSecure secret key ID:",
        "PROCTORING_SECRET_KEY_ID",
        config,
        {"PROCTORING_SECRET_KEY_ID": ""})
    interactive.ask(
        "SoftwareSecure download url:",
        "PROCTORING_SOFTWARE_DOWNLOAD_URL",
        config,
        {"PROCTORING_SOFTWARE_DOWNLOAD_URL": ""})


def load_config(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions(config, defaults)
    return config, defaults


@click.command(help="Config proctoring variables", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
              type=config_cli.YamlParamType(),
              multiple=True,
              metavar="KEY=VAL",
              help="Set a configuration value")
@click.pass_obj
def config_proctoring(context, interactive, set_):
    config, defaults = load_config(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)


@click.command(help="Print proctoring version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")


@click.group(help="Extra command for proctoring")
@click.pass_obj
def command(context):
    pass


command.add_command(print_version)
command.add_command(config_proctoring)
