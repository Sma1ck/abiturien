# Generated by Django 3.2.5 on 2021-07-13 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regabitur', '0019_auto_20210628_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='message',
            field=models.CharField(blank=True, default=' ', max_length=512, verbose_name='Сообщение от приемной комисии'),
        ),
        migrations.CreateModel(
            name='PublishRecTab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(choices=[('ЕГЭ', 'ЕГЭ'), ('Вступительные испытания', 'Вступительные испытания')], max_length=256, verbose_name='Вступительные испытания')),
                ('date_pub', models.DateTimeField(auto_now=True, null=True)),
                ('obsh_point', models.SmallIntegerField(blank=True, verbose_name='Обществознание')),
                ('tgp_point', models.SmallIntegerField(blank=True, verbose_name='Теор. Гос-ва и Права')),
                ('okp_point', models.SmallIntegerField(blank=True, verbose_name='ОКП РФ')),
                ('gp_point', models.SmallIntegerField(blank=True, verbose_name='ГП')),
                ('up_point', models.SmallIntegerField(blank=True, verbose_name='УП')),
                ('rus_point', models.SmallIntegerField(blank=True, verbose_name='Конст. Право РФ')),
                ('spec_point', models.SmallIntegerField(blank=True, verbose_name='Спец. дисциплина (Асп)')),
                ('bak_ofo_up', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ОФО УП')),
                ('bak_ofo_gp', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ОФО ГП')),
                ('bak_zfo_up', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ЗФО УП')),
                ('bak_zfo_gp', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ЗФО ГП')),
                ('bak_ozfo_up', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ОЗФО УП')),
                ('bak_ozfo_gp', models.BooleanField(default=False, verbose_name='ЕГЭ в БАК ОЗФО ГП')),
                ('vstupit_bak_ofo_up', models.BooleanField(default=False, verbose_name='Вступительные в БАК ОФО УП')),
                ('vstupit_bak_ofo_gp', models.BooleanField(default=False, verbose_name='Вступительные в БАК ОФО ГП')),
                ('vstupit_bak_zfo_up', models.BooleanField(default=False, verbose_name='Вступительные в БАК ЗФО УП')),
                ('vstupit_bak_zfo_gp', models.BooleanField(default=False, verbose_name='Вступительные в БАК ЗФО ГП')),
                ('vstupit_bak_ozfo_up', models.BooleanField(default=False, verbose_name='Вступительные в БАК ОЗФО УП')),
                ('vstupit_bak_ozfo_gp', models.BooleanField(default=False, verbose_name='Вступительные в БАК ОЗФО ГП')),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='publishRec', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
