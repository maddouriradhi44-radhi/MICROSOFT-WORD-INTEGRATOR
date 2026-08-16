from app.services.word_comparison_service import (
    WordComparisonService,
)


def test_no_change():

    service = WordComparisonService()

    result = service.compare(
        current_title="Introduction",
        current_content="Original content",
        imported_title="Introduction",
        imported_content="Original content",
    )

    assert result["changed"] is False
    assert result["title_changed"] is False
    assert result["content_changed"] is False


def test_content_changed():

    service = WordComparisonService()

    result = service.compare(
        current_title="Introduction",
        current_content="Original content",
        imported_title="Introduction",
        imported_content="Modified content",
    )

    assert result["changed"] is True
    assert result["title_changed"] is False
    assert result["content_changed"] is True


def test_title_changed():

    service = WordComparisonService()

    result = service.compare(
        current_title="Introduction",
        current_content="Original content",
        imported_title="New Introduction",
        imported_content="Original content",
    )

    assert result["changed"] is True
    assert result["title_changed"] is True
    assert result["content_changed"] is False