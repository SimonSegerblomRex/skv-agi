#https://www.skatteverket.se/download/18.339cd9fe17d1714c0772aea/1639485591481/Bilaga%20Exempelfiler_1.1.11.1.pdf
from lxml import etree

NSMAP = {
    None: "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "agd": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
}

root = etree.Element("Skatteverket", omrade="Arbetsgivardeklaration", nsmap=NSMAP)
sender = etree.SubElement(root, f"{{{NSMAP['agd']}}}Avsandare")

tree = etree.ElementTree(root)
tree.write(
    "test.xml",
    encoding="utf-8",
    xml_declaration=True,
    standalone=False,
    pretty_print=True,
)
