################################################################################
## SKRIPT SOM AUTOMAGISKT FIXAR DIN QUALISYS TSV-FIL SÅ ATT PANDAS GILLAR DEN
## Skriven av Alexander Mayer, mars 2024

# Välj filen du vill ladda in, i tsv-format
# Resultatet kommer vara en liknande fil som skapas med filmnamnet "ORIGINALFILNAMN_formatted.csv"


CONVERT_TO_CSV = True
################################################################################
import tkinter as tk
from tkinter import filedialog


# välj fil
root = tk.Tk(); root.withdraw()
tsv_filepath = filedialog.askopenfilename(filetypes=[("Qualisys data", "*.tsv")])
if not tsv_filepath:
    print('No file selected!')
    quit()

# laddar in filen
with open(tsv_filepath,'r',encoding='utf-8') as f:
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
new_header = new_header[:-1]

# fixar det nya innehållet, med all data direkt under en första rad med de nya markörnamnen
if len(all_text.split('Measured\n'))==2:
    new_text = new_header+'\n' + all_text.split('Measured\n')[1]
elif len(all_text.split('Mixed\n'))==2:
    new_text = new_header+'\n' + all_text.split('Mixed\n')[1]
else:
    raise Exception('FEL: Kunde inte identifiera var datan började (Dvs hittade inte en rad som slutar på `Mixed` eller `Measured`)')



if not CONVERT_TO_CSV:
    new_filepath = tsv_filepath.replace('.tsv','_formatted.tsv')
else:
    # konverterar tsv till csv
    new_text = new_text.replace('\t',',')
    new_filepath = tsv_filepath.replace('.tsv','_formatted.csv')

# sparar den nya filen
with open(new_filepath,'w',encoding='utf-8') as f:
    f.write(new_text)
print('Successfully generated '+str(new_filepath.split('/')[-1]))