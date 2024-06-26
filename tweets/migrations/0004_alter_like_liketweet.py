# Generated by Django 4.2.11 on 2024-05-11 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0003_rename_tweet_like_liketweet_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="liketweet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="like_tweet", to="tweets.tweet"
            ),
        ),
    ]
