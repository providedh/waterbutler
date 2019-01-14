import pytest

from waterbutler.providers.osfstorage.tei_p5_normalizator import Tei5Normalizator


class TestNormalizeTeiP5:

    removing_namespaces_test_data = [
        ("""<tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:ns2="http://exist.sourceforge.net/NS/exist">
                <tei:teiHeader>
                    <tei:title>Rota 1, Księga Ziemska 1, Karta 14v, Pyzdry</tei:title>
                </tei:teiHeader>
            </tei:TEI>""",
         """<TEI xmlns:ns2="http://exist.sourceforge.net/NS/exist">
                <teiHeader>
                    <title>Rota 1, Księga Ziemska 1, Karta 14v, Pyzdry</title>
                </teiHeader>
            </TEI>"""),
    ]

    @pytest.mark.parametrize("file_content, expected", removing_namespaces_test_data)
    def test_removing_default_tei_p5_namespaces(self, file_content, expected):
        normalizator = Tei5Normalizator()
        output = normalizator.remove_default_tei5_namespace(file_content)

        assert output == expected

    exception_test_data = [
        ("""<tei:TEI xmlns:tei="http://www.link.to.wrong.uri.com" xmlns:ns2="http://exist.sourceforge.net/NS/exist">
                    <tei:teiHeader>
                        <tei:title>Rota 1, Księga Ziemska 1, Karta 14v, Pyzdry</tei:title>
                    </tei:teiHeader>
                </tei:TEI>""",
         """<TEI xmlns:ns2="http://exist.sourceforge.net/NS/exist">
                <teiHeader>
                    <title>Rota 1, Księga Ziemska 1, Karta 14v, Pyzdry</title>
                </teiHeader>
            </TEI>"""),
    ]

    @pytest.mark.parametrize("file_content", exception_test_data)
    def test_removing_default_tei_p5_namespaces_with_bad_declaration(self, file_content):
        normalizator = Tei5Normalizator()

        with pytest.raises(Exception):
            output = normalizator.remove_default_tei5_namespace(file_content)
