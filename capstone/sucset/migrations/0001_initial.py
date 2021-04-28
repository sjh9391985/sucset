# Generated by Django 3.1.7 on 2021-03-21 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Symbol', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=20)),
                ('Date', models.DateField(verbose_name='finance-date')),
                ('Open', models.IntegerField()),
                ('High', models.IntegerField()),
                ('Low', models.IntegerField()),
                ('Close', models.IntegerField()),
                ('Volume', models.IntegerField()),
                ('Change', models.FloatField()),
            ],
        ),
    ]