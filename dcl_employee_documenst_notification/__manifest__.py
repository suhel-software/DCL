# -*- coding: utf-8 -*-
{
    'name': 'DCL Employee Documents Notification',
    'version': '16.0.1.0.0',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': """Manages Employee Related Documents with Expiry Notifications. Standalone custom edition.""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Imran Hoque',
    'depends': ['base', 'hr', 'hr_contract'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/document_type_data.xml',
        'views/employee_document_view.xml',
        'views/document_type_view.xml',
        'views/hr_document_template.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
