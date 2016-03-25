#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Try to clean up your fucking Gmail by deleting 1 at a time.

Hard-coded to delete by sender right now. If you want to delete by something
else, Google it.

Also, it sometimes crashes for random reasons but usually will end up deleting
10s of thousands of emails before that happens.

How this works
==============

1. Make sure you change the settings in your Gmail inbox like so:

    http://stackoverflow.com/a/5366205

2. Update UNWANTED_SENDER with the email address of the sender you want to
   delete.

3. Update USERNAME with your Gmail address.

4. Update PASSWORD with your Gmail password. If you have two-step
   authentication enabled, you'll need to create a new application password and
   use that here.

5. Run it like so::

    $ ./gmail_cleaner.py
"""

from __future__ import unicode_literals, print_function
import imaplib
import sys


__author__ = 'Jathan McCollum'
__email__ = 'jathan@gmail.com'
__version__ = '0.5'


# Who we want to kill
UNWANTED_SENDER = 'fake@notreal'

# Credentials. If you have two-step authentication enabled, you're going to use
# your application password here.
USERNAME = 'you@gmail.com'
PASSWORD = 'bogus'

# How many messages to delete between expunges
BATCH_SIZE = 100

# Upper limit for batches
UPPER_LIMIT = 1000


def login(username=USERNAME, password=PASSWORD):
    print('Logging in as %s' % username)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')  # Connect to inbox.
    return mail


def get_message_ids(mail, sender, reverse_order=True):
    print('Searching for emails from: %s' % sender)

    query = '(HEADER From "%s")' % sender
    result = mail.uid('search', None, query)
    status, ids = result
    id_list = ids[0].split()  # ids is a string in a list WTF?

    if reverse_order:
        id_list = id_list[::-1]

    print('Got %s messages' % len(id_list))

    return id_list


def delete_messages(mail, id_list, batch_size=50, upper_limit=1000):
    total_counter = 1
    counter = 1

    while id_list:
        msg_id = id_list.pop(0)
        try:
            mail.uid('store', msg_id, '+FLAGS', '(\\Deleted)')
            # mail.store(msg_id, '+FLAGS', '\\Deleted')
        except:
            print ('Error deleting msg %s. Resetting mailbox.' % msg_id)
            return False
        print('DELETED message %s' % msg_id)

        counter += 1
        total_counter += 1
        if counter >= batch_size:
            print('%s messages hit; EXPUNGING!' % batch_size)
            print('%s messages deleted so far.' % total_counter)
            try:
                mail.expunge()
            except:
                print('Got an error while expunging. Resetting mailbox.')
                return False
            else:
                counter = 1

        if total_counter >= upper_limit:
            print('Upper limit of %s reached. Starting over.' % upper_limit)
            return False  # Force exit.

    return True


def logout(mail):
    print('Final expunge.')
    try:
        mail.expunge()
        mail.close()
        mail.logout()
    except Exception as err:
        print('Unexpected while logging out. Error: %s' % err)
        rv = False
    else:
        print('Done. Closing connection and logging out.')
        rv = True

    print('All done.')
    return rv


def delete_batch(batch_size=50, upper_limit=1000):
    """Get a mailbox, search and delete shit."""
    ok = False
    mail = None
    try:
        mail = login()
        sender = UNWANTED_SENDER
        id_list = get_message_ids(mail, sender)
        ok = delete_messages(
            mail, id_list, batch_size=batch_size, upper_limit=upper_limit
        )
    except KeyboardInterrupt:
        sys.exit('Ctrl-C detected. Exiting...')
    finally:
        if mail is None:
            ok = False
        else:
            try:
                ok = logout(mail)
            except:
                ok = False

    print('Batch done.')
    return ok


if __name__ == '__main__':
    batch_count = 1
    batch_size = 10
    upper_limit = 100
    ok = delete_batch(batch_size=batch_size, upper_limit=upper_limit)
    while ok:
        try:
            ok = delete_batch(batch_size=batch_size, upper_limit=upper_limit)
            batch_count += 1
        finally:
            print('Completed %s batches.' % batch_count)
