# Generated by Django 4.2 on 2024-07-04 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_useraccount_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='プロフィール画像'),
        ),
    ]
