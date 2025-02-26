from settings import settings, logger

logger.info(f"directory: {settings.basedir}")


import warnings
warnings.simplefilter('ignore')

import pandas as pd
import sqlite3

# %% [markdown]
# Zet de volgende bestanden in een makkelijk terug te vinden map:
# - go_sales_train.sqlite
# - go_crm_train.sqlite
# - go_staff_train.sqlite

# %% [markdown]
# Bestudeer de bovenste 3 bestanden in DB Browser (SQLite), <a href="https://sqlitebrowser.org/dl/">hier</a> te downloaden. Wat valt je op qua datatypen?<br>

# %% [markdown]
# ## Databasetabel inlezen

# %% [markdown]
# Creëer een databaseconnectie met het bestand go_sales_train.sqlite.

# %%
db_path = 'Sqlite files/go_sales_train.sqlite'

sales_conn = sqlite3.connect(db_path)
sales_conn

# %% [markdown]
# <b>Let goed op:</b><br>
# Als je per ongeluk een verkeerde bestandsnaam ingeeft, maakt Python zélf een leeg databasebestand aan! Er ontstaat dan dus een nieuwe .sqlite, en dat is nadrukkelijk <u>niet de bedoeling.</u>

# %% [markdown]
# Gebruik de onderstaande sql_query om te achterhalen welke databasetabellen in go_sales_train zitten.

# %%
sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#Vul dit codeblok verder in
tables = pd.read_sql(sql_query, sales_conn)
print(tables)

# %% [markdown]
# Krijg je lege output? Dan heb je per ongeluk een leeg  databasebestand (.sqlite) aangemaakt.<br>
# Lees de informatie onder het kopje <u>Let goed op:</u> hierboven nog eens goed door.

# %% [markdown]
# Gebruik de gecreëerde databaseconnectie om de resultaten van de volgende query in een DataFrame te zetten:<br>
# *SELECT * FROM sales_staff* 

# %%
sales_staff = pd.read_sql("SELECT * FROM sales_staff", sales_conn)
sales_staff

# %% [markdown]
# ## Datumkolommen

# %% [markdown]
# Zoals je misschien al hebt gezien in DB Browser, zijn datums als TEXT opgeslagen, en niet als DATE, DATETIME o.i.d. Hier moeten we dus nog even "typische datumkolommen" van maken. Dat doen we met de volgende code:

# %%
sales_staff['DATE_HIRED'] = pd.to_datetime(sales_staff['DATE_HIRED'])
sales_staff.dtypes

# %% [markdown]
# Als we hier het jaar uit willen halen, schrijven we:

# %%
pd.DatetimeIndex(sales_staff['DATE_HIRED']).quarter

# %% [markdown]
# Deze zelfde syntax is te gebruiken voor het extraheren van kwartalen, maanden, weken en dagen. Probeer het maar eens!

# %% [markdown]
# ## DataFrames uitsplitsen en opbouwen met Series

# %% [markdown]
# De volgende 5 kolommen hebben betrekking op de contactdetails van elke medewerker in dit DataFrame:
# - SALES_STAFF_CODE
# - WORK_PHONE
# - EXTENSION
# - FAX
# - EMAIL
# 
# Maak van elk van deze 5 kolommen een serie.

# %%
sales_staff.loc[:,  
                ['SALES_STAFF_CODE', 'WORK_PHONE',
                  'EXTENSION', 'FAX', 'EMAIL']]


# %% [markdown]
# Zet allevijf gecreëerde series als kolommen naast elkaar in een DataFrame (*contact_details*). Gebruik pd.concat(...)<br>
# Hulpvraag: welke waarde geef je aan de axis-parameter?

# %%
contact_details = pd.concat([sales_staff['SALES_STAFF_CODE'], 
                             sales_staff['WORK_PHONE'], 
                             sales_staff['EXTENSION'], 
                             sales_staff['FAX'], 
                             sales_staff['EMAIL']], axis= 1)
contact_details

# %% [markdown]
# ## Series en DataFrames maken vanuit lists en dictionaries

# %% [markdown]
# Met .head(*getal*) kan je de bovenste *getal* rijen van een tabel selecteren.<br>
# Selecteer op deze manier de bovenste 5 rijen van *contact_details*.<br>
# Sla dit resultaat op in een nieuw DataFrame.

# %%
contact_details.head(5)

# %% [markdown]
# Aan deze 10 rijen met contactdetails willen we 3 kolommen toevoegen: 'FIRST_LANGUAGE', 'SECOND_LANGUAGE' & 'THIRD_LANGUAGE'.<br>
# Iedereens 'First Language' is Engels, afgekort 'EN'. Maak een lijst waarin 5x 'EN' staat.<br>
# Converteer deze lijst vervolgens naar een serie en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.

# %%
eerste_taal = ['EN'] * 5

taalseries = pd.Series(eerste_taal, name='FIRST_LANGUAGE')

ENsprekers_lijst = pd.concat([taalseries, 
                             sales_staff['SECOND_LANGUAGE'], 
                             sales_staff['THIRD_LANGUAGE']], axis= 1)

ENsprekers_lijst.head(5)

# %% [markdown]
# Maak nu de tweede kolom ('SECOND_LANGUAGE'). Maak daarvoor een dictionary, met daarin...
# - Als keys: alle indexen uit het resultaat van het vorige codeblok.
# - Als values: bij de eerste 3 elementen 'FR' (Frankrijk), bij de laatste 2 'DE' (Duitsland).
# 
# Maak vervolgens ook hier weer een serie van en voeg ook deze weer horizontaal samen met het rsultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.

# %%
mijn_dict = {'EN' }

# %% [markdown]
# Maak ten slotte de derde kolom ('THIRD_LANGUAGE') door een dictionary te maken met daarin...
# - Als key: de naam van de nieuwe kolom. Zie je het verschil qua keys met de vorige opdracht?
# - Als waarde: een lijst met daarin 'NL', 'NL', 'JPN', 'JPN', 'KOR'.
# 
# Converteer deze dictionary nu naar een DataFrame en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Waarom hoef je hierna de nieuw ontstane kolom geen passende naam meer te geven?

# %%


# %% [markdown]
# ## Data toevoegen

# %% [markdown]
# ### Rijen

# %% [markdown]
# Gebruik de originele databasetabel *sales_staff*.<br>
# Voeg een extra rij toe met eigen invulling. Zorg ervoor dat de index netjes doorloopt.<br>
# Hulpvraag: welke waarde geef je nu aan axis?

# %%
data = ['S101', 'John', 'Doe', 'representative', '123456789', 123, '123456789', 'voorbeeld@example.com', '2023-01-01', 1, 'John Doe']
sales_staff.loc[len(sales_staff)] = data
sales_staff

# %% [markdown]
# ### Kolommen

# %% [markdown]
# Voeg een kolom *FULL_NAME* toe die de waarden van *FIRST_NAME* en *LAST_NAME* achter elkaar zet, gescheiden door een spatie.

# %%
sales_staff['FULL_NAME'] = sales_staff['FIRST_NAME'] + ' ' + sales_staff['LAST_NAME']
sales_staff

# %% [markdown]
# ## Data wijzigen

# %% [markdown]
# ### Datatypen

# %% [markdown]
# Door het attribuut .dtypes van een DataFrame op te vragen krijg je een serie die per kolom het datatype weergeeft. Doe dit bij de originele databasetabel *sales_staff*

# %%
sales_staff.dtypes

# %% [markdown]
# Hier valt op dat elke kolom het datatype 'object' heeft: Python leest dus alles als string. Wiskundige operaties zijn hierdoor niet mogelijk.<br>
# We kunnen proberen om kolommen met getallen, bijvoorbeeld de 'extension', te converteren naar een int. Zie onderstaande code.

# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(int)
sales_staff.dtypes

# %% [markdown]
# Dit lukt echter niet, omdat er in de kolom 'EXTENSION' lege waarden zitten die niet geconverteerd kunnen worden naar een int.<br>
# Wél kan je deze naar een float converteren, zie onderstaande code:

# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(float)
sales_staff.dtypes

# %% [markdown]
# Als we in de rij van 'EXTENSION' kijken zien we dat de conversie van het datatype nu is gelukt.<br>
# Dit is <b>randvoorwaardelijk</b> voor het uitvoeren van wiskundige operaties.<br>

# %% [markdown]
# ### Rijen

# %% [markdown]
# Zorg er nu voor dat bij alle extensions 1 wordt opgeteld.

# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'] + 1
sales_staff

# %% [markdown]
# Elke 'Branch Manager' wordt nu 'General Manager'. Schrijf code zodat deze wijziging doorgevoerd wordt in het DataFrame.

# %%
sales_staff.loc[sales_staff['POSITION_EN'] == 'Branch Manager', 'POSITION_EN'] = 'General Manager'
sales_staff

# %% [markdown]
# ### Kolommen

# %% [markdown]
# Verander de kolomnaam 'POSITION_EN' naar 'POSITION'.

# %%
sales_staff.rename(columns = {'POSITION_EN': 'POSITION'}, inplace = True)
sales_staff

# %% [markdown]
# ## Data verwijderen

# %% [markdown]
# ### Rijen

# %% [markdown]
# De medewerkers op indexen 99, 100 en 101 hebben helaas ontslag genomen.<br>
# Verwijder de bijbehorende rijen uit het DataFrame. Gebruik slechts één keer de .drop()-methode.

# %%
sales_staff.drop([sales_staff.index[99], sales_staff.index[100], sales_staff.index[101]], inplace = True)
sales_staff


# %% [markdown]
# ### Kolommen

# %% [markdown]
# Faxen zijn inmiddels ouderwets: niemand gebruikt zijn/haar faxnummer nog.<br>
# Verwijder de bijbehorende kolom uit het DataFrame.

# %%
#sales_staff.drop(columns = ['FAX'], axis= 1, inplace = True)
sales_staff.columns
# de FAX kolom zit er niet in, maar de kolom was nog niet verwijderd


