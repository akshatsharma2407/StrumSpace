from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from app.modules.enquiries.schemas import (
    EnquiryCreate,
    EnquiryInternalUpdate,
    EnquiryListQuery,
    EnquiryVisitorResponse,
    EnquiryVisitorUpdate,
)


def test_create_normalizes_contact_fields() -> None:
    enquiry = EnquiryCreate(
        full_name="  Ravi Kumar  ",
        phone_number=" +91 98765 43210 ",
        email="  ravi@example.com ",
        experience_level="BEGINNER",
        message="  Evening classes  ",
    )

    assert enquiry.full_name == "Ravi Kumar"
    assert enquiry.phone_number == "+919876543210"
    assert enquiry.email == "ravi@example.com"
    assert enquiry.experience_level == "BEGINNER"
    assert enquiry.message == "Evening classes"


def test_enum_values_must_use_canonical_uppercase_without_spaces() -> None:
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number="9876543210", experience_level="beginner")
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number="9876543210", experience_level=" BEGINNER")


def test_optional_blank_text_is_normalized_to_none() -> None:
    enquiry = EnquiryCreate(
        full_name="Ravi",
        phone_number="9876543210",
        email="   ",
        message="\t",
    )

    assert enquiry.email is None
    assert enquiry.message is None


@pytest.mark.parametrize(
    "phone_number",
    ["1234567890", "+91987654321", "+9188765432101", "+14155552671"],
)
def test_invalid_phone_numbers_are_rejected(phone_number: str) -> None:
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number=phone_number)


def test_create_rejects_invalid_boundaries() -> None:
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="   ", phone_number="9876543210")
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number="9876543210", age=5)
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number="9876543210", age=121)
    with pytest.raises(ValidationError):
        EnquiryCreate(full_name="Ravi", phone_number="9876543210", message="x" * 1001)


def test_update_distinguishes_omitted_fields_from_explicit_null() -> None:
    update = EnquiryVisitorUpdate(email=None)

    assert update.model_fields_set == {"email"}
    assert update.email is None
    assert "message" not in update.model_fields_set


def test_required_visitor_fields_cannot_be_cleared() -> None:
    with pytest.raises(ValidationError):
        EnquiryVisitorUpdate(full_name=None)
    with pytest.raises(ValidationError):
        EnquiryVisitorUpdate(phone_number=None)


def test_empty_update_and_restricted_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        EnquiryVisitorUpdate()
    with pytest.raises(ValidationError):
        EnquiryVisitorUpdate(status="CLOSED")  # type: ignore[call-arg]


def test_internal_update_normalizes_datetime_and_validates_follow_up() -> None:
    last_contacted = datetime.now().astimezone() - timedelta(hours=1)
    update = EnquiryInternalUpdate(
        status="CONTACTED",
        last_contacted_at=last_contacted,
        next_follow_up_at=last_contacted + timedelta(days=1),
    )

    assert update.status == "CONTACTED"
    assert update.last_contacted_at is not None
    assert update.last_contacted_at.tzinfo is not None


def test_internal_update_rejects_future_contact_and_invalid_follow_up() -> None:
    with pytest.raises(ValidationError):
        EnquiryInternalUpdate(last_contacted_at=datetime.now().astimezone() + timedelta(minutes=1))

    last_contacted = datetime.now().astimezone() - timedelta(hours=1)
    with pytest.raises(ValidationError):
        EnquiryInternalUpdate(
            last_contacted_at=last_contacted,
            next_follow_up_at=last_contacted,
        )


def test_naive_datetime_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EnquiryInternalUpdate(last_contacted_at=datetime(2026, 11, 28, 10, 30))


def test_query_accepts_canonical_uppercase_values() -> None:
    query = EnquiryListQuery(status="NEW", sort_by="UPDATED_AT", order="ASC")

    assert query.status == "NEW"
    assert query.sort_by == "UPDATED_AT"
    assert query.order == "ASC"
    assert query.limit == 20
    assert query.offset == 0


def test_query_enum_values_must_use_canonical_uppercase_without_spaces() -> None:
    with pytest.raises(ValidationError):
        EnquiryListQuery(status="new")
    with pytest.raises(ValidationError):
        EnquiryListQuery(sort_by="updated_at")
    with pytest.raises(ValidationError):
        EnquiryListQuery(order="DESC ")


def test_internal_status_must_use_canonical_uppercase() -> None:
    with pytest.raises(ValidationError):
        EnquiryInternalUpdate(status="contacted")


def test_query_normalizes_search_and_validates_inclusive_ranges() -> None:
    query = EnquiryListQuery(
        search="  ravi  ",
        created_from="2026-11-28T10:30:00+05:30",
        created_to="2026-11-28T10:30:00+05:30",
    )

    assert query.search == "ravi"
    assert query.created_from == query.created_to


def test_query_rejects_reversed_ranges_and_invalid_pagination() -> None:
    with pytest.raises(ValidationError):
        EnquiryListQuery(
            created_from="2026-11-29T10:30:00+05:30",
            created_to="2026-11-28T10:30:00+05:30",
        )
    with pytest.raises(ValidationError):
        EnquiryListQuery(limit=101)
    with pytest.raises(ValidationError):
        EnquiryListQuery(offset=-1)


def test_visitor_response_does_not_include_internal_follow_up_fields() -> None:
    response = EnquiryVisitorResponse(
        id=1,
        full_name="Ravi",
        phone_number="+919876543210",
        status="NEW",
        created_at="2026-11-28T10:30:00+05:30",
        updated_at="2026-11-28T10:30:00+05:30",
    )

    assert "last_contacted_at" not in response.model_dump()
    assert "next_follow_up_at" not in response.model_dump()
