# Generated by Django 3.2.6 on 2021-08-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stepautomationapp', '0003_alter_userdata_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='profilepic',
            field=models.ImageField(default='/media/profilepic.png', upload_to='media'),
        ),
    ]