# Generated by Django 2.0 on 2020-02-18 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wordoid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='disble_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
