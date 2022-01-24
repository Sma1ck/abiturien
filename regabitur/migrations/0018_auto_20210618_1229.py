# Generated by Django 3.2.3 on 2021-06-18 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regabitur', '0017_auto_20210618_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_of_doc',
            field=models.CharField(default=' ', max_length=32, verbose_name='Дата выдачи документа об образовании в формате ДД.ММ.ГГГГ'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='snils',
            field=models.CharField(default=' ', max_length=32, verbose_name='Номер снилса'),
        ),
    ]