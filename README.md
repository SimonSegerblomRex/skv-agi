Arbetsgivardeklaration (AGI) / PAYE tax return tools
====================================================

PAYE tax return / Arbetsgivardeklaration (AGI)

Usage
-----
Install dependencies:
```shell
python3 -m pip install lxml
```

Create a *.toml-file with information about the gross salaries that were paid out the previous month:
```toml
[sender]
id = 160000000000 # Organization number pre-fixed with 16 (or 12 digit personal identity number)
name = "Your name"
email = "email@address.se"

[period]
year = 2023
month = 12

[employer]
id = 160000000000 # Organization number pre-fixed with 16

[[payments]]
# Employee 0
id = 197001010000 # 12 digit personal identity number
gross = 5000

[[payments]]
# Employee 1
id = 200012310000 # 12 digit personal identity number
gross = 3500

...
```

Run
```shell
python3 create_agd.py <path to *.toml-file>
```
to generate an *.xml-file ready to be uploaded to skatteverket.se.

**NOTE:** The script makes certain assumptions about the net salaries
and the amount of tax that has been deducted from the gross salaries.
Please make sure that these assumptions are correct before submitting
the PAYE tax return. If necessary you can make corrections in the web
interface after uploading the file, or make changes to the script
generating the file.

References
----------
* [Lämna arbetsgivardeklaration](https://skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration.4.41f1c61d16193087d7fcaeb.html)
* [Teknisk beskrivning och testtjänst](https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/tekniskbeskrivningochtesttjanst.4.309a41aa1672ad0c8377c8b.html)
* [Teknisk beskrivning (1.1.11.1) för arbetsgivardeklaration på individnivå](https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/tekniskbeskrivningochtesttjanst/tekniskbeskrivning1111.4.7eada0316ed67d7282a791.html)
* [Testtjänstenlänk till annan webbplats](https://sso.test.skatteverket.se/dama141/da_testtjanst_web/login.do?method=test)
* [Struktur, XML-dokument](https://www.skatteverket.se/download/18.339cd9fe17d1714c0772aec/1639485591598/Bilaga%20Struktur,%20XML-dokument_1.1.11.1.xlsx)
