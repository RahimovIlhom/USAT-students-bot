# Generated by Django 5.1.3 on 2024-11-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_student_contract_amount_student_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='contract_amount',
            field=models.CharField(max_length=10, verbose_name='Shartnoma summasi'),
        ),
        migrations.AlterField(
            model_name='student',
            name='debt_amount',
            field=models.CharField(max_length=10, verbose_name='Qarz summasi'),
        ),
        migrations.AlterField(
            model_name='student',
            name='paid_amount',
            field=models.CharField(max_length=10, verbose_name="To'langan summasi"),
        ),
        migrations.AlterField(
            model_name='student',
            name='voucher_amount',
            field=models.CharField(max_length=10, verbose_name='Voucher summasi'),
        ),
    ]