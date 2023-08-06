import os
import pickle


def mailman_create_config():
    c = {
        'info': 'INFO',
        'archive_private': False,
        # 'default_member_moderation':
        'members': {
        },
        'moderator': {
        },
        'owner': {
        },
        'digest_members': {
        },
        'language': {
        },
        'delivery_status': {
        },
        'user_options': {
        },
        'usernames': {
        },
    }
    return c


def mailman_add(c, email, **kwargs):
    for k, v in (('members', True),
                 ('moderator', False),
                 ('owner', False),
                 ('language', 'en'),
                 ('delivery_status', 0),
                 ('user_options', 0),
                 ('usernames', 'My Name')):
        c[k][email] = kwargs.get(k, v)


def mailman_write_config(d, c):
    os.makedirs(d)
    pickle.dump(c, open(f'{d}/config.pck', 'wb'))
