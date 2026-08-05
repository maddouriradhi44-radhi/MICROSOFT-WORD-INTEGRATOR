from app.services.word_analyzer import WordAnalyzer


def test_word_analyzer():

    analyzer = WordAnalyzer()


    result = analyzer.analyze(
    "app/tests/files/test_document.docx"
    )

    assert len(result) == 3


    assert result[0]["title"] == "Introduction"

    assert result[0]["level"] == 1


    assert len(result[0]["blocks"]) == 2


    assert result[1]["title"] == "Architecture"


    assert result[2]["level"] == 2