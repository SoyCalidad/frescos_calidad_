from odoo import models, fields, api
from odoo.exceptions import UserError

class PopularityTableWizard(models.TransientModel):
    _name = 'product.popularity.table.wizard'
    _description = 'Products Popularity Table'

    def generate_report(self):
        self.ensure_one()
        products = self.env['product.template'].search([('sales_count', '>', 0)])

        return self.env.ref('frescos_inventory_customizations.report_popularity_table_xlsx').report_action(products)

class ProductPopularityXlsxReport(models.AbstractModel):
    _name = 'report.report_product_popularity_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Product Popularity Report'

    def generate_xlsx_report(self, workbook, data, records):
        sorted_records = sorted(records, key=lambda product: product.sales_count, reverse=True)

        sheet = workbook.add_worksheet('Product Popularity')
        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 20)

        sheet.write(0, 0, 'Product Name', workbook.add_format({'bold': True}))
        sheet.write(0, 1, 'Number of Sales', workbook.add_format({'bold': True}))

        row = 1
        for product in sorted_records:
            sheet.write(row, 0, product.name)
            sheet.write(row, 1, product.sales_count)
            row += 1