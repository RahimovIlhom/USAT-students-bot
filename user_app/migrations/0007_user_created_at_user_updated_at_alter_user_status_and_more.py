# Generated by Django 5.1.3 on 2024-11-30 04:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_alter_student_edu_direction_alter_student_edu_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Yaratilgan vaqti'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Oxirgi yangilangan vaqti'),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Qoralama'), ('PHONE_INPUT', 'Telefon raqamini kiritish'), ('PASSPORT_INPUT', 'Pasport maʼlumotlarini kiritish'), ('CONFIRMATION', 'Tasdiqlash'), ('EDIT', 'Tahrirlash'), ('COMPLETED', 'Tugatildi'), ('BLOCKED', 'Bloklangan')], default='DRAFT', max_length=15, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Telegram ID'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['tg_id'], name='users_tg_id_e19202_idx'),
        ),
    ]