# Generated by Django 3.0.5 on 2020-05-05 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlist', '0002_remove_userlist_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlist',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]