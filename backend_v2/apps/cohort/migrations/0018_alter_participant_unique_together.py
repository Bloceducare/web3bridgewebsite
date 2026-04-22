# Uniqueness: one signup per email per programme (registration) per course.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cohort", "0017_assessment_breakdown_column_if_missing"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="participant",
            unique_together=(),
        ),
        migrations.AddConstraint(
            model_name="participant",
            constraint=models.UniqueConstraint(
                fields=("email", "registration", "course"),
                name="cohort_participant_email_registration_course_uniq",
            ),
        ),
    ]
