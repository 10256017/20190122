# Generated by Django 2.1.5 on 2019-01-22 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20190122_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='內文')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='commits', to=settings.AUTH_USER_MODEL, verbose_name='建立者')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_commits', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commits', to='posts.Post', verbose_name='文章')),
            ],
        ),
    ]
