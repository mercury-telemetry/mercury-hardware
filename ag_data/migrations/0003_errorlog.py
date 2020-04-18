# Generated by Django 2.2.11 on 2020-04-18 19:15

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ag_data', '0002_agactiveevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('error_code', models.CharField(choices=[('UNKNOWN_FORMAT', 'Unknown Format'), ('MISSING_COLUMN', 'Missing Column'), ('MISSING_FIELD_IN_RAW_READING', 'Missing Field In Raw Reading'), ('INVALID_COLUMN_NAME', 'Invalid Column Name'), ('INVALID_COLUMN_VALUE', 'Invalid Column Value'), ('INVALID_FIELD_IN_RAW_READING', 'Invalid Field In Raw Reading'), ('FORMULA_PROCESS_MEASUREMENT_ERROR', 'Error When Formula Processing Measurement'), ('EXTRANEOUS_KEY_VALUE_PAIR_IN_MEASUREMENT', 'Extraneous Key-Value Pair In Measurement'), ('OTHER_ERROR', 'Other Error')], default='OTHER_ERROR', max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('raw_data', models.CharField(max_length=256)),
            ],
        ),
    ]
