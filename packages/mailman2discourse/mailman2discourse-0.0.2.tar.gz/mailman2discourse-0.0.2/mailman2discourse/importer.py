import hashlib
import logging
import mailbox
import os
from mailman2discourse.mailman import Mailman
from mailman2discourse.discourse import Discourse

logger = logging.getLogger(__name__)


class Importer(object):

    def __init__(self, args):
        self.args = args

    def name_get(self):
        return self.mailman.name

    def managers_get(self):
        return [u for u in self.mailman.user.values() if u.get('owner')]

    def members_get(self):
        return self.mailman.user.values()

    def members_add(self, users):
        before = {}
        after = {}
        for user in users:
            email = user['email']
            username = hashlib.md5(email.encode('utf-8')).hexdigest()[:20]
            password = hashlib.md5(os.urandom(16)).hexdigest()[:20]
            try:
                b, after[email] = self.discourse.user_create(
                    email, username, password, user.get('usernames', ''))
            except Exception as e:
                logger.error(f'SKIP user {user} because {e}')
            if b is not None:
                before[email] = b
        return before, after

    def managers_add(self, group_name, users):
        before = {}
        after = {}
        for user in users:
            email = user['email']
            b, after[email] = self.discourse.group_member_create(group_name, email, owner=True)
            if b is not None:
                before[email] = b
        return before, after

    def group_managers_get(self):
        return f'{self.mailman.name}-managers'

    def mbox_load(self, path):
        mbox = mailbox.mbox(path, create=False)
        for k in mbox.keys():
            try:
                msg = mbox.get_message(k).as_bytes(unixfrom=False)
            except Exception as e:
                logging.error(f'mbox_load: {e}')
            self.discourse.message_load(msg)

    def archive_load(self):
        for p in os.listdir(self.args.mailman_archive):
            self.mbox_load(p)

    def importer(self):
        before = {
        }
        after = {
        }
        (before['settings'], after['settings']) = self.discourse.settings_set(
            email_in='true',
            log_mail_processing_failures='true',
            download_remote_images_to_local='true',
            min_post_length='5',
            min_first_post_length='5',
            min_title_similar_length='10240',
            disable_system_edit_notifications='true',
            hide_user_profiles_from_public='true')
        (before['category'], after['category']) = self.discourse.category_create(
            self.name_get())
        logger.debug('Adding members')
        (before['members'], after['members']) = self.members_add(self.members_get())
        logger.debug('Adding managers (owners)')
        (before['group-managers'], after['group-managers']) = self.discourse.group_create(
            self.group_managers_get())
        (before['managers'], after['managers']) = self.managers_add(
            self.group_managers_get(), self.managers_get())
        return before, after

    def init(self):
        self.discourse = Discourse(self.args)
        self.discourse.connect()
        self.mailman = Mailman(self.args)
        self.mailman.load()
        return self

    def main(self):
        self.init()
        self.importer()
        return 0
