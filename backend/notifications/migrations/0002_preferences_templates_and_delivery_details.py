import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('notifications', '0001_initial')]

    operations = [
        migrations.AddField(model_name='guest', name='accepts_push', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='notification', name='attempt_count', field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name='notification', name='failure_reason', field=models.TextField(blank=True)),
        migrations.AddField(model_name='notification', name='notification_type', field=models.CharField(choices=[('booking_confirmation', 'Booking confirmation'), ('pre_arrival', 'Pre-arrival'), ('post_stay', 'Post-stay')], default='booking_confirmation', max_length=30)),
        migrations.AlterField(model_name='notification', name='channel', field=models.CharField(choices=[('email', 'Email'), ('sms', 'SMS'), ('push', 'Push')], max_length=10)),
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('booking_confirmation', 'Booking confirmation'), ('pre_arrival', 'Pre-arrival'), ('post_stay', 'Post-stay')], max_length=30)),
                ('channel', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS'), ('push', 'Push')], default='email', max_length=10)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('body', models.TextField(help_text='Use {guest_name}, {hotel_name}, {confirmation_code}, {check_in}, or {check_out}.')),
                ('is_active', models.BooleanField(default=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='notifications.hotel')),
            ],
        ),
        migrations.AddConstraint(model_name='notificationtemplate', constraint=models.UniqueConstraint(fields=('hotel', 'notification_type', 'channel'), name='unique_hotel_template')),
    ]
