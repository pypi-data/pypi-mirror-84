"""
trionyx_accounts.models
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from django.conf import settings
from trionyx import models
from trionyx.data import COUNTRIES
from trionyx.config import variables
from django.utils.translation import ugettext_lazy as _

from .conf import settings as app_settings


class AccountType(models.BaseModel):
    """Account type model"""

    name = models.CharField(max_length=128)

    class Meta:
        """Model meta"""

        verbose_name = _('Account type')
        verbose_name_plural = _('Account types')


class Account(models.BaseModel):
    """Account model"""

    type = models.ForeignKey(
        AccountType, models.SET_NULL,
        null=True, blank=True, related_name='accounts', verbose_name=_('Type'))
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        null=True, blank=True, related_name='assigned_accounts', verbose_name=_('Assigned user'))

    name = models.CharField(_('Name'), max_length=255)
    debtor_id = models.CharField(_('Debtor id'), max_length=64, default='', blank=True)
    website = models.URLField(_('Website'), default='', blank=True)
    phone = models.CharField(_('Phone'), max_length=32, default='', blank=True)
    email = models.EmailField(_('Email'), default='', blank=True)
    description = models.TextField(_('Description'), default='', blank=True)

    billing_address = models.ForeignKey(
        'trionyx_accounts.address', models.SET_NULL,
        null=True, blank=True, related_name='+', verbose_name=_('Billing address'))
    shipping_address = models.ForeignKey(
        'trionyx_accounts.address', models.SET_NULL,
        null=True, blank=True, related_name='+', verbose_name=_('Shipping address'))

    class Meta:
        """Model meta"""

        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def save(self, *args, **kwargs):
        """Save account"""
        if not self.debtor_id:
            with variables.get_increment('accounts_account_increment') as increment:
                self.debtor_id = app_settings.DEBTOR_ID_FORMAT.format(
                    increment=increment,
                    increment_long=str(increment).zfill(8),
                )
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class Contact(models.BaseModel):
    """Contact model"""

    account = models.ForeignKey(
        Account, models.CASCADE,
        related_name='contacts', verbose_name=_('Account'))
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL,
        null=True, blank=True, related_name='assigned_contacts', verbose_name=_('Assigned user'))

    first_name = models.CharField(_('First name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255, default='', blank=True)

    email = models.EmailField(_('Email'), default='', blank=True)
    phone = models.CharField(_('Phone'), max_length=32, default='', blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=32, default='', blank=True)
    title = models.CharField(_('Title'), max_length=255, default='', blank=True)
    description = models.TextField(_('Description'), default='', blank=True)

    address = models.ForeignKey(
        'trionyx_accounts.address', models.SET_NULL,
        null=True, blank=True, related_name='+', verbose_name=_('Address'))

    class Meta:
        """Model meta"""

        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def get_absolute_url(self):
        """Get absolute url"""
        return self.account.get_absolute_url()


class Address(models.BaseModel):
    """Address model"""

    account = models.ForeignKey(
        Account, models.CASCADE,
        related_name='addresses', verbose_name=_('Account'))

    street = models.CharField(_('Street'), max_length=255)
    city = models.CharField(_('City'), max_length=255)
    state = models.CharField(_('State'), max_length=255, default='', blank=True)
    postcode = models.CharField(_('Postcode'), max_length=32, default='', blank=True)
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)

    class Meta:
        """Model meta"""

        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def get_absolute_url(self):
        """Get absolute url"""
        return self.account.get_absolute_url()
