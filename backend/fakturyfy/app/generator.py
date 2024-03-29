import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
from InvoiceGenerator.api import Invoice, Item, Creator, Client, Provider
from InvoiceGenerator.pdf import ProformaInvoice
from fakturyfy.app.models import Entity
from fakturyfy.app.serializers import NewInvoiceRequest, RequestItem

os.environ["INVOICE_LANG"] = "cs"

class InvoiceExporter:
    def __init__(self, number: str, provider: Entity, client: Entity, item_list: list[RequestItem]) -> None:
        
        self.provider = Provider(
            provider.name,
            address=provider.address,
            city=provider.city,
            zip_code=provider.zip_code,
            country=provider.country,
            phone=provider.phone,
            email=provider.email,
            bank_name=provider.bank_name,
            bank_account=provider.bank_account,
            bank_code=provider.bank_code,
            ir=provider.ic_number,
            vat_id=provider.tax_number,
            note=provider.tax_note,
            logo_filename=provider.logo.path if provider.logo else None
        )

        self.client = Client(
            client.name,
            address=client.address,
            city=client.city,
            zip_code=client.zip_code,
            country=client.country,
            phone=client.phone,
            email=client.email,
            bank_name=client.bank_name,
            bank_account=client.bank_account,
            bank_code=client.bank_code,
            ir=client.ic_number,
            vat_id=client.tax_number,
        )
        
        self.number = str(number)
        self.item_list = item_list
        self.date = datetime.now()
        self.payback = self.date + relativedelta(months=1)
        self.date_format = '%d.%m.%Y'
        self.currency = 'Kč'

    def set_date(self, date: datetime) -> None:
        self.date = date
    
    def set_payback(self, payback: datetime) -> None:
        self.payback = payback

    def as_pdf(self, target_dir: Path = Path(__file__).parent.parent, prefix: str = 'faktura') -> Path:
        target_dir = Path(target_dir)
        assert target_dir.is_dir()

        creator = Creator(self.provider.summary)
        invoice = Invoice(self.client, self.provider, creator)
        
        invoice.currency_locale = 'cs_CZ.UTF-8'
        invoice.currency = self.currency

        for item in self.item_list:
            invoice.add_item(Item(
                description=item.description,
                count=item.quantity,
                price=item.price,
                tax=item.tax,
                unit='ks'
            ))

        number = str(self.date.year) + self.number

        invoice.number = number
        invoice.variable_symbol = number
        invoice.date = self.date.strftime(self.date_format)
        invoice.taxable_date = invoice.date
        invoice.paytype = 'převod'
        invoice.use_tax = any([item.tax > 0 for item in invoice.items])
        invoice.payback = self.payback.strftime(self.date_format)
        
        document = ProformaInvoice(invoice)
        path = target_dir / f'{prefix}_{number}.pdf'
        document.gen(str(path), generate_qr_code=True)
        return path


def generate_invoice(number: int, request: NewInvoiceRequest, target_dir: Path) -> Path:
    target_dir = Path(target_dir)
    target_dir.mkdir(exist_ok=True, parents=True)
    
    exporter = InvoiceExporter(number, request.provider, request.client, request.item_list)
    exporter.set_date(request.date)
    exporter.set_payback(request.paydate)
    
    return exporter.as_pdf(target_dir)

