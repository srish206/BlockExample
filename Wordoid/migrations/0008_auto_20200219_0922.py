# Generated by Django 2.0 on 2020-02-19 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wordoid', '0007_auto_20200219_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('like', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='Wordoid.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name', to='Wordoid.UserProfile'),
        ),
    ]
