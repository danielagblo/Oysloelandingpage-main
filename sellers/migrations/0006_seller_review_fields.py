from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sellers', '0005_pricingplan_cancelled_monthly_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='reviewed_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reviewed_sellers',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='seller',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='review_notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]

