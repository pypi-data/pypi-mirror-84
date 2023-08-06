import getpass
import os
import py_compile
import shutil
import tempfile

import click
import paramiko
import scp

from py_deploy import __version__

DEFAULT_SSH_PORT = 22


def get_file_name(file_path: str) -> str:
    return file_path.rsplit('/', 1)[-1]


def get_pyc_name(file_path: str) -> str:
    return f"{get_file_name(file_path).rsplit('.', 1)[0]}.pyc"


def verbose_log(verbose: bool, phrase: str):
    if verbose:
        print(phrase)


@click.command()
@click.option('-i', '--identity-file', 'identity_file', help='SSH identity file')
@click.option('-p', '--password', 'with_password', is_flag=True)
@click.option('-P', '--port', 'port', help='SSH target port')
@click.option('-s', '--source', 'source', help='Source', default='.')
@click.option('-t', '--target', 'target', help='Target', required=True)
@click.option('-h', '--host', 'host', help='Host IP address or name', required=True)
@click.option('-u', '--username', 'username', help='Remote username')
@click.option(
    '-e',
    '--exclude',
    'exclude_dirs',
    help='Dirs names to exclude',
    multiple=True,
    default=['tests', '.git', '__pycache__'],
)
@click.option('-v', '--verbose', 'verbose', is_flag=True)
@click.version_option(version=__version__)
def cli(
        identity_file,
        with_password,
        port,
        source,
        target,
        host,
        username,
        exclude_dirs,
        verbose,
):
    password = None
    if with_password:
        password = getpass.getpass('Remote server password: ')

    with tempfile.TemporaryDirectory() as dest_dir:
        verbose_log(verbose, f'Compiling into {dest_dir}')

        for root, dirs, files in os.walk(source):
            if any(exclude_dir in root for exclude_dir in exclude_dirs):
                continue

            out_dir = os.path.join(dest_dir, root.lstrip(f'.{os.sep}'))
            os.makedirs(out_dir, mode=os.stat(root).st_mode, exist_ok=True)
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.py'):
                    out_file = py_compile.compile(file_path, cfile=os.path.join(out_dir, get_pyc_name(file)))
                    verbose_log(verbose, f'Compiled: {file_path} -> {out_file}')
                else:
                    shutil.copyfile(file_path, os.path.join(out_dir, get_file_name(file)))
                    verbose_log(verbose, f'Copied: {file_path} -> {os.path.join(out_dir, get_file_name(file))}')

        with tempfile.NamedTemporaryFile() as file:
            verbose_log(verbose, f'Creating archive: {file.name}.zip')
            archive_path = shutil.make_archive(file.name, 'zip', dest_dir)

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(
                hostname=host,
                port=port or DEFAULT_SSH_PORT,
                username=username,
                password=password,
                key_filename=identity_file,
            )

            verbose_log(verbose, f'Copying: {archive_path} -> {host}:{target}.zip')
            scp.put(client.get_transport(), archive_path, f'{target}.zip')

            verbose_log(verbose, f'Unpacking archive into "{target}" folder')
            client.exec_command(' '.join(('unzip', f'{target}.zip', '-d', target)))
            client.exec_command(' '.join(('rm', '-f', f'{target}.zip')))
