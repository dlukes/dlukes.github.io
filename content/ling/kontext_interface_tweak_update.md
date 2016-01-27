Title: Úprava rozhraní konkordanceru KonText -- vylepšená verze
Date: 2015-05-14
Tags: KonText, korpus, konkordance, NoSke, Bonito
Slug: kontext-interface-tweak-update
Alias: /output/kontext-interface-tweak-update.html
Summary: Vylepšená verze skriptu, kterým si uživatel Českého národního korpusu může upravit rozhraní konkordanceru KonText.

Před nějakou dobou jsem zde vyvěsil
[skript]({filename}/ling/kontext_interface_tweak.md), jehož pomocí lze lehce
"přeskládat" a upravit rozhraní korpusového konkordanceru
[KonText](https://kontext.korpus.cz):

- menu je umístěné po straně místo nahoře a permanentně rozbalené
- nad vyhledanou konkordancí je umístěn rychlý hledací box, v němž lze
  předchozí dotaz pohodlně upravit

Víc o motivaci těchto úprav se dočtete
[v původním článku](kontext-interface-tweak.html#background). Stále
platí, že ČNK nemá v plánu tyto změny začlenit přímo do oficiální verze
KonTextu, zejména proto, že rychlý hledací box sice v jistých situacích může
být užitečný, nicméně oproti standardnímu formuláři *Nový dotaz* výrazně
omezuje možnosti pro zadání dotazu.

Vylepšená verze, která je k dispozici níže, odstraňuje některé předchozí
nedostatky skriptu: rychlý hledací box nad konkordancí je větší, ukazuje **vždy
CQL podobu posledního zadaného dotazu**[^1], a především zůstává zobrazený i
během listování konkordancí (tj. není k dispozici jen na její první
stránce). Dotaz lze nyní navíc pro větší přehlednost rozdělit do více řádků,
takže opětovné vyhledávání se nově spouští stiskem kombinace kláves
**Ctrl+Enter** (místo jen Enteru).

Výsledné upravené rozhraní KonText vypadá stále podobně:

<img alt="Upravené rozhraní KonText." src="images/kontext_interface_tweak_update.png" style="max-width: 100%;">

# Postup instalace skriptu

Nová verze skriptu je k dispozici zde:

<script src="https://gist.github.com/dlukes/a99dca231db63c9d5bb7.js"></script>

Kroky k jeho zprovoznění zůstávají stejné:

1.  Nainstalovat si do svého prohlížeče plugin
    [Tampermonkey](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en),
    pokud používáte Chrome, nebo
    [Greasemonkey](https://addons.mozilla.org/en-us/firefox/addon/greasemonkey/),
    pokud používáte Firefox. (Pokud používáte Internet Explorer, budete muset
    dočasně přesedlat na Chrome nebo Firefox.) Testovaný je skript zatím jen na
    Chromu.

2.  Založit v daném pluginu nový skript (pro Chrome je tutorial
    [zde](http://hibbard.eu/tampermonkey-tutorial/), pro Firefox
    [zde](http://hayageek.com/greasemonkey-tutorial/)).

3.  Smazat kostru nového skriptu a nahradit ji skriptem, který si zkopírujete výše.

4.  Skript uložit.

5.  Používat KonText jako normálně -- skript už by podle adresy měl sám poznat,
    že se má spustit. Pokud se tak nestane, nejspíš to znamená, že je
    prohlížečový plugin (Tampermonkey nebo Greasemonkey) deaktivovaný a je
    potřeba jej znovu aktivovat.

[^1]: V předchozí verzi se po aplikaci libovolného filtru změnil obsah
hledacího boxu na parametry filtrování.
