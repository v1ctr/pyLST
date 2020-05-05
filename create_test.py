import click
import requests
from datetime import datetime

@click.command()
@click.option('--jahr', default=2020, help='Steuerjahr.')
@click.option('--af', default=1, help='Anwendung des Faktorverfahrens.')
@click.option('--f', default=1.0, help='Eingetragener Faktor mit drei Nachkommastellen.')
@click.option('--AJAHR', default=0, help='Auf die Vollendung des 64. Lebensjahres folgende Kalenderjahr')
@click.option('--ALTER1', default=0, help='1, wenn das 64. Lebensjahr zu Beginn des Kalenderjahres vollendet wurde, in dem der Lohnzahlungszeitraum endet (§ 24 a EStG),')
@click.option('--ENTSCH', default=0, help='In VKAPA und VMT enthaltene Entschädigungen nach §24 Nummer 1 EStG in Cent.')
@click.option('--JFREIB', default=0, help='Jahresfreibetrag nach Maßgabe der Eintragungen auf der Lohnsteuerkarte in Cents (ggf. 0).')
@click.option('--JHINZU', default=0, help='Jahreshinzurechnungsbetrag in Cents (ggf. 0).')
@click.option('--JRE4', default=0, help='Voraussichtlicher Jahresarbeitslohn ohne sonstige Bezüge und ohne Vergütung für mehrjährige Tätigkeit in Cent')
@click.option('--JVBEZ', default=0, help='In JRE4 enthaltene Versorgungsbezuege in Cents (ggf. 0)')
@click.option('--KRV', default='0', help='Merker für die Vorsorgepauschale', type=click.Choice(['0', '1', '2']))
@click.option('--KVZ', default=0, help='Einkommensbezogener Zusatzbeitragssatz eines gesetzlich krankenversicherten Arbeitnehmers, auf dessen Basis der an die Krankenkasse zu zahlende Zusatzbeitrag berechnet wird, in Prozent (bspw. 0,90 für 0,90 %) mit 2 Dezimalstellen.')
@click.option('--LZZ', default='1', help='Lohnzahlungszeitraum', type=click.Choice(['1', '2', '3', '4']))
@click.option('--LZZFREIB', default=0, help='In der Lohnsteuerkarte des Arbeitnehmers eingetragener Freibetrag für den Lohnzahlungszeitraum in Cent')
@click.option('--LZZHINZU', default=0, help='In der Lohnsteuerkarte des Arbeitnehmers eingetragener Hinzurechnungsbetrag für den Lohnzahlungszeitraum in Cent')
@click.option('--PKPV', default=0, help='Dem Arbeitgeber mitgeteilte Zahlungen des Arbeitnehmers zur privaten Kranken- bzw. Pflegeversicherung im Sinne des §10 Abs. 1 Nr. 3 EStG 2010 als Monatsbetrag in Cent')
@click.option('--PKV', default='0', help='Krankenversicherung', type=click.Choice(['0', '1', '2']))
@click.option('--PVS', default=0, help='1, wenn bei der sozialen Pflegeversicherung die Besonderheiten in Sachsen zu berücksichtigen sind bzw. zu berücksichtigen wären, sonst 0')
@click.option('--PVZ', default=0, help='1, wenn er der Arbeitnehmer den Zuschlag zur sozialen Pflegeversicherung zu zahlen hat, sonst 0.')
@click.option('--R', default=0, help='Religionsgemeinschaft des Arbeitnehmers lt. Lohnsteuerkarte.')
@click.option('--RE4', default=0, help='Steuerpflichtiger Arbeitslohn vor Beruecksichtigung der Freibetraege fuer Versorgungsbezuege, des Altersentlastungsbetrags und des auf der Lohnsteuerkarte fuer den Lohnzahlungszeitraum eingetragenen Freibetrags in Cents.')
@click.option('--SONSTB', default=0, help='Sonstige Bezuege (ohne Verguetung aus mehrjaehriger Taetigkeit) einschliesslich Sterbegeld bei Versorgungsbezuegen sowie Kapitalauszahlungen/Abfindungen, soweit es sich nicht um Bezuege fuer mehrere Jahre handelt in Cents (ggf. 0)')
@click.option('--STERBE', default=0, help='Sterbegeld bei Versorgungsbezuegen sowie Kapitalauszahlungen/Abfindungen, soweit es sich nicht um Bezuege fuer mehrere Jahre handelt (in SONSTB enthalten) in Cents')
@click.option('--STKL', default='1', help='Steuerklasse', type=click.Choice(['1', '2', '3', '4', '5', '6']))
@click.option('--VBEZ', default=0, help='In RE4 enthaltene Versorgungsbezuege in Cents (ggf. 0)')
@click.option('--VBEZM', default=0, help='Vorsorgungsbezug im Januar 2005 bzw. fuer den ersten vollen Monat')
@click.option('--VBEZS', default=0, help='Voraussichtliche Sonderzahlungen im Kalenderjahr des Versorgungsbeginns bei Versorgungsempfaengern ohne Sterbegeld, Kapitalauszahlungen/Abfindungen bei Versorgungsbezuegen in Cents')
@click.option('--VBS', default=0, help='In SONSTB enthaltene Versorgungsbezuege einschliesslich Sterbegeld in Cents (ggf. 0)')
@click.option('--VJAHR', default=0, help='Jahr, in dem der Versorgungsbezug erstmalig gewaehrt wurde; werden mehrere Versorgungsbezuege gezahlt, so gilt der aelteste erstmalige Bezug')
@click.option('--VKAPA', default=0, help='Kapitalauszahlungen / Abfindungen / Nachzahlungen bei Versorgungsbezügen für mehrere Jahre in Cent (ggf. 0)')
@click.option('--VMT', default=0, help='Vergütung für mehrjährige Tätigkeit ohne Kapitalauszahlungen und ohne Abfindungen bei Versorgungsbezügen in Cent (ggf. 0)')
@click.option('--ZKF', default=0, help='Zahl der Freibetraege fuer Kinder (eine Dezimalstelle, nur bei Steuerklassen I, II, III und IV)')
@click.option('--ZMVB', default=0, help='Zahl der Monate, fuer die Versorgungsbezuege gezahlt werden (nur erforderlich bei Jahresberechnung (LZZ = 1)')
@click.option('--JRE4ENT', default=0, help='In JRE4 enthaltene Entschädigungen nach § 24 Nummer 1 EStG in Cent')
@click.option('--SONSTENT', default=0, help='In SONSTB enthaltene Entschädigungen nach § 24 Nummer 1 EStG in Cent')
def create_test(jahr, **kwargs):
    if jahr == 2020:
        url = "http://www.bmf-steuerrechner.de/interface/2020Version1.xhtml"
        url = add_params_to_url(url, kwargs)
        r = requests.get(url)
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        path = f'tests/xml/{jahr}/{timestamp}.xml'
        with open(path, 'wb') as f:
            f.write(r.content)
        click.echo(path+" wurde erfolgreich angelegt.")


def add_params_to_url(url, params):
    url += '?' + 'code' + '=' + 'Lohn2020'
    for key in params:
        url += '&' + key + '=' + str(params[key])
    return url


if __name__ == '__main__':
    create_test()
