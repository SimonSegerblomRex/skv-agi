"""...

Specification:
https://www.skatteverket.se/download/18.339cd9fe17d1714c0772aec/1639485591598/Bilaga%20Struktur,%20XML-dokument_1.1.11.1.xlsx

Test:
https://sso.test.skatteverket.se/dama141/da_testtjanst_web/login.do?method=test
"""
import datetime
from dataclasses import dataclass

from lxml import etree


@dataclass
class User:
    """...."""

    id: int
    name: str
    email: str
    phone: str = None

@dataclass
class Payment:
    """..."""
    id: int
    gross: float


NSMAP = {
    None: "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "agd": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
}
agd = lambda s: f"{{{NSMAP['agd']}}}{s}"

root = etree.Element("Skatteverket", omrade="Arbetsgivardeklaration", nsmap=NSMAP)


def add_sender(root, user):
    """Avsandare"""
    sender = etree.SubElement(root, agd("Avsandare"))

    software = etree.SubElement(sender, agd("Programnamn"))
    software.text = "skv-agi"

    # Since the file will be submitted manually it
    # makes most sense to use the contact information
    # for the user here.
    orgnbr = etree.SubElement(sender, agd("Organisationsnummer"))
    orgnbr.text = str(user.id)

    contact = etree.SubElement(sender, agd("TekniskKontaktperson"))
    name = etree.SubElement(contact, agd("Namn"))
    name.text = user.name
    phone = etree.SubElement(contact, agd("Telefon"))
    phone.text = user.phone or "-"
    email = etree.SubElement(contact, agd("Epostadress"))
    email.text = user.email

    created = etree.SubElement(sender, agd("Skapad"))
    created.text = datetime.datetime.now().isoformat()


def add_common(root, user):
    """Blankettgemensamt"""
    common = etree.SubElement(root, agd("Blankettgemensamt"))

    employer = etree.SubElement(common, agd("Arbetsgivare"))

    orgnbr = etree.SubElement(employer, agd("AgRegistreradId"))
    orgnbr.text = str(user.id)

    contact = etree.SubElement(employer, agd("Kontaktperson"))
    name = etree.SubElement(contact, agd("Namn"))
    name.text = user.name
    phone = etree.SubElement(contact, agd("Telefon"))
    phone.text = user.phone or "-"
    email = etree.SubElement(contact, agd("Epostadress"))
    email.text = user.email


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

    # FIXME: Some more stuff maybe..?


def add_iu(root, nbr, payment):
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
    receiverid.text = "198202252386"  # FIXME Personnummer

    period = etree.SubElement(iu, agd("RedovisningsPeriod"), faltkod="006")
    period.text = "202112"  # FIXME

    specnbr = etree.SubElement(iu, agd("Specifikationsnummer"), faltkod="570")
    specnbr.text = str(nbr)

    taxred = etree.SubElement(iu, agd("AvdrPrelSkatt"), faltkod="001")

    # Assuming only one payment per year so that iu.gross is the
    # total amount for the whole year
    if payment.gross < 1000:
        taxred.text = "0"
        paid = etree.SubElement(iu, agd("KontantErsattningEjUlagSA"), faltkod="131")
        paid.text = str(payment.gross)
    else:
        # Ugly to do this here, but hard coding the deducted tax to 30 %
        taxred.text = str(int(0.3 * payment.gross))
        paid = etree.SubElement(iu, agd("KontantErsattningUlagAG"), faltkod="011")
        paid.text = str(payment.gross)


if __name__ == "__main__":
    import toml

    config = toml.load("test.toml")
    sender = User(**config["sender"])

    add_sender(root, sender)
    add_common(root, sender)
    add_hu(root)
    for i, payment in enumerate(config["payments"]):
        add_iu(root, nbr=i + 1, payment=Payment(**payment))

    tree = etree.ElementTree(root)
    tree.write(
        "test.xml",
        encoding="utf-8",
        xml_declaration=True,
        standalone=False,
        pretty_print=True,
    )

    # Skattverket's parser doesn't like single quotes...
    # https://github.com/lxml/lxml/pull/277
    with open("test.xml", "r+b") as f:
        old = f.readline()
        new = old.replace(b"'", b'"')
        f.seek(0)
        f.write(new)
