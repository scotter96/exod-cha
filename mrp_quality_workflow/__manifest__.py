# -*- coding: utf-8 -*-
{
    'name': "mrp_quality_workflow",

    'summary': "Adds a Quality Workflow for Manufacturing Order",

    'description': """
Adds a Quality Workflow for Manufacturing Order as a test for Exo Digital job
    """,

    'author': "Tama",
    'website': "https://scotter96.github.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'product'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'views/mrp_production_views.xml',

        'report/mrp_production_templates.xml',
        'report/mrp_report_views_main.xml',
    ],
}

