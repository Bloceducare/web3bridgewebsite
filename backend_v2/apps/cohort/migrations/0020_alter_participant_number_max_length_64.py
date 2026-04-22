from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cohort", "0019_alter_participant_number_max_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="number",
            field=models.CharField(
                blank=False,
                help_text="International formats allowed; validated loosely in the API.",
                max_length=64,
                null=True,
                verbose_name="phone number",
            ),
        ),
    ]
