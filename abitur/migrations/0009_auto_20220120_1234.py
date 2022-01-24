# Generated by Django 3.2.5 on 2022-01-20 12:34

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abitur', '0008_auto_20210727_0919'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationalFormSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_educational_form', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='img',
            field=models.ImageField(blank=True, default='pictures/base.jpg', max_length=255, storage=django.core.files.storage.FileSystemStorage(base_url='/uploads', location='/home/oleg/PycharmProjects/abiturient-master/myproject/uploads'), upload_to='image/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='newsfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url='/uploads', location='/home/oleg/PycharmProjects/abiturient-master/myproject/uploads'), upload_to='files', verbose_name='Прикрепить файл'),
        ),
        migrations.CreateModel(
            name='OrdersSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_order', models.CharField(max_length=256, verbose_name='Название')),
                ('number_order', models.CharField(max_length=64, verbose_name='Номер документа')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('date_order', models.DateField(verbose_name='Дата создания приказа')),
                ('file', models.FileField(upload_to='files', verbose_name='Файл')),
                ('educational_form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='linked_orders', to='abitur.educationalformspec', verbose_name='Форма обучения')),
            ],
            options={
                'verbose_name': 'Приказ о зачислении(специалитет)',
                'verbose_name_plural': 'Приказы о зачислении - СПЕЦИАЛИТЕТ',
            },
        ),
    ]