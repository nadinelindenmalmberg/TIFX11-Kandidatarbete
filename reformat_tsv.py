################################################################################
## SKRIPT SOM AUTOMAGISKT FIXAR DIN QUALISYS TSV-FIL SÅ ATT PANDAS GILLAR DEN
## Skriven av Alexander Mayer, mars 2024

# Filen du vill ladda in, i samma mapp som du kör skriptet
TSV_FILENAME = '240306_v2_vals.tsv'

# Resultatet kommer vara en liknande fil som skapas med filmnamnet "ORIGINALFILNAMN_formatted.tsv"

CONVERT_TO_CSV = True

################################################################################


# laddar in filen
with open(TSV_FILENAME,'r',encoding='utf-8') as f:
    all_text = f.read()

# hittar rubrikerna för varje markör
header = ''
raise_header_error = True
for row in all_text.splitlines():
    words = row.split('\t')
    if words[0] == 'MARKER_NAMES':
        header = words[1:]
        raise_header_error = False
        break
if raise_header_error:
    raise Exception('Kunde inte hitta rubriken MARKER_NAMES i den givna tsv-filen, som krävs för att definiera namn på markörerna')
        

# lägger till -x , -y , -z på slutet av namnet på varje markör
new_header = ""
for name in header:
    new_header += f'{name}-x\t{name}-y\t{name}-z\t'

# fixar det nya innehållet, med all data direkt under en första rad med de nya markörnamnen
if len(all_text.split('Measured\n'))==2:
    new_text = new_header+'\n' + all_text.split('Measured\n')[1]
elif len(all_text.split('Mixed\n'))==2:
    new_text = new_header+'\n' + all_text.split('Mixed\n')[1]
else:
    raise Exception('FEL: Kunde inte identifiera var datan började (Dvs hittade inte en rad som slutar på `Mixed` eller `Measured`)')



if not CONVERT_TO_CSV:
    new_filename = TSV_FILENAME.replace('.tsv','_formatted.tsv')
else:
    # konverterar tsv till csv
    new_text = new_text.replace('\t',',')
    new_filename = TSV_FILENAME.replace('.tsv','_formatted.csv')

# sparar den nya filen
with open(new_filename,'w',encoding='utf-8') as f:
    f.write(new_text)