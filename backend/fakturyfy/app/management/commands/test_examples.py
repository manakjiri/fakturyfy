from fakturyfy.app.models import Entity
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # see if mi.aw s.r.o. exists:
        if Entity.objects.filter(abbreviation="Mi.aw").exists():
            self.stdout.write(self.style.SUCCESS('Entity "Mi.aw s.r.o." already exists'))
            
        else:

            cat1 = Entity(name="Mi.aw s.r.o.", 
                        abbreviation="Mi.aw", 
                        tax_number="CZ1234567890", 
                        ic_number=1234567890, 
                        address="Pillow 1", 
                        zip_code="12345", 
                        city="Catville", 
                        country="Czech Republic", 
                        bank_account="1234567890", 
                        bank_code="1234", 
                        bank_name="Cat Bank", 
                        tax_note="Poznámka")

            cat1.save()
            self.stdout.write(self.style.SUCCESS('Successfully added entity "%s"' % cat1.name))

        # see if Kitty s.r.o. exists:
        if Entity.objects.filter(abbreviation="Kitty").exists():
            self.stdout.write(self.style.SUCCESS('Entity "Kitty s.r.o." already exists'))
            
        else:
            cat2 = Entity(name="Kitten s.r.o.", 
                        abbreviation="Kitty", 
                        tax_number="CZ0987654321", 
                        ic_number=9876543210, 
                        address="Under desk 13", 
                        zip_code="54321", 
                        city="Catville", 
                        country="Czech Republic", 
                        bank_account="0987654321", 
                        bank_code="4321", 
                        bank_name="Cat Bank", 
                        tax_note="Poznámka")
            
            cat2.save()
            self.stdout.write(self.style.SUCCESS('Successfully added entity "%s"' % cat2.name))