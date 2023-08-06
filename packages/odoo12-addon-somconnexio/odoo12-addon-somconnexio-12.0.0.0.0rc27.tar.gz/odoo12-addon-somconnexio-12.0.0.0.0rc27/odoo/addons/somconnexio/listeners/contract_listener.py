from odoo.addons.component.core import Component


class Contract(Component):
    _name = 'contract.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['contract.contract']

    def on_record_create(self, record, fields=None):
        self.env['contract.contract'].with_delay().create_subscription(record.id)

    def on_record_write(self, record, fields=None):
        if record.is_terminated:
            self.env['contract.contract'].with_delay().terminate_subscription(record.id)
