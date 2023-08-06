import copy
import logging
import pydiscourse
import requests
from pydiscourse import DiscourseClient
from mailman2discourse.retry import retry

logger = logging.getLogger(__name__)


class DiscourseErrorManyMembers(Exception):
    pass


class DiscourseErrorManyGroupMembers(Exception):
    pass


class Discourse(object):

    def __init__(self, args):
        self.args = args

    def connect(self):
        self.d = DiscourseClient(
            self.args.url,
            api_username=self.args.api_user,
            api_key=f'{self.args.api_key}')
        self.about = self.d._get('/about.json')['about']
        logging.info(f'{self.args.url} discourse version {self.about["version"]}')
        return self

    def category_fields(self):
        return ('name', 'id', 'color', 'text_color')

    def category_get(self, name):
        found = [c for c in self.d._get('/categories.json')['category_list']['categories']
                 if c['name'] == name]
        if found:
            return {k: found[0][k] for k in self.category_fields()}
        else:
            return None

    def category_create(self, name):
        category = self.category_get(name)
        if category:
            return category, category
        else:
            category = self.d._post(
                '/categories.json', name=name, color='BF1E2E', text_color='FFFFFF',
                #                   'permissions[everyone]'='1',
                allow_badges='false')['category']
            return None, {k: category[k] for k in self.category_fields()}

    def category_delete(self, name):
        category = self.category_get(name)
        if category:
            self.d._delete(f'/categories/{category["id"]}')
        return category

    def category_set(self, name, **kwargs):
        category = self.category_get(name)
        put_kwargs = {
            'name': name,
            'color': category['color'],
            'text_color': category['text_color'],
        }
        put_kwargs.update(kwargs)
        self.d._put(f'/categories/{category["id"]}', **put_kwargs)

    def settings_set(self, **kwargs):
        keys = kwargs.keys()
        before = self.settings_get(*keys)
        for k, v in kwargs.items():
            self.d._put(f'/admin/site_settings/{k}', **{k: v})
        return before, self.settings_get(*keys)

    def settings_get(self, *names):
        return {
            s['setting']: s['value'] for s in self.d._get('/admin/site_settings')['site_settings']
            if s['setting'] in names
        }

    def group_fields(self):
        return ('name', 'id')

    def group_get(self, name):
        try:
            group = self.d._get(f'/groups/{name}.json')['group']
            return {k: group[k] for k in self.group_fields()}
        except pydiscourse.exceptions.DiscourseClientError:
            return None

    def group_create(self, name):
        group = self.group_get(name)
        if group:
            return group, group
        else:
            kwargs = {
                'group[name]': name,
            }
            group = self.d._post('/admin/groups', **kwargs)['basic_group']
            return None, {k: group[k] for k in self.group_fields()}

    def group_delete(self, name):
        group = self.group_get(name)
        if group:
            self.d._delete(f'/admin/groups/{group["id"]}')
        return group

    def group_member_fields(self):
        return ('id', 'username', 'name', 'owner')

    def group_member_get(self, name, email):
        members = self.d._get(f'/groups/{name}/members.json', filter=email)
        if len(members['members']) == 0:
            return None
        if len(members['members']) > 1:
            raise DiscourseErrorManyGroupMembers(
                f'expected only one member with {email} in group {name} and got {members}')
        if len(members['owners']) > 0:
            member = members['owners'][0]
            member['owner'] = True
        else:
            member = members['members'][0]
            member['owner'] = False
        return {k: member[k] for k in self.group_member_fields()}

    def group_member_create(self, name, email, owner):
        before = self.group_member_get(name, email)
        if not before:
            group = self.group_get(name)
            user = self.user_get(email)
            if owner:
                endpoint = f'/admin/groups/{group["id"]}/owners.json'
                kwargs = {'group[usernames]': user['username']}
            else:
                endpoint = f'/groups/{group["id"]}/members.json'
                kwargs = {'usernames': user['username']}
            self.d._put(endpoint, **kwargs)
            return None, self.group_member_get(name, email)
        if before['owner'] != owner:
            group = self.group_get(name)
            endpoint = f'/admin/groups/{group["id"]}/owners.json'
            if owner:
                kwargs = {
                    'group[usernames]': before['username'],
                }
                self.d._put(endpoint, **kwargs)
            else:
                self.d._delete(endpoint, user_id=before['id'])
            after = copy.deepcopy(before)
            after['owner'] = owner
            return before, after
        return before, before

    def group_member_delete(self, name, email):
        member = self.group_member_get(name, email)
        if member:
            group = self.group_get(name)
            self.d._delete(f'/groups/{group["id"]}/members.json', user_id=member['id'])
        return member

    def user_fields(self):
        return ('username', 'name', 'id', 'email')

    def user_get(self, email):
        user = self.d._get('/admin/users/list/active.json', filter=email, show_emails='true')
        if len(user) == 0:
            return None
        if len(user) > 1:
            raise DiscourseErrorManyMembers(f'expected only one user with {email} and got {user}')
        return {k: user[0][k] for k in self.user_fields()}

    def user_create(self, email, username, password, name):
        user = self.user_get(email)
        if user:
            return user, user
        else:
            kwargs = {
                'email': email,
                'active': True,
                'username': username,
                'password': password,
                'name': name,
                'user_fields[1]': None,
            }
            self.d._post('/users', **kwargs)
            return None, self.user_get(email)

    def user_delete(self, email):
        user = self.user_get(email)
        if user:
            self.d._delete(f'/admin/users/{user["id"]}', delete_posts=True)
        return user

    def topic_delete(self, id):
        self.d._delete(f'/t/{id}')

    def message_load(self, email):
        #
        # There is no convenient way to reverse engineer the /admin/email/handle_mail endpoint
        #
        # https://github.com/discourse/discourse/blob/427d54b2b00fa94474c0522eaed750452c4e7f43/app/controllers/admin/email_controller.rb#L145-L159
        # Which is run by app/jobs/regular/process_email.rb calling Email::Processor.process!
        # Which calls lib/email/processor.rb Email::Receiver.new
        #
        # Errors when processing the queue are found in http://forum.example.com/logs/
        #
        params = {
            'email': email,
            'api_key': self.d.api_key,
            'api_username': self.d.api_username,
        }
        r = requests.post(f'{self.d.host}/admin/email/handle_mail',
                          allow_redirects=False,
                          timeout=self.d.timeout,
                          params=params)
        logger.debug(r.text)
        r.raise_for_status()
        return r

    @retry(AssertionError, tries=5)
    def topic_wait(self, category_name, subject):
        category = self.category_get(category_name)
        kwargs = {
            'term': subject,
            'search_context[type]': 'category',
            'search_context[id]': category["id"],
        }
        r = self.d._get('/search/query', **kwargs)
        assert 'topics' in r
        assert len(r['topics']) > 0
        return r['topics'][0]

    def disconnect(self):
        del self.d
