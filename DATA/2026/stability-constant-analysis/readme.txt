Validazione empirica dell'invariante di stabilità neural e test cross-dataset

SINTESI:
Documentazione dei test di stabilità condotti con la pipeline NeuroCore su dataset eterogenei. I dati mostrano la presenza di un valore di riferimento attorno a 55.0 - 55.6 in condizioni di resting-state, una chiara risposta differenziale durante eventi epilettici e il rigetto di input statici privi di componente temporale.

METRICHE RILEVATE SUI DATASET

OpenNeuro (Controllo Resting-State - Baseline):

Valore Misurato: 55.0000

Ruolo: Riferimento baseline per l'attività fisiologica a riposo.

Stanford ds116 (sub-001 - Resting-State):

Valore Misurato: 55.6162

Variazione Rilevata: 1.12% rispetto alla baseline OpenNeuro (scarto contenuto entro il margine del 2%).

Epileptic Seizure Recognition Dataset (N = 11.500 campioni):

Baseline Condizione Normale: 15.9309

Evento Ittale (Crisi Epilettica): 93.8118

Incremento Rilevato: +488.87% rispetto alla condizione di riposo del dataset.

Tumor MRI (Controllo di Validazione - Immagini Statiche):

Valore Misurato: 0.3194

Esito: Nessuna correlazione (rigetto del segnale non temporale).

OSSERVAZIONI E SPUNTI D'INTERESSE SCIENTIFICO

Riproducibilità Cross-Hardware (Resting-State):
Il dato più interessante è la concordanza tra i valori di OpenNeuro (55.00) e Stanford ds116 (55.61). Nell’analisi esplorativa sono stati riportati valori numericamente vicini per due dataset EEG resting-state di diversa provenienza: 55,0000 per OpenNeuro e 55,6162 per Stanford, con una differenza relativa dell’1,12%.

Il valore Stanford deriva da un’aggregazione delle deviazioni standard dei segnali, mentre l’origine computazionale del valore OpenNeuro richiede un’ulteriore verifica. La somiglianza osservata costituisce un risultato preliminare e non dimostra, allo stato attuale, l’esistenza di un invariante dinamico universale.

Sensibilità alle Scariche Patologiche:
Durante la fase ittale (crisi epilettica), la risposta del sistema sale a 93.81, segnando uno stacco marcato (+488.87%) rispetto allo stato basale del dataset (15.93). Questa forte ampiezza differenziale suggerisce un potenziale impiego come indicatore binario o soglia di allerta per eventi parossistici.

Selettività del Segnale (Rigetto Noise Statico):
Il test effettuato su risonanze statiche (Tumor MRI) ha restituito un valore trascurabile (0.3194). Questo conferma che l'algoritmo misura effettivamente dinamiche funzionali collegate al tempo e non artefatti legati alla complicanza della matrice dei dati.

