# -*- coding: utf-8 -*-

from click.testing import CliRunner
import threading

import localshare


def test_non_existent_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(localshare.share, ['nonexistent'])
        assert result.exit_code == 2
        assert 'Path "nonexistent" does not exist.' in result.output


def test_existing_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('hello.txt', 'w') as f:
            f.write('Hello World!')
        thread = threading.Thread(target=runner.invoke, args=[localshare.download, ["hello.txt"]])
        thread.start()
        result = runner.invoke(localshare.share, ['hello.txt'])
        assert result.exit_code == 0
        assert 'Sharing hello.txt' in result.output


def test_wrongfile_download():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('hello.txt', 'w') as f:
            f.write('Hello World!')
        thread = threading.Thread(target=runner.invoke, args=[localshare.share, ["hello.txt"]])
        thread.start()
        result = runner.invoke(localshare.download, ['nothello.txt'])
        assert result.exit_code == 1
        assert 'nothello.txt not found in available files.' in str(result.exception)