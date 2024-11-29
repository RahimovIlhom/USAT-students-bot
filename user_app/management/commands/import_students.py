import pandas as pd
from django.core.management.base import BaseCommand
from education_app.models import EduDirection, EduType
from user_app.models import Student


class Command(BaseCommand):
    help = 'Excel fayldan talabalarni ma\'lumotlar bazasiga import qiladi'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Excel faylning yo\'li')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Excel faylni o'qish
            data = pd.read_excel(file_path)

            # Har bir qatorda iteratsiya qilish
            for _, row in data.iterrows():
                try:
                    # EduDirection va EduType obyektlarini topish
                    edu_direction = EduDirection.objects.get(name=row['Faculty Name'])
                    edu_type = EduType.objects.get(name=row['Type of education'])

                    # Student obyektini yangilash yoki yaratish
                    student, created = Student.objects.update_or_create(
                        passport=row['Passport number'],  # unique identifikator sifatida passportni tanladik
                        defaults={
                            'fullname': row['Full Name'],
                            'pinfl': str(row['PINFL'])[:14],
                            'course': row['Kurs'],
                            'edu_direction': edu_direction,
                            'edu_type': edu_type,
                            'edu_lang': 'uz' if row['Language of education'] == "O'zbek" else 'ru',
                            'contract_amount': str(row['Kontrakt summasi']),
                            'voucher_amount': str(row['VAUCHER']),
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Yangi talaba qo'shildi: {row['Full Name']}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Talaba yangilandi: {row['Full Name']}"))

                except EduDirection.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Xato: Faculty Name topilmadi: {row['Faculty Name']}"))
                except EduType.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Xato: Type of education topilmadi: {row['Type of education']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Xato: {e}"))

            self.stdout.write(self.style.SUCCESS("Talabalar muvaffaqiyatli qo'shildi!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Xatolik yuz berdi: {e}"))
