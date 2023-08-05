"""
trionyx_accounts.conf
~~~~~~~~~~~~~~~~~~~~~

:copyright: 2020 by Maikel Martens
:license: GPLv3
"""
from trionyx.config import AppSettings

settings = AppSettings('ACCOUNTS', {
    'DEBTOR_ID_FORMAT': '{increment_long}',
})
