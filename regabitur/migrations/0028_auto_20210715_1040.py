# Generated by Django 3.2.5 on 2021-07-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regabitur', '0027_auto_20210715_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishrectab',
            name='bak_zfo_gp',
            field=models.BooleanField(default=False, verbose_name='БАК ЗФО ГП'),
        ),
        migrations.AlterField(
            model_name='publishrectab',
            name='choice_ege_point',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='История / Английский (Асп. англ тоже сюда)'),
        ),
    ]
