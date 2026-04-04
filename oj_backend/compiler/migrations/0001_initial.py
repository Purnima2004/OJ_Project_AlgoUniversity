from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('python', 'Python'), ('cpp', 'C++'), ('java', 'Java')], default='python', max_length=20)),
                ('code', models.TextField()),
                ('input_data', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('execution_time', models.FloatField(blank=True, null=True)),
                ('memory_used', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unique_id', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_app_codesubmission',
            },
        ),
    ]
