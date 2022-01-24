# Generated by Django 3.0.3 on 2020-06-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regabitur', '0003_auto_20200602_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='work_flag',
            field=models.BooleanField(default=False, verbose_name='Взят в работу:'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(blank=True, default='', max_length=80, verbose_name='Отчество (при наличии)'),
        ),
    ]
