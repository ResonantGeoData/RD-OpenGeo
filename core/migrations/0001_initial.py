# Generated by Django 3.0.3 on 2020-03-16 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('data', models.FileField(upload_to='algorithm')),
                (
                    'creator',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='AlgorithmResult',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', models.FileField(upload_to='results')),
                (
                    'algorithm',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.Algorithm'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('data', models.FileField(upload_to='dataset')),
                (
                    'creator',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Groundtruth',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('public', models.BooleanField(default=False)),
                ('data', models.FileField(upload_to='groundtruth')),
                (
                    'creator',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    'dataset',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.Dataset'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ScoreAlgorithm',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('data', models.FileField(upload_to='scorealgorithm')),
                (
                    'creator',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                (
                    'creator',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', models.FileField(upload_to='scores')),
                (
                    'algorithmresult',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.AlgorithmResult'
                    ),
                ),
                (
                    'groundtruth',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.Groundtruth'
                    ),
                ),
                (
                    'scorealgorithm',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.ScoreAlgorithm'
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='scorealgorithm',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task'),
        ),
        migrations.AddField(
            model_name='groundtruth',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task'),
        ),
        migrations.AddField(
            model_name='algorithmresult',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Dataset'),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task'),
        ),
        migrations.AlterUniqueTogether(name='groundtruth', unique_together={('task', 'dataset')},),
    ]
