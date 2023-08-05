"""
trionyx_accounts.forms
~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx import forms
from trionyx.forms.helper import FormHelper
from trionyx.forms.layout import Layout, Fieldset, Div
from django.utils.translation import ugettext_lazy as _

from .models import Account, Address, Contact


@forms.register(default_create=True, default_edit=True)
class AccountForm(forms.ModelForm):
    """Account form"""

    class Meta:
        """Form meta"""

        model = Account
        fields = ['type', 'assigned_user', 'name', 'website', 'phone', 'email', 'description', 'billing_address', 'shipping_address']

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            self.fields['billing_address'].queryset = Address.objects.filter(account=self.instance)
            self.fields['shipping_address'].queryset = Address.objects.filter(account=self.instance)
        else:
            self.fields['billing_address'].queryset = Address.objects.filter(account_id=-1)
            self.fields['shipping_address'].queryset = Address.objects.filter(account_id=-1)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    _('General'),
                    Div(
                        Div(
                            'name',
                            css_class='col-md-6'
                        ),
                        Div(
                            'website',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'type',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'phone',
                            css_class='col-md-6'
                        ),
                        Div(
                            'email',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'billing_address',
                            css_class='col-md-6'
                        ),
                        Div(
                            'shipping_address',
                            css_class='col-md-6'
                        ),
                        css_class='row',
                    ),
                    css_class='col-md-6',
                ),
                Fieldset(
                    _('Info'),
                    'assigned_user',
                    'description',
                    css_class='col-md-6',
                ),
            ),
        )


@forms.register(default_create=True, default_edit=True)
class ContactForm(forms.ModelForm):
    """Contact form"""

    account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput())

    class Meta:
        """Form meta"""

        model = Contact
        fields = [
            'account', 'assigned_user', 'first_name', 'last_name', 'email', 'phone',
            'mobile_phone', 'title', 'address', 'description'
        ]

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            self.fields['address'].queryset = Address.objects.filter(account=self.instance.account)
        elif 'account' in self.initial:
            self.fields['address'].queryset = Address.objects.filter(account_id=self.initial['account'])
        elif self.data and 'account' in self.data:
            self.fields['address'].queryset = Address.objects.filter(account_id=self.data['account'])

        self.fields['description'].widget.attrs['rows'] = 3
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'account',
            Div(
                Div(
                    'first_name',
                    css_class='col-md-6'
                ),
                Div(
                    'last_name',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'email',
                    css_class='col-md-6'
                ),
                Div(
                    'title',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'phone',
                    css_class='col-md-6'
                ),
                Div(
                    'mobile_phone',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'address',
                    css_class='col-md-6'
                ),
                Div(
                    'assigned_user',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            'description'
        )


@forms.register(default_create=True, default_edit=True)
class AddressForm(forms.ModelForm):
    """Address form"""

    account = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput())
    default_shipping = forms.BooleanField(label=_('Default shipping'), required=False, initial=False)
    default_billing = forms.BooleanField(label=_('Default billing'), required=False, initial=False)

    class Meta:
        """Form meta"""

        model = Address
        fields = ['account', 'street', 'city', 'postcode', 'country', 'state']

    def __init__(self, *args, **kwargs):
        """Init form"""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            account = self.instance.account
            self.initial['default_shipping'] = self.instance == account.shipping_address
            self.initial['default_billing'] = self.instance == account.billing_address
        elif 'account' in self.initial:
            account = Account.objects.get(id=self.initial['account'])
            if not account.shipping_address:
                self.initial['default_shipping'] = True
            if not account.billing_address:
                self.initial['default_billing'] = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'account',
            'street',
            Div(
                Div(
                    'postcode',
                    css_class='col-md-6'
                ),
                Div(
                    'city',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'state',
                    css_class='col-md-6'
                ),
                Div(
                    'country',
                    css_class='col-md-6'
                ),
                css_class='row',
            ),
            'default_shipping',
            'default_billing'
        )

    def save(self, commit=True):
        """Save model and set default shipping and billing"""
        obj = super().save(commit)

        save_account = False
        if self.cleaned_data['default_shipping']:
            obj.account.shipping_address = obj
            save_account = True

        if self.cleaned_data['default_billing']:
            obj.account.billing_address = obj
            save_account = True

        if save_account:
            obj.account.save(update_fields=['shipping_address', 'billing_address'])
