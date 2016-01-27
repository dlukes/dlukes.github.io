Title: Úprava rozhraní konkordanceru KonText
Date: 2015-02-17
Tags: KonText, korpus, konkordance, NoSke, Bonito
Slug: kontext-interface-tweak
Summary: Skript, kterým si uživatel Českého národního korpusu může upravit rozhraní konkordanceru KonText.

# !POZOR!

K dispozici je nyní
[vylepšená verze níže popsaného skriptu]({filename}/ling/kontext_interface_tweak_update.md).

# Hledání v korpusech ČNK

[Český národní korpus](http://korpus.cz) je sbírka jazykových korpusů částečně
vytvářených [Ústavem Českého národního korpusu](http://ucnk.ff.cuni.cz) a
částečně jinými institucemi. Všechny jsou hostované na jednom serveru a
dostupné skrz různá vyhledávací rozhraní
(tzv. [konkordancery](http://wiki.korpus.cz/doku.php/pojmy:korpusovy_manazer)),
např. [NoSke](https://www.korpus.cz/corpora),
[Bonito](http://ucnk.ff.cuni.cz/bonito/index.php) či nejnověji
[KonText](https://kontext.korpus.cz). Koncem března 2015 ovšem bude podpora
starších rozhraní ukončena a nadále půjde k datům v ČNK přistupovat primárně
pouze přes KonText.

(Pokud vám odstavec výše nedává příliš smysl, s jazykovými korpusy se setkáváte
poprvé, ale chcete se dozvědět víc, raději si místo tohoto postu přečtěte,
[k čemu je takový korpus dobrý](http://wiki.korpus.cz/doku.php/pojmy:korpus), a
[zkuste si v něm něco pro zajímavost vyhledat](https://kontext.korpus.cz). Pokud
se vám při vzpomínce na Bonito či NoSke naopak zaskvěla slza v oku, čtěte dál!)

# <a id="background"></a>KonText vs. Bonito / NoSke

KonText má oproti starším rozhraním řadu výhod -- bohatší funkcionalitu, mnohé
pomůcky, které vám pomohou se zadáním složitějších dotazů (sestavení
morfologického tagu či podmínky `within`), a v neposlední řadě mnohem lépe
vypadá, což kupříkladu mně při práci působí jako balzám na duši. Nicméně
dlouholetí uživatelé ČNK byli jednoduše zvyklí na některé aspekty Bonita a
NoSke, které jim teď v KonTextu chybí.

Onehdy při rozhovoru s jedním z nich vyplavaly na povrch jako hodně důležité
dvě stížnosti:

1. Vrchní menu v KonTextu je zákeřné, schovává se, člověk nemá přehled nad
   dostupnými funkcemi. Oproti tomu NoSke má menu po straně a je permanentně
   rozvinuté, takže uživatel má všechny možnosti interakce s konkordancí
   soustavně jako na dlani.
2. Po zadání dotazu člověk často na základě konkordance zjistí, že jej
   potřebuje ještě trochu upravit / zjemnit. KonText si sice předchozí dotazy
   pamatuje, je ale potřeba se k nim doklikat; šikovnější by bylo, kdyby tato
   možnost byla dostupná přímo ze stránky konkordance v podobě nějakého
   zjednodušeného hledacího boxu. (NoSke tohle vlastně taky neumí, v Bonitu je
   to jednodušší.)

V obou případech jde o smysluplné požadavky, jenže KonText je poměrně velká a
složitá aplikace, takže i pokud se ČNK rozhodne do ní tyto podněty v nějaké
podobě zapracovat (např. jako možnost přepnutí zobrazení menu), bude nějakou
chvíli trvat, než se implementace navrhne, vytvoří, řádně otestuje a konečně
dostane k uživatelům. Nicméně aby bylo možné alespoň vyzkoušet, jak by zmíněné
změny vypadaly v praxi, dal jsem dohromady krátký skript, který již v
prohlížeči nahraný KonText trochu "přestaví" a upraví. Výsledek vypadá
následovně:

<img alt="Upravené rozhraní KonText." src="images/kontext_interface_tweak.png" style="max-width: 100%;">

Rovnou předesílám: ten skript je nevzhledný bastl přilepený na KonText
zvnějšku; proto taky bylo možné jej dát dohromady poměrně rychle, protože si
neklade nárok na spolehlivost, která se vyžaduje od oficiální verze
KonTextu. Je to spíš prototyp, jehož účelem je otestovat výše popsané změny v
praxi a získat představu o tom, zda a do jaké míry jsou přínosné. (Vlastní
zkušenost: po chvíli používání mi přijde přídatný hledací box nad konkordancí
hodně šikovný a užitečný.)

Teď k jádru pudla: **pokud máte zájem, můžete si KonText takto k obrazu svému**
(resp. k obrázku o odstavec výš) **upravit také** a vyzkoušet, jak vám takové
nastavení vyhovuje. Když se vám jedna z úprav bude líbit (nebo vás u toho
napadne jiná, kterou by si KonText zasloužil), můžete pak zadat
[požadavek na nový feature](https://podpora.korpus.cz/projects/kontext/issues/new).
Návod, jak si KonText upravit, následuje níže.

# Postup instalace skriptu

Skript samotný je k dispozici zde:

<script src="https://gist.github.com/dlukes/0764590b7a8464cbd000.js"></script>

K jeho zprovoznění jsou potřeba následující kroky:

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

# Omezení

Skript má pravděpodobně hromadu drobných much, na které se mi zatím nepodařilo
přijít -- budu se je snažit průběžně opravovat, když na ně padnu, nebo
[když mi o nich dáte vědět](pages/about.html). Krom toho má i některé mouchy, o
nichž už vím, ale bohužel toho s nimi nejde moc dělat.

Asi nejnápadnější je, že přidaný hledací box funguje jen na těch stránkách, kde
je původní dotaz i součástí adresy URL (což nejsou všechny -- třeba když
začnete **listovat konkordancí** na druhou stránku a dál, **dotaz je z adresy
vyjmut** a **pomocný hledací box tedy zmizí**). Ale vzhledem k tomu, že jeho
hlavní účel má být možnost lehce upravit dotaz po prvním rychlém nahlédnutí do
konkordance, snad to nebude takový problém. Pokud někdy bude podobný box řádně
přidán přímo do KonTextu, takovými nedostatky samozřejmě trpět nebude.

A ještě k **používání přidaného hledacího boxu**:

1. Typ dotazu, který je do něj potřeba zadat, je stejný jako ten, který jste
   při prvotním vyhledání konkordance zadali na stránce
   [Nový dotaz](https://kontext.korpus.cz/first_form). Pokud tento prvotní
   dotaz byl *Základní* dotaz, můžete pomocí rychlého boxu zadat jiný
   *Základní* dotaz; pokud to byl *CQL* dotaz, můžete ho upravit zas jen na
   další *CQL* dotaz. Důvodem je, že **smyslem** tohoto pomocného boxu **není
   nahradit plnohodnotný formulář** pro zadání dotazu, jen poskytnout rychlou
   možnost, jak již **zadaný dotaz upravit**.
2. Pomocný hledací box se objeví i poté, co na konkordanci provedete
   filtrování. V takové situaci se dá použít k tomu, abyste **pozměnili zadání
   aktuálního filtru**, tj. filtrování se provede znovu na původní konkordanci,
   ne na této již filtrované. Pokud chcete opakovaně filtrovat tu samou
   konkordanci a postupně podle daných kritérií vyřazovat / přidávat řádky, je
   potřeba místo hledacího boxu opakovaně použít menu *Filtr*.

# Komu si stěžovat, když to nebude fungovat

Skript je volně šiřitelný pod licencí
[GNU GPL v3](http://www.gnu.org/copyleft/gpl.html), takže se na něj neváže
žádná záruka. Když se vám ale nebude dařit jej zprovoznit, rád se pokusím
pomoct! Stačí se ozvat na adresu uvedenou [zde](pages/about.html).
