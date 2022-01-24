# Generated by Django 3.1.3 on 2021-04-08 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regabitur', '0007_auto_20210405_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='additionalinfo',
            options={'verbose_name': 'Профиль обучения', 'verbose_name_plural': 'Профили обучения'},
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='PublishTab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual_str', models.CharField(blank=True, max_length=32)),
                ('test_type', models.CharField(choices=[('ЕГЭ', 'ЕГЭ'), ('Вступительные испытания', 'Вступительные испытания')], max_length=256, verbose_name='Вступительные испытания')),
                ('bac_ofo', models.BooleanField(default=False, verbose_name='Опубликовать в БАК ОФО')),
                ('bac_zfo', models.BooleanField(default=False, verbose_name='Опубликовать в БАК ЗФО')),
                ('bac_ozfo', models.BooleanField(default=False, verbose_name='Опубликовать в БАК ОЗФО')),
                ('mag_ofo', models.BooleanField(default=False, verbose_name='Опубликовать в МАГ ОФО')),
                ('mag_zfo', models.BooleanField(default=False, verbose_name='Опубликовать в МАГ ЗФО')),
                ('asp_ofo', models.BooleanField(default=False, verbose_name='Опубликовать в АСП ОФО')),
                ('asp_zfo', models.BooleanField(default=False, verbose_name='Опубликовать в АСП ЗФО')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Опубликовать в списки подавших',
                'verbose_name_plural': 'Опубликовать в списки подавших',
            },
        ),
    ]
