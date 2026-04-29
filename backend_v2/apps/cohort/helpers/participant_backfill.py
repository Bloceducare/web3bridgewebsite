from __future__ import annotations

from django.db import IntegrityError

from cohort import models
from cohort.helpers.cohort_label import fit_participant_cohort, resolve_active_cohort_label


def normalize_participant_cohort_value(registration):
    if registration is None:
        return None
    return fit_participant_cohort(resolve_active_cohort_label(registration=registration))


def autocorrect_participant_links(*, participant_id=None, email=None, return_stats=False):
    """
    Backfill legacy Participant rows:
    - registration_id from course.registration when missing
    - cohort from registration label when missing/stale
    """
    qs = models.Participant.objects.select_related("course__registration", "registration")
    if participant_id is not None:
        qs = qs.filter(pk=participant_id)
    if email:
        qs = qs.filter(email__iexact=(email or "").strip())

    updated = 0
    skipped_conflicts = 0
    for participant in qs.iterator():
        changed_fields = []
        registration_for_cohort = participant.registration

        if participant.registration_id is None and participant.course_id:
            linked_registration = getattr(participant.course, "registration", None)
            if linked_registration is not None:
                participant.registration_id = linked_registration.pk
                registration_for_cohort = linked_registration
                changed_fields.append("registration")

        expected_cohort = normalize_participant_cohort_value(registration_for_cohort)
        # Backfill only when missing (None/blank), do not rewrite existing non-empty cohort.
        if (participant.cohort or "").strip() == "" and expected_cohort is not None:
            participant.cohort = expected_cohort
            changed_fields.append("cohort")

        if not changed_fields:
            continue

        # Guard uniqueness: do not update rows that would collide on
        # (email, cohort) unique constraint.
        if (
            expected_cohort is not None
            and models.Participant.objects.filter(
                email__iexact=(participant.email or "").strip(),
                cohort=expected_cohort,
            )
            .exclude(pk=participant.pk)
            .exists()
        ):
            skipped_conflicts += 1
            continue

        try:
            participant.save(update_fields=sorted(set(changed_fields)))
            updated += 1
        except IntegrityError:
            skipped_conflicts += 1

    if return_stats:
        return {"updated": updated, "skipped_conflicts": skipped_conflicts}
    return updated
