"""
trionyx_accounts.layouts
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: 2019 by Maikel Martens
:license: GPLv3
"""
from trionyx.views import tabs
from trionyx.layout import Container, Row, Column3, Column9, Panel, DescriptionList, Html, Button, Table, ButtonGroup, Component
from django.utils.translation import ugettext_lazy as _

from .models import Account, Contact


@tabs.register(Account)
def order_general(obj):
    """Account general tab"""
    return Container(
        Row(
            Column9(
                Panel(
                    _('General'),
                    DescriptionList(
                        'name',
                        'type',
                        'debtor_id',
                        'website',
                        'phone',
                        'email',
                        {
                            'label': _('Shipping address'),
                            'value': str(obj.shipping_address),
                        } if obj.shipping_address else None,
                        {
                            'label': _('Billing address'),
                            'value': str(obj.billing_address),
                        } if obj.billing_address else None,
                    )
                ),
                Panel(
                    _('Info'),
                    DescriptionList(
                        'assigned_user',
                        'description',
                    )
                ),
                Panel(
                    Component(
                        ButtonGroup(
                            Button(
                                '<i class="fa fa-plus"></i>',
                                model_url='dialog-create',
                                model_params={
                                    'account': obj.id,
                                },
                                dialog=True,
                                dialog_reload_tab='general',
                                css_class='btn btn-flat btn-success btn-xs',
                                object=Contact(),
                            ),
                            css_class='btn-group pull-right',
                        ),
                        Html(_('Contacts')),
                    ),
                    Table(
                        obj.contacts.all(),
                        'title',
                        'first_name',
                        'last_name',
                        'email',
                        'phone',
                        'mobile_phone',
                        {
                            'field': 'address',
                            'renderer': lambda value, **options: str(value) if value else '',
                        },
                        'description',
                        'assigned_user=width:100px',
                        {
                            'label': _('Options'),
                            'width': '80px',
                            'value': ButtonGroup(
                                Button(
                                    label='<i class="fa fa-edit"></i>',
                                    model_url='dialog-edit',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                    css_class='btn btn-flat bg-theme btn-sm'
                                ),
                                Button(
                                    label='<i class="fa fa-times"></i>',
                                    model_url='dialog-delete',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                    css_class='btn btn-flat btn-danger btn-sm'
                                ),
                            )
                        },
                    )
                )
            ),
            Column3(
                *[
                    Panel(
                        Component(
                            ButtonGroup(
                                Button(
                                    label='<i class="fa fa-edit"></i>',
                                    model_url='dialog-edit',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                    css_class='btn btn-flat bg-theme btn-xs',
                                    object=address,
                                ),
                                Button(
                                    label='<i class="fa fa-times"></i>',
                                    model_url='dialog-delete',
                                    model_params={
                                        'account': obj.id,
                                    },
                                    dialog=True,
                                    dialog_reload_tab='general',
                                    css_class='btn btn-flat btn-danger btn-xs',
                                    object=address,
                                ),
                                css_class='btn-group pull-right',
                            ),
                            Html(_('Address'))
                        ),
                        DescriptionList(
                            'street',
                            'postcode',
                            'city',
                            'state',
                            'country',
                            {
                                'label': _('Default shipping'),
                                'value': True
                            } if address == obj.shipping_address else None,
                            {
                                'label': _('Default billing'),
                                'value': True
                            } if address == obj.billing_address else None,
                            object=address,
                        ),
                        object=address,
                    ) for address in obj.addresses.all()
                ]
            ),
        ),
    )
