# Macondo Photo Project — guida al sito

## Struttura del sito
- `index.html` — home, tabellone con tre sezioni: Progetti, Collezioni, Sciolti
- `biografia.html` — la tua biografia
- `progetti/` — un file per ogni progetto documentario (es. `linea-est.html`, `tesi.html`). Ogni foto è una `<figure class="plate">` con didascalia stile "stazione — km/anno".
- `collezioni/` — `index.html` elenca le collezioni come card; ogni collezione ha una sua pagina (vedi `esempio.html`) con una griglia di foto.
- `sciolti.html` — griglia di scatti singoli senza progetto dietro.

## Come mettere online il sito (gratis)

## 1. Pubblicare su GitHub Pages
1. Vai su github.com e crea un account gratuito (se non l'hai già).
2. Crea un nuovo repository pubblico, es. `mio-portfolio`.
3. Carica tutti i file di questa cartella dentro il repository (si può fare trascinandoli dalla pagina web di GitHub, sezione "Add file → Upload files").
4. Vai su **Settings → Pages** del repository, e in "Branch" seleziona `main` (o `master`) e cartella `/root`. Salva.
5. Dopo 1-2 minuti il sito è online su un indirizzo tipo:
   `https://tuonomeutente.github.io/mio-portfolio/`

## 2. Aggiungere un dominio personalizzato (opzionale, ~10-15€/anno)
Se in futuro vuoi un indirizzo tipo `tuonome.com`, lo compri da un registrar (es. Namecheap, OVH) e lo colleghi da Settings → Pages → Custom domain. Non è necessario per iniziare.

## 3. Come aggiungere le foto
- Metti le immagini nella cartella `images/linea-est/` (o creane una nuova per un nuovo progetto).
- In `progetti/linea-est.html`, ogni foto è dentro un blocco `<figure class="plate">...</figure>`.
- Sostituisci il testo placeholder dentro `.plate-frame` con:
  `<img src="../images/linea-est/NOMEFILE.jpg" alt="Descrizione della foto">`
- Copia/incolla l'intero blocco `<figure class="plate">...</figure>` per aggiungere altre foto.

## 4. Come aggiungere un nuovo progetto
1. Duplica `progetti/linea-est.html`, rinominalo (es. `progetti/nuovo-progetto.html`).
2. Aggiorna titolo, testo introduttivo e foto.
3. In `index.html`, trasforma la riga "02 — In attesa" in un link vero, sul modello della riga "01 — Linea Est".

## 5. Come aggiungere una nuova collezione
1. Duplica `collezioni/esempio.html`, rinominalo.
2. Sostituisci titolo, descrizione e le foto nella `.loose-grid`.
3. In `collezioni/index.html`, copia il blocco `<a class="collection-card">...</a>` e collegalo alla nuova pagina.

## 6. Come aggiungere scatti sciolti
Apri `sciolti.html` e copia un blocco `<div class="thumb">...</div>`, sostituendolo con `<img src="images/sciolti/NOMEFILE.jpg" alt="Descrizione">`.

## 7. Cosa personalizzare subito
- Sostituisci `[Nome Cognome]` e `tua@email.com` in tutte le pagine.
- Scrivi il testo in `biografia.html`.
- Aggiungi il tuo ritratto al posto del placeholder `.bio-portrait`.
- Compila `progetti/tesi.html` con titolo e foto del tuo lavoro di fine studi.
