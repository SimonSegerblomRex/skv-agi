"""...

Specification:
https://www.skatteverket.se/download/18.339cd9fe17d1714c0772aec/1639485591598/Bilaga%20Struktur,%20XML-dokument_1.1.11.1.xlsx

Test:
https://sso.test.skatteverket.se/dama141/da_testtjanst_web/index.jsp?method=test#!/start
"""
import datetime

from lxml import etree


NSMAP = {
    None: "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "agd": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
}
agd = lambda s: f"{{{NSMAP['agd']}}}{s}"

root = etree.Element("Skatteverket", omrade="Arbetsgivardeklaration", nsmap=NSMAP)


def add_sender(root):
    """Avsandare"""
    sender = etree.SubElement(root, agd("Avsandare"))

    software = etree.SubElement(sender, agd("Programnamn"))
    software.text = "skv-agi"
    orgnbr = etree.SubElement(sender, agd("Organisationsnummer"))
    orgnbr.text = "167460001667"  # FIXME ?

    contact = etree.SubElement(sender, agd("TekniskKontaktperson"))
    name = etree.SubElement(contact, agd("Namn"))
    name.text = "Simon Segerblom Rex"
    phone = etree.SubElement(contact, agd("Telefon"))
    phone.text = "0"
    email = etree.SubElement(contact, agd("Epostadress"))
    email.text = "SimonSegerblomRex@users.noreply.github.com"

    created = etree.SubElement(sender, agd("Skapad"))
    created.text = datetime.datetime.now().isoformat()


def add_common(root):
    """Blankettgemensamt"""
    common = etree.SubElement(root, agd("Blankettgemensamt"))

    employer = etree.SubElement(common, agd("Arbetsgivare"))
    orgnbr = etree.SubElement(employer, agd("AgRegistreradId"))
    orgnbr.text = "167460001667"  # FIXME: Parse from config

    contact = etree.SubElement(employer, agd("Kontaktperson"))
    name = etree.SubElement(contact, agd("Namn"))
    name.text = "Test"  # FIXME
    phone = etree.SubElement(contact, agd("Telefon"))
    phone.text = "046-010203"  # FIXME
    email = etree.SubElement(contact, agd("Epostadress"))
    email.text = "tmp@tmp.no"  # FIXME


def add_hu(root):
    """Huvuduppgift"""
    form = etree.SubElement(root, agd("Blankett"))

    info = etree.SubElement(form, agd("Arendeinformation"))
    orgnbr = etree.SubElement(info, agd("Arendeagare"))
    orgnbr.text = "167460001667"  # FIXME
    period = etree.SubElement(info, agd("Period"))
    period.text = "202112"  # FIXME

    content = etree.SubElement(form, agd("Blankettinnehall"))
    hu = etree.SubElement(content, agd("HU"))

    employer = etree.SubElement(hu, agd("ArbetsgivareHUGROUP"))
    orgnbr = etree.SubElement(employer, agd("AgRegistreradId"), faltkod="201")
    orgnbr.text = "167460001667"  # FIXME

    period = etree.SubElement(hu, agd("RedovisningsPeriod"), faltkod="006")
    period.text = "202112"  # FIXME

    # FIXME: Some more stuff maybe


def add_iu(root):
    """Individuppgift"""
    form = etree.SubElement(root, agd("Blankett"))

    info = etree.SubElement(form, agd("Arendeinformation"))
    orgnbr = etree.SubElement(info, agd("Arendeagare"))
    orgnbr.text = "167460001667"  # FIXME
    period = etree.SubElement(info, agd("Period"))
    period.text = "202112"  # FIXME

    content = etree.SubElement(form, agd("Blankettinnehall"))
    iu = etree.SubElement(content, agd("IU"))

    employer = etree.SubElement(iu, agd("ArbetsgivareIUGROUP"))
    orgnbr = etree.SubElement(employer, agd("AgRegistreradId"), faltkod="201")
    orgnbr.text = "167460001667"  # FIXME

    receiver = etree.SubElement(iu, agd("BetalningsmottagareIUGROUP"))
    receiverg = etree.SubElement(receiver, agd("BetalningsmottagareIDChoice"))
    receiverid = etree.SubElement(receiverg, agd("BetalningsmottagarId"), faltkod="215")
    receiverid.text = "198202252386"  # FIXME

    period = etree.SubElement(iu, agd("RedovisningsPeriod"), faltkod="006")
    period.text = "202112"  # FIXME

    # FIXME!!! Allt hardkodat nedanfor...
    specnbr = etree.SubElement(iu, agd("Specifikationsnummer"), faltkod="570")
    specnbr.text = "001"

    taxred = etree.SubElement(iu, agd("AvdrPrelSkatt"), faltkod="001")
    taxred.text = "9300"


add_sender(root)
add_common(root)
add_hu(root)
add_iu(root)

tree = etree.ElementTree(root)
tree.write(
    "test.xml",
    encoding="utf-8",
    xml_declaration=True,
    standalone=False,
    pretty_print=True,
)

#https://github.com/lxml/lxml/pull/277
with open("test.xml", "r+b") as f:
    old = f.readline()
    new = old.replace(b"'", b'"')
    f.seek(0)
    f.write(new)
