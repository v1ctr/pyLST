import unittest
import requests
from pathlib import Path
import xml.etree.ElementTree as ET
from lst2020 import Lohnsteuer2020, BigDecimal


class Lst2020TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'https://www.bmf-steuerrechner.de/interface/2020Version1.xhtml'
        self.code = 'Lohn2020'
        self.year = '2020'
        self.path = Path('tests/xml/2020')

    def convert_xml_to_object(self, path):
        lohnsteuer = {
            'eingaben': {},
            'ausgaben': {}
        }
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            if child.tag == 'eingaben':
                for eingabe in child:
                    try:
                        lohnsteuer['eingaben'][eingabe.attrib['name']] = int(eingabe.attrib['value'])
                    except ValueError:
                        lohnsteuer['eingaben'][eingabe.attrib['name']] = float(eingabe.attrib['value'])
            if child.tag == 'ausgaben':
                for ausgabe in child:
                    lohnsteuer['ausgaben'][ausgabe.attrib['name']] = BigDecimal(ausgabe.attrib['value'])
        return lohnsteuer


    def test_all_2020_xml(self):
        for path in self.path.iterdir():
            if path.is_file():
                obj = self.convert_xml_to_object(path)
                lst2020 = Lohnsteuer2020(**obj['eingaben'])
                lst2020.MAIN()

                for key in obj['ausgaben']:
                    with self.subTest(key=key):
                        self.assertEqual(obj['ausgaben'][key], getattr(lst2020, key))
