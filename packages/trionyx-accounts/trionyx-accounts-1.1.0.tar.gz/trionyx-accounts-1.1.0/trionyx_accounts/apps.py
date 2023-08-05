"""
trionyx_accounts.apps
~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx.trionyx.apps import BaseConfig
from django.utils.translation import ugettext_lazy as _


def get_add_address_url(obj, context):
    """Get add address url"""
    from trionyx.urls import model_url
    return model_url('trionyx_accounts.address', 'dialog-create', params={
        'account': obj.id,
    })


class AccountsConfig(BaseConfig):
    """Django core config app"""

    name = 'trionyx_accounts'
    verbose_name = 'Accounts'

    class Account:
        """Account config"""

        verbose_name = '{name}'
        menu_root = True
        menu_icon = 'fa  fa-building'
        menu_name = 'Accounts'
        menu_order = 5

        list_default_fields = ['type', 'name', 'website', 'email', 'phone', 'debtor_id']

        header_buttons = [
            {
                'label': _('Add Address'),
                'url': get_add_address_url,
                'show': lambda obj, context: context.get('page') == 'view' and context.get('tab') == 'general',
                'dialog': True,
                'dialog_options': {
                    'callback': "function(data, dialog) { if (data.success) { trionyx_reload_tab('general'); dialog.close(); } }",
                }
            }
        ]

    class AccountType:
        """Account type config"""

        verbose_name = '{name}'
        disable_search_index = True
        menu_exclude = True

    class Contact:
        """Contact config"""

        verbose_name = '{first_name} {last_name}'
        menu_exclude = True

    class Address:
        """Address config"""

        verbose_name = '{street}, {city}, {postcode}'
        menu_exclude = True
        disable_search_index = True
