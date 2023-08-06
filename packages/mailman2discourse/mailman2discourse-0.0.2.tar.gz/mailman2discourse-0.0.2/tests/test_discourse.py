import pytest
import time
from mailman2discourse import discourse


def test_connect(test_options):
    d = discourse.Discourse(test_options).connect()
    assert 'version' in d.about


def test_category(test_options):
    d = discourse.Discourse(test_options).connect()
    name = 'ABCD'
    before0, after0 = d.category_create(name)
    assert before0 is None
    assert after0['name'] == name
    before1, after1 = d.category_create(name)
    assert after0 == before1
    assert before1 == after1

    assert d.category_delete(name)['id'] == after1['id']
    assert d.category_delete(name) is None


def test_category_set(test_options):
    d = discourse.Discourse(test_options).connect()
    name = 'CATEGORYNAME'
    try:
        _, category = d.category_create(name)
        assert category['name'] == name
        color = '112233'
        d.category_set(name, color=color)
        category = d.category_get(name)
        assert category['color'] == color
    finally:
        d.category_delete(name)


def test_group(test_options):
    d = discourse.Discourse(test_options).connect()
    name = 'GROUPNAME'
    before0, after0 = d.group_create(name)
    assert before0 is None
    assert after0['name'] == name
    before1, after1 = d.group_create(name)
    assert after0 == before1
    assert before1 == after1

    assert d.group_delete(name)['id'] == after1['id']
    assert d.group_delete(name) is None


@pytest.mark.parametrize("email", [
    'user@example.com',
    'some+else@test.com',  # + must be quoted otherwise it fails
])
def test_user(test_options, email):
    d = discourse.Discourse(test_options).connect()
    password = 'dashkeedfakojfiesMob'
    before0, after0 = d.user_create(email, 'MYUSERNAME', password, 'Display Name')
    assert before0 is None
    assert after0['email'] == email
    before1, after1 = d.user_create(email, 'MYUSERNAME', password, 'Display Name')
    assert after0 == before1
    assert before1 == after1

    assert d.user_delete(email)['id'] == after1['id']
    assert d.user_delete(email) is None


def test_group_member(test_options):
    try:
        d = discourse.Discourse(test_options).connect()
        email = 'user@example.com'
        password = 'dashkeedfakojfiesMob'
        username = 'MYUSERNAME'
        _, user = d.user_create(email, username, password, 'Display Name')
        group_name = 'GROUPNAME'
        _, group = d.group_create(group_name)

        #
        # Verify idempotence with owner=False
        #
        before0, after0 = d.group_member_create(group_name, email, owner=False)
        assert before0 is None
        assert after0['username'] == username
        before1, after1 = d.group_member_create(group_name, email, owner=False)
        assert after0 == before1
        assert before1 == after1

        #
        # Modify owner to True
        #
        before2, after2 = d.group_member_create(group_name, email, owner=True)
        assert before2['id'] == after2['id']
        assert before2['owner'] is False
        assert after2['owner'] is True
        #
        # Modify owner to False
        #
        before3, after3 = d.group_member_create(group_name, email, owner=False)
        assert before3['id'] == after3['id']
        assert before3['owner'] is True
        assert after3['owner'] is False

        #
        # Delete
        #
        assert d.group_member_delete(group_name, email)['id'] == after1['id']
        assert d.group_member_delete(group_name, email) is None

        #
        # Added with owner=True
        #
        before0, after0 = d.group_member_create(group_name, email, owner=True)
        assert before0 is None
        assert after0['username'] == username

    finally:
        d.group_delete(group_name)
        d.user_delete(email)


def test_settings(test_options):
    d = discourse.Discourse(test_options).connect()
    _, after0 = d.settings_set(email_in='false',
                               download_remote_images_to_local='false')
    assert after0['email_in'] == 'false'
    assert after0['download_remote_images_to_local'] == 'false'
    before1, after1 = d.settings_set(email_in='true',
                                     download_remote_images_to_local='true')
    assert after0 == before1
    assert after1['email_in'] == 'true'
    assert after1['download_remote_images_to_local'] == 'true'


def test_message_load(test_options):
    topic = None
    email = 'user@example.com'
    category_name = 'CATNAME'
    try:
        d = discourse.Discourse(test_options).connect()
        password = 'dashkeedfakojfiesMob'
        username = 'MYUSERNAME'
        _, user = d.user_create(email, username, password, 'Display Name')
        _, category = d.category_create(category_name)
        email_in = 'list@example.com'
        d.settings_set(email_in='true',
                       log_mail_processing_failures='true',
                       email_in_min_trust='0',
                       min_post_length='5',
                       min_first_post_length='5',
                       min_title_similar_length='10240')
        d.category_set(category_name,
                       email_in=email_in,
                       email_in_allow_strangers='true')
        subject = 'MESSAGE ONE'
        message = f"""From user@example.com  Mon Nov  9 21:54:11 1999
Message-ID: <msg@{time.time()}>
From: "Some One" <user@example.com>
To: <list@example.com>
Date: Fri,  6 Apr 2007 15:43:55 -0700 (PDT)
Subject: {subject} {time.time()}

First content
        """
        assert 'email has been received' in d.message_load(message).text
        topic = d.topic_wait(category_name, subject)
    finally:
        if topic:
            d.topic_delete(topic['id'])
        d.user_delete(email)
        d.category_delete(category_name)
        d.settings_set(email_in='false')
