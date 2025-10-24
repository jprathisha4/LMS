from django.core.management.base import BaseCommand
from library.models import StudentExtra


class Command(BaseCommand):
    help = 'Regenerate barcodes for all students with the new format including department and year'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration even if barcode already exists',
        )

    def handle(self, *args, **options):
        students = StudentExtra.objects.all()
        force = options['force']
        
        self.stdout.write(f"Found {students.count()} students to process...")
        
        updated_count = 0
        for student in students:
            try:
                # Force regeneration by temporarily setting barcode_value to None
                if force:
                    student.barcode_value = None
                
                # Save will trigger barcode regeneration
                student.save()
                updated_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Regenerated barcode for {student.user.username} "
                        f"(Roll: {student.roll_number}, Dept: {student.department})"
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Failed to regenerate barcode for {student.user.username}: {str(e)}"
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Successfully regenerated barcodes for {updated_count} students!"
            )
        )
        
        if not force:
            self.stdout.write(
                self.style.WARNING(
                    "\n💡 Use --force to regenerate barcodes for students who already have them."
                )
            ) 