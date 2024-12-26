from odoo.tests.common import TransactionCase
from odoo.tests import tagged

# FILE: mrp_quality_workflow/models/test_mrp_quality_check.py

@tagged('post_install', '-at_install')
class TestQualityChecks(TransactionCase):

    def setUp(self):
        super(TestQualityChecks, self).setUp()
        self.MRPProd = self.env['mrp.production']
        self.QualityCheck = self.env['mrp.quality.checkpoint']
        self.StockMove = self.env['stock.move']
        self.Product = self.env['product.product']

        self.finished_product = self.Product.create({
            'name': 'Finished Product',
        })
        self.product = self.Product.create({
            'name': 'Test Product',
        })

        self.move = self.StockMove.create({
            'name': 'Test Move',
            'product_id': self.product.id,
            'location_id': 15,
            'location_dest_id': 8,
            'product_uom_qty': 10,
            'quantity': 10,
        })

        self.MO = self.MRPProd.create({
            'product_id': self.finished_product.id,
            'move_raw_ids': [(6, 0, [self.move.id])],
        })

    def test_compute_state_pass(self):
        quality_check = self.QualityCheck.create({
            'move_id': self.move.id,
            'tolerance': 1.0,
            'measured_value': 10.0,
        })
        quality_check._compute_state()
        self.assertEqual(quality_check.state, 'pass')
        self.assertFalse(quality_check.message)

    def test_compute_state_fail(self):
        quality_check = self.QualityCheck.create({
            'move_id': self.move.id,
            'tolerance': 1.0,
            'measured_value': 12.0,
        })
        quality_check._compute_state()
        self.assertEqual(quality_check.state, 'fail')
        self.assertEqual(quality_check.message,
                         'The measured value is out of tolerance range')

    def test_compute_state_no_measured_value(self):
        quality_check = self.QualityCheck.create({
            'move_id': self.move.id,
            'tolerance': 1.0,
            'measured_value': 0.0,
        })
        quality_check._compute_state()
        self.assertFalse(quality_check.state)
        self.assertFalse(quality_check.message)

    def test_quality_check_pdf_report(self):
        # ctx = {
        #     'model': 'mrp.production',
        #     'active_ids': [self.MO.id],
        # }
        # data_dict = {
        #     'date_from': datetime.today().strftime('%Y-%m-01'),
        #     'emp': [(6, 0, [self.ref('hr.employee_admin')])],
        #     'holiday_type': 'Approved'
        # }
        # self.env.company.external_report_layout_id = self.env.ref(
        #     'web.external_layout_standard').id
        # test_reports.try_report_action(self.env.cr, self.env.uid, 'report_quality_check_pdf',
        #                                wiz_data={}, context=ctx, our_module='mrp_quality_workflow')

        test_record_report = self.env['ir.actions.report'].with_context(
            force_report_rendering=True
        )._render_qweb_pdf(
            'mrp_quality_workflow.report_quality_check_pdf',
            res_ids=self.MO.id
        )
        print("\n ^ a successful test should return 'The PDF report has been generated for model: mrp.production...' \n\n")
        self.assertTrue(
            test_record_report,
            "The PDF should have been generated"
        )
