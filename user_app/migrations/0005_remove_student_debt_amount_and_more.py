# Generated by Django 5.1.3 on 2024-11-29 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_alter_student_contract_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='debt_amount',
        ),
        migrations.RemoveField(
            model_name='student',
            name='paid_amount',
        ),
    ]
