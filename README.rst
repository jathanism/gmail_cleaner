#############
gmail_cleaner
#############

Try to clean up your fucking Gmail by deleting 1 at a time.

It's hard-coded to delete by sender right now. If you want to delete by something
else, Google it.

Also, it sometimes crashes for random reasons but usually will end up deleting
10s of thousands of emails before that happens.

How this works
==============

1. Make sure you change the settings in your Gmail inbox like so:

    http://stackoverflow.com/a/5366205

2. Update ``UNWANTED_SENDER`` with the email address of the sender you want to
   delete.

3. Update ``USERNAME`` with your Gmail address.

4. Update ``PASSWORD`` with your Gmail password. If you have two-step
   authentication enabled, you'll need to create a new application password and
   use that here.

5. Run it like so::

    $ ./gmail_cleaner.py

Coming Soon
===========

- Arg parsing.
- Features.
- Just kidding, whatever.
