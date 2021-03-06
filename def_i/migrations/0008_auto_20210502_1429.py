# Generated by Django 3.1.7 on 2021-05-02 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('def_i', '0007_auto_20210502_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lesson', to='def_i.course'),
        ),
        migrations.CreateModel(
            name='StudyingCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studying_course', to='def_i.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studying_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
