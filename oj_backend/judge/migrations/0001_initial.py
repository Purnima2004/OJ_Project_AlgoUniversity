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
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=50)),
                ('examples', models.TextField(blank=True)),
                ('constraints', models.TextField(blank=True)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'auth_app_problem',
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField()),
                ('expected_output', models.TextField()),
                ('is_sample', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='judge.problem')),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'auth_app_testcase',
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problems', models.ManyToManyField(blank=True, to='judge.problem')),
            ],
            options={
                'db_table': 'auth_app_contest',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.CharField(choices=[('python', 'Python'), ('cpp', 'C++'), ('java', 'Java')], default='python', max_length=20)),
                ('status', models.CharField(choices=[('AC', 'Accepted'), ('WA', 'Wrong Answer'), ('TLE', 'Time Limit Exceeded'), ('RE', 'Runtime Error'), ('CE', 'Compilation Error'), ('MLE', 'Memory Limit Exceeded'), ('PE', 'Presentation Error')], default='WA', max_length=10)),
                ('execution_time', models.FloatField(blank=True, null=True)),
                ('memory_used', models.IntegerField(blank=True, null=True)),
                ('test_cases_passed', models.IntegerField(default=0)),
                ('total_test_cases', models.IntegerField(default=0)),
                ('error_message', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.problem')),
                ('contest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='judge.contest')),
            ],
            options={
                'ordering': ['-submitted_at'],
                'db_table': 'auth_app_submission',
            },
        ),
        migrations.CreateModel(
            name='SubmissionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AC', 'Accepted'), ('WA', 'Wrong Answer'), ('TLE', 'Time Limit Exceeded'), ('RE', 'Runtime Error'), ('CE', 'Compilation Error'), ('MLE', 'Memory Limit Exceeded'), ('PE', 'Presentation Error')], max_length=10)),
                ('execution_time', models.FloatField(blank=True, null=True)),
                ('memory_used', models.IntegerField(blank=True, null=True)),
                ('actual_output', models.TextField(blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='judge.submission')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.testcase')),
            ],
            options={
                'db_table': 'auth_app_submissionresult',
            },
        ),
        migrations.CreateModel(
            name='ContestParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.contest')),
                ('problems_solved', models.ManyToManyField(blank=True, to='judge.problem')),
            ],
            options={
                'db_table': 'auth_app_contestparticipation',
                'unique_together': {('user', 'contest')},
            },
        ),
    ]
