Install
=======

* apt-get install python3-dev python3-pipenv
* pipenv install mailman2discourse

Bulk archive import
===================

When the archives are large, the [mbox
importer](https://lab.enough.community/discourse/mailman2discourse/-/issues/2)
may be used. The first step is to use `mailman2discourse` with an
empty archive directory so that it creates the category matching the
mailing list and creates the users. The `mbox importer` will then
attach the mails to the member matching the email, in the same way
`mailman2discourse` does.

It is safe to import messages multiple times, those with a
`Message-ID` header that is already known to discourse will be ignored.

Conversion
==========

The settings must be modified to activate **email in**.

For a given list (thelist), a discourse category is created by the same name.

The `thelist-managers` group is created, for [moderation
purposes](https://meta.discourse.org/t/category-group-review-moderation/116478). The
group access is set to **Allow users to leave the group freely**.

The `thelist-members` group is created, for membership purposes,
unless the mailing list has public archives and anyone can subscribe
without the approval of a moderator. The group access is set to
**Allow users to leave the group freely**.

The mailing list email (i.e. `thelist@domain`) is set in the **Email** section
of the category settings.

The content of the `config.pck` file describing the mailing list is mapped as follows:

* **info**: copied into the category description
* **archive** is not set or **archive_private** is set: the category
    permissions are modified to restrict access to the members of
    thelist-members. The owners of the `thelist-managers` group are
    made owners of the `thelist-members` group
* **default_member_moderation** is set:
  * **member_moderation_action** is `hold`: `thelist-members` membership access
     is set to **Allow users to send membership requests to group owners**
  * **member_moderation_action** is `discard` or `reject`: `thelist-members` visibility
    is set to **Group owners, members**
* **default_member_moderation** is not set: `thelist-members` membership access
     is set to **Allow users to join the group freely** and the category settings must
     have **Accept emails from anonymous users with no accounts** set in
     the **Email** section.
* **owner**: they are made owners of the `thelist-members` and `thelist-managers` groups
* **moderator**: they are made members of the `thelist-managers` group
* **member**: they are made members of the `thelist-members` group, if the `thelist`
  category is restricted to the members of the `thelist-members` group, because the
  archives of the mailing list are private.
* **delivery_status**: if 0, the user is **Watching** the category. Otherwise it is **Muted**.
* **digest_members**: discarded. It is not possible to request a digest mode
  on a per-category basis.
* **language**: the interface language is set accordingly in the user preference
* **usernames**: discarded. If the subscriber never posted to the
   list, their membership never was public. If the subscriber posted
   to the list, it is possible they used a name that is different
   and do not want the name used to subscribe to the list to be
   made public.

Development
===========

* virtualenv --python=python3 venv
* source venv/bin/activate
* pip install pipenv
* pipenv install --dev
* pipenv run pipenv_to_requirements
* docker rm -f app ; sudo rm -fr discourse_docker/shared ; tests/build-discourse
* echo $(cat discourse_docker/ip) forum.example.com | sudo tee -a /etc/hosts
* firefox http://forum.example.com user: api, password: BefShnygs33SwowCifViwag
* tox

Release management
==================

* Prepare a new version

 - version=1.3.0 ; rm -f inventory/hosts.yml ; perl -pi -e "s/^version.*/version = $version/" setup.cfg ; for i in 1 2 ; do python setup.py sdist ; amend=$(git log -1 --oneline | grep --quiet "version $version" && echo --amend) ; git commit $amend -m "version $version" ChangeLog setup.cfg ; git tag -a -f -m "version $version" $version ; done
 - git push ; git push --tags
 - twine upload -s --username enough --password "$ENOUGH_PYPI_PASSWORD" dist/mailman2discourse-$version.tar.gz
