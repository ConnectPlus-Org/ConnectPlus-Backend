# Generated by Django 4.1.4 on 2023-01-20 01:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(blank=True, max_length=100, null=True)),
                ('field_of_study', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('grade', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Education',
            },
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=150)),
                ('currently_working', models.BooleanField(default=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('industry', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_image', models.ImageField(default='profolio/background/default.jpg', upload_to='background/')),
                ('about', models.TextField(blank=True, default=None, null=True)),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('current_company', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Profile.experience')),
                ('current_school', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Profile.education')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(choices=[('Company', 'Company'), ('School', 'School'), ('None', 'None')], default='None', max_length=50)),
                ('registered', models.BooleanField(default=False)),
                ('logo', models.ImageField(default='profolio/logo/default1.jpg', upload_to='logo/')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('avatar', models.ImageField(default='profolio/avatar/default.jpg', upload_to='avatar/')),
                ('headline', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('phone_number', models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('first_degrees', models.ManyToManyField(blank=True, related_name='first_degree', through='Network.FirstConnections', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(blank=True, related_name='following', through='Network.Follow', to=settings.AUTH_USER_MODEL)),
                ('second_degrees', models.ManyToManyField(blank=True, related_name='second_degree', through='Network.SecondConnections', to=settings.AUTH_USER_MODEL)),
                ('third_degrees', models.ManyToManyField(blank=True, related_name='third_degree', through='Network.ThirdConnections', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=50)),
                ('test_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_score', to='Profile.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testscore', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
                ('endorsed_by', models.ManyToManyField(blank=True, related_name='endorsement', to='Profile.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_time', models.DateTimeField(auto_now=True)),
                ('viewed_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='Profile.mainprofile')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_by', to='Profile.profile')),
            ],
        ),
        migrations.AddField(
            model_name='mainprofile',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Main_Profile', to='Profile.profile'),
        ),
        migrations.AddField(
            model_name='mainprofile',
            name='viewers',
            field=models.ManyToManyField(through='Profile.ProfileView', to='Profile.profile'),
        ),
        migrations.AddField(
            model_name='experience',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='Profile.organization'),
        ),
        migrations.AddField(
            model_name='experience',
            name='employment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Profile.employment'),
        ),
        migrations.AddField(
            model_name='experience',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='experience', to='Profile.skill'),
        ),
        migrations.AddField(
            model_name='experience',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='education',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='education', to='Profile.organization'),
        ),
        migrations.AddField(
            model_name='education',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_number', models.CharField(blank=True, max_length=20, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='Profile.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='experience',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gte', models.F('start_date'))), name='correct end date', violation_error_message='End date should be greater than starting date'),
        ),
        migrations.AddConstraint(
            model_name='education',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gte', models.F('start_date'))), name='Correct end date', violation_error_message='End date should be greater than starting date'),
        ),
    ]
