# Generated by Django 4.2.6 on 2023-11-21 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_studentprofile_student_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='full_name',
            field=models.CharField(default='DefaultValue', max_length=50),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='student_number',
            field=models.CharField(max_length=15),
        ),
    ]