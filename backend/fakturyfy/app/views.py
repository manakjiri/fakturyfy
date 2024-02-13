from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from fakturyfy.app import models, serializers
from fakturyfy.app.generator import generate_invoice
from fakturyfy.app.history import History
from fakturyfy.settings import DATA_DIR


def index(request, page="index"):
    # TODO add 404 to non-existing pages
    return render(request, "index.html")

class EntityViewSet(viewsets.ModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer


class NewInvoice(APIView):
    def post(self, request: Request):
        new_invoice_serializer = serializers.NewInvoiceSerializer(data=request.data)
        if new_invoice_serializer.is_valid():
            request: serializers.NewInvoiceRequest = new_invoice_serializer.save()
            
            history = History(request.provider.abbreviation, request.client.abbreviation, request.date.year)
            number = str(request.client.pk).zfill(2) + str(history.get_count() + 1).zfill(2)
            
            tmp_dir = DATA_DIR / 'tmp'
            if not tmp_dir.exists():
                tmp_dir.mkdir(parents=True)
            else:
                for file in tmp_dir.iterdir():
                    file.unlink()

            invoice = generate_invoice(number, request, tmp_dir)

            if request.save:
                history.base_dir.mkdir(exist_ok=True, parents=True)
                invoice = invoice.rename(history.base_dir / invoice.name)
            
            return Response({'path': str(invoice.relative_to(DATA_DIR))})
        
        else:
            return Response({'error': new_invoice_serializer.errors})

class ListInvoices(APIView):
    def get(self, request: Request):
        get_invoices_serializer = serializers.GetInvoicesSerializer(data=request.query_params)
        if not get_invoices_serializer.is_valid():
            return Response({'error': get_invoices_serializer.errors})
        
        request: serializers.GetInvoicesRequest = get_invoices_serializer.save()
        providers = [models.Entity.objects.get(pk=request.provider_id)] if request.provider_id else models.Entity.objects.all()
        clients = [models.Entity.objects.get(pk=request.client_id)] if request.client_id else models.Entity.objects.all()
        ret = []
        
        for p in providers:
            for c in clients:
                history = History(p.abbreviation, c.abbreviation, 'all')
                for invoice in history.get_all():
                    ret.append({
                        'path': str(invoice.relative_to(DATA_DIR)),
                        'name': invoice.name,
                        'provider': p.abbreviation,
                        'client': c.abbreviation,
                        'modify_time': int(invoice.stat().st_mtime)
                    })
        
        return Response(sorted(ret, key=lambda x: x['modify_time'], reverse=True))
