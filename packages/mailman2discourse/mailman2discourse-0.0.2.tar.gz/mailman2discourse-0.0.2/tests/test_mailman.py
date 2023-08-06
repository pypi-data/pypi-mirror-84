import argparse
import pytest
from mailman2discourse import mailman
from tests.helpers_mailman import mailman_write_config, mailman_create_config


def test_load_synthetic(tmpdir):
    n = 'listname'
    mailman_write_config(f'{tmpdir}/{n}', mailman_create_config())
    m = mailman.Mailman(argparse.Namespace(mailman_dir=str(tmpdir),
                                           mailman_encoding='UTF-8',
                                           list=n))
    assert m.load() is True


def test_load_skip(tmpdir, caplog):
    n = 'listname'
    c = mailman_create_config()
    email = 'some@example.com'
    c['digest_members'][email] = 0
    c['language'][email] = 'fr'
    mailman_write_config(f'{tmpdir}/{n}', c)
    m = mailman.Mailman(argparse.Namespace(mailman_dir=str(tmpdir),
                                           mailman_encoding='UTF-8',
                                           list=n))
    assert m.load() is True
    assert f'SKIP digest_members for unknown user {email}' in caplog.text
    assert f'SKIP language for unknown user {email}' in caplog.text


@pytest.mark.parametrize("workload,encoding", [('greek', 'iso-8859-1'),
                                               ('regular', 'UTF-8'),
                                               ('instances', 'UTF-8')])
def test_load_realistic(workload, encoding):
    m = mailman.Mailman(argparse.Namespace(mailman_dir='tests/data',
                                           mailman_encoding=encoding,
                                           list=workload))
    assert m.load() is True
