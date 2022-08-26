# Generated by Django 4.1 on 2022-08-12 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raterapp', '0002_game_description_game_designer_game_est_time_to_play_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='picture_url',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='player',
        ),
        migrations.AddField(
            model_name='picture',
            name='action_pic',
            field=models.ImageField(null=True, upload_to='actionimages'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pictures', to='raterapp.game'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='raterapp.game'),
        ),
    ]