from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpcode',
            name='session_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='otpcode',
            name='chat_id',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.RenameField(
            model_name='user',
            old_name='reading_goal_2026',
            new_name='annual_reading_goal',
        ),
    ]