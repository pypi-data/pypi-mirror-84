from mailman2discourse import importer
from tests.helpers_mailman import (
    mailman_write_config,
    mailman_create_config,
    mailman_add)


def test_main(test_options, tmpdir):
    n = 'listname'
    mailman_write_config(f'{tmpdir}/{n}', mailman_create_config())
    test_options.list = n
    test_options.mailman_dir = str(tmpdir)
    i = importer.Importer(test_options)
    assert i.main() == 0
    assert i.discourse.category_get(i.name_get()) is not None
    assert i.discourse.group_get(i.group_managers_get()) is not None
    i.discourse.group_delete(i.group_managers_get())
    i.discourse.category_delete(i.name_get())


def test_importer(test_options, tmpdir):
    try:
        n = 'listname'
        c = mailman_create_config()
        email = 'someone@example.com'
        mailman_add(c, email, owner=True)
        mailman_write_config(f'{tmpdir}/{n}', c)
        test_options.list = n
        test_options.mailman_dir = str(tmpdir)
        i = importer.Importer(test_options).init()
        before0, after0 = i.importer()
        assert before0['category'] is None
        assert before0['managers'] == {}
        assert before0['members'] == {}
        assert before0['group-managers'] is None
        assert 'email_in' in before0['settings']

        assert after0['category']['name'] == n
        assert after0['settings']['email_in'] == 'true'
        assert after0['group-managers']['name'].startswith(n)
        assert email in after0['managers']
        before1, after1 = i.importer()
        assert before1 == after0
        assert before1 == after1
    finally:
        i.discourse.group_delete(i.group_managers_get())
        i.discourse.category_delete(i.name_get())
        i.discourse.user_delete(email)
