from __future__ import annotations

import re

from django.apps import apps


def _normalize_roman_token(token: str) -> str:
    token = (token or "").strip()
    if not token:
        return token
    return token.upper()


def normalize_cohort_label(raw_label: str | None) -> str | None:
    """
    Canonicalize cohort labels while preserving non-cohort labels.

    Examples:
    - "cohort xv" -> "Cohort XV"
    - "master class cohort iii" -> "Master Class Cohort III"
    """
    label = (raw_label or "").strip()
    if not label:
        return None

    master_match = re.search(
        r"master\s*class\s*cohort\s*([ivxlcdm0-9]+)",
        label,
        flags=re.IGNORECASE,
    )
    if master_match:
        return f"Master Class Cohort {_normalize_roman_token(master_match.group(1))}"

    cohort_match = re.search(r"\bcohort\s*([ivxlcdm0-9]+)\b", label, flags=re.IGNORECASE)
    if cohort_match:
        return f"Cohort {_normalize_roman_token(cohort_match.group(1))}"

    if re.fullmatch(r"[ivxlcdm0-9]+", label, flags=re.IGNORECASE):
        return f"Cohort {_normalize_roman_token(label)}"

    return re.sub(r"\s+", " ", label).strip()


def _course_track_key(*, registration_name: str, cohort_label: str, course_name: str) -> str:
    text = " ".join(
        [
            (registration_name or "").lower(),
            (cohort_label or "").lower(),
            (course_name or "").lower(),
        ]
    )
    if "rust" in text or "master class" in text or "masterclass" in text:
        return "rust"
    if "zk" in text or "zero knowledge" in text:
        return "zk"
    if "web2" in text:
        return "web2"
    if "web3" in text or "solidity" in text:
        return "web3"
    return "generic"


def _registration_matches_track(registration, track_key: str) -> bool:
    if track_key == "generic":
        return True
    text = " ".join(
        [
            (registration.name or "").lower(),
            (registration.cohort or "").lower(),
        ]
    )
    if track_key == "rust":
        return ("rust" in text) or ("master class" in text) or ("masterclass" in text)
    if track_key == "zk":
        return ("zk" in text) or ("zero knowledge" in text)
    if track_key == "web2":
        return "web2" in text
    if track_key == "web3":
        return ("web3" in text) or ("solidity" in text)
    return True


def resolve_current_open_registration_ids() -> list[int]:
    """
    Active intake registration IDs: newest ``is_open`` programme per track (web3/web2/zk/rust).

    Older programmes often stay ``is_open=True`` in admin; this avoids pulling every
    historical paid row linked to any open registration.
    """
    registration_model = apps.get_model("cohort", "Registration")
    open_regs = list(
        registration_model.objects.filter(is_open=True).order_by("-updated_at", "-id")
    )
    if not open_regs:
        return []

    chosen_ids: list[int] = []
    seen_tracks: set[str] = set()
    for registration in open_regs:
        track_key = _course_track_key(
            registration_name=registration.name or "",
            cohort_label=registration.cohort or "",
            course_name="",
        )
        if track_key in seen_tracks:
            continue
        seen_tracks.add(track_key)
        chosen_ids.append(registration.id)
    return chosen_ids


def resolve_active_cohort_label(*, registration=None, course=None) -> str | None:
    """
    Resolve the cohort label from the current active intake when possible.

    Falls back to the linked registration label when no active peer is found.
    """
    linked_registration = registration
    if linked_registration is None and course is not None:
        linked_registration = getattr(course, "registration", None)
    if linked_registration is None:
        return None

    linked_label = normalize_cohort_label(
        linked_registration.cohort or linked_registration.name
    )
    track_key = _course_track_key(
        registration_name=linked_registration.name or "",
        cohort_label=linked_registration.cohort or "",
        course_name=getattr(course, "name", "") or "",
    )
    if track_key == "generic":
        return linked_label

    registration_model = apps.get_model("cohort", "Registration")
    active_registration = (
        registration_model.objects.filter(is_open=True)
        .order_by("-updated_at", "-id")
    )
    for reg in active_registration:
        if _registration_matches_track(reg, track_key):
            active_label = normalize_cohort_label(reg.cohort or reg.name)
            if active_label:
                return active_label
    return linked_label


def fit_participant_cohort(label: str | None) -> str | None:
    if label is None:
        return None
    participant_model = apps.get_model("cohort", "Participant")
    max_len = participant_model._meta.get_field("cohort").max_length
    return label[:max_len]
