import logging
import os
import pickle

logger = logging.getLogger(__name__)


class MailmanUnpickler(pickle.Unpickler):

    class Noop:
        pass

    def find_class(self, module, name):
        logger.debug(f'{module} {name}')
        if name == '_Bouncer._BounceInfo':
            return MailmanUnpickler.Noop
        if name == '_BounceInfo':
            return MailmanUnpickler.Noop
        return super().find_class(module, name)


class ErrorMailmanNotFound(Exception):
    pass


class Mailman(object):

    def __init__(self, args):
        self.args = args

    @staticmethod
    def moderation_action_mapping(value):
        # Convert the member_moderation_action option to an Action enum.
        # The values were: 0==Hold, 1==Reject, 2==Discard
        return {
            0: 'approval',
            1: 'ignore',
            2: 'ignore',
            }[value]

    def load(self):
        self.name = self.args.list
        p = f'{self.args.mailman_dir}/{self.name}/config.pck'
        if not os.path.exists(p):
            raise ErrorMailmanNotFound(f'{p} not found, skipping')
        c = MailmanUnpickler(open(p, 'rb'), encoding=self.args.mailman_encoding).load()

        self.info = {
            'private': c['archive_private'],
            'info': c['info'],
        }
        if bool(c.get('default_member_moderation', 0)):
            self.info['moderation'] = self.moderation_action_mapping(
                c['default_member_moderation'])
        else:
            c['moderation'] = 'no'
        self.user = {}
        for email in c['members']:
            self.user[email] = {'email': email}
        for k in ('moderator', 'owner'):
            for email in c[k]:
                self.user.setdefault(email, {'email': email})[k] = True
        for email in c['digest_members']:
            if email not in self.user:
                logger.error(f'SKIP digest_members for unknown user {email}')
                continue
            self.user[email]['digest'] = True
        for k in ('language', 'usernames', 'delivery_status', 'user_options'):
            for email, value in c[k].items():
                if email not in self.user:
                    logger.error(f'SKIP {k} for unknown user {email}')
                    continue
                self.user[email][k] = value
        return True
