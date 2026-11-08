
# ASHI-CORE v2.1.0

### Modulo sperimentale opzionale dell'architettura NeuroCore

**Stato:** prototipo statistico online — validazione industriale e robotica non effettuata  
**Ultimo audit sperimentale:** 8 novembre 2026  
**Ruolo progettuale:** Adaptive Statistical Deviation Monitor

---

## 1. Scopo del modulo

**ASHI-CORE** è progettato come monitor statistico di deviazioni (*Adaptive Statistical Deviation Monitor*).

Riceve un valore numerico per campione, aggiorna le proprie statistiche interne e restituisce un allarme binario quando il valore supera una soglia adattiva.

All'interno di **NeuroCore**, il suo ruolo proposto è quello di un **layer opzionale e sostituibile di osservazione statistica**.

ASHI-CORE non costituisce:

- Un controllore robotico.
- Un modello di previsione dei guasti.
- Un sistema di diagnostica causale.
- Un modello autonomo di comprensione dello stato fisico.
- Un sistema completo di gestione della stabilità dinamica.

### Architettura proposta

L'integrazione seguente è una proposta progettuale, non ancora validata su hardware robotico.

```text
┌─────────────────────────────────────────────┐
│           SENSORI / TELEMETRIA              │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          PRE-ELABORAZIONE DEI DATI          │
│   Costruzione di un indicatore scalare      │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│               ASHI-CORE                     │
│      Monitor statistico di deviazione       │
│           [LAYER OPZIONALE]                 │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          SEGNALAZIONI STATISTICHE           │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│           SUPERVISORE NEUROCORE             │
│      + altri operatori dinamici             │
└─────────────────────────────────────────────┘
```

Il supervisore e le eventuali azioni di regolazione sono esterni al kernel ASHI.

Il modulo può essere rimosso o sostituito senza assumere che l'intera architettura NeuroCore dipenda dal suo funzionamento.

---

## 2. Funzionamento matematico implementato

Il file sorgente `ashicore_v210.c` implementa un kernel statistico incrementale.

Per ogni campione in ingresso, il sistema mantiene:

- Numero cumulativo di osservazioni.
- Media cumulativa.
- Stima incrementale della varianza.
- Deviazione standard campionaria.
- Soglia statistica adattiva.

### 2.1 Aggiornamento della media

Dato un campione $x_t$, la media viene aggiornata secondo:

$$
\mu_t = \mu_{t-1} + \frac{x_t-\mu_{t-1}}{t}
$$

### 2.2 Aggiornamento della varianza

Il kernel utilizza un aggiornamento incrementale di tipo **Welford**.

Definendo:

$$
\delta_t=x_t-\mu_{t-1}
$$

$$
\delta'_t=x_t-\mu_t
$$

la somma cumulativa degli scarti quadratici viene aggiornata mediante:

$$
M_{2,t}=M_{2,t-1}+\delta_t\delta'_t
$$

La varianza campionaria è:

$$
s_t^2=\frac{M_{2,t}}{t-1}
$$

e la deviazione standard:

$$
\sigma_t=\sqrt{\frac{M_{2,t}}{t-1}}
$$

per $t>1$.

### 2.3 Soglia adattiva

La soglia utilizzata dal kernel è:

$$
\boxed{T_t=\mu_t+K_c\sigma_t}
$$

con:

$$
\boxed{K_c=1.441}
$$

La decisione binaria è:

$$
A_t=
\begin{cases}
1 & \text{se } x_t>T_t\\
0 & \text{altrimenti}
\end{cases}
$$

Dove:

- $x_t$ è il campione corrente.
- $\mu_t$ è la media cumulativa aggiornata.
- $\sigma_t$ è la deviazione standard aggiornata.
- $K_c$ è la costante del kernel.
- $A_t$ è l'uscita binaria.

### 2.4 Relazione con lo Z-score

Per $\sigma_t>0$, la condizione di allarme è equivalente a:

$$
\boxed{\frac{x_t-\mu_t}{\sigma_t}>1.441}
$$

Pertanto, il nucleo decisionale di ASHI-CORE v2.1.0 corrisponde a un **test Z-score cumulativo post-aggiornamento** con soglia fissa pari a 1,441.

Le statistiche includono il campione corrente.

Per i primi quattro campioni, il kernel restituisce sempre:

$$
A_t=0 \qquad \text{per } t<5
$$

### 2.5 Limiti dell'implementazione

Il codice C originale non implementa direttamente:

- Rilevamento esplicito di transizioni di fase.
- Stima della vita utile residua (*Remaining Useful Life*, RUL).
- Analisi multivariata dei sensori.
- Diagnostica causale.
- Controllo robotico.
- Persistenza temporale degli allarmi.

Il campo `trend_buffer[10]` è presente nella struttura del kernel, ma non partecipa alla logica decisionale attuale.

**Nota sul parametro $K_c$:** il valore 1,441 è una costante dell'implementazione esaminata. I benchmark disponibili non ne dimostrano l'universalità fisica, biologica o statistica.

---

## 3. Funzione proposta all'interno di NeuroCore

ASHI-CORE può fornire all'architettura NeuroCore:

1. Un segnale binario di deviazione statistica aggiornato campione per campione.
2. Un modulo deterministico con stato interno limitato.
3. Un'implementazione C compatta.
4. Un componente indipendente, sostituibile e confrontabile con altri rilevatori statistici.

### Persistenza degli allarmi

Il kernel originale non calcola direttamente la persistenza.

Nei benchmark NASA C-MAPSS, la persistenza è stata valutata mediante una regola esterna:

$$
P_t=
\mathbb{1}
\left[
\sum_{i=t-14}^{t}A_i\geq10
\right]
$$

per le finestre complete di 15 campioni.

In altri termini, viene riconosciuta una condizione persistente quando almeno **10 degli ultimi 15 campioni** hanno prodotto un allarme.

Questa regola appartiene al **protocollo sperimentale**, non al kernel C originale.

---

## 4. Applicazioni progettuali candidate

Le applicazioni seguenti rappresentano possibili scenari di integrazione, non validazioni sperimentali su dispositivi fisici.

| Ambito | Possibile ingresso | Funzione candidata |
|---|---|---|
| Attuatori elettromeccanici | Indicatore di corrente o vibrazione | Segnalare deviazioni dal comportamento storico |
| Robot industriali | Indicatore composito di carico o stato | Fornire un segnale aggiuntivo al supervisore |
| Sistemi di raffreddamento | Indicatore termico normalizzato | Segnalare valori elevati rispetto alla storia |
| Banchi prova | Indicatore scalare derivato dai sensori | Monitorare deviazioni online |
| NeuroCore | Indice di stato pre-elaborato | Fornire un ingresso statistico opzionale |

**Stato della validazione:** nessuna delle applicazioni elencate è stata verificata mediante prove operative su hardware robotico reale.

---

## 5. Benchmark sperimentale: NASA C-MAPSS

### 5.1 Dataset e protocollo

Il benchmark ha utilizzato le traiettorie complete di addestramento del dataset **NASA C-MAPSS**, suddiviso nei gruppi:

- FD001
- FD002
- FD003
- FD004

Il totale comprende:

| Partizione | Motori |
|---|---:|
| Calibrazione | 354 |
| Valutazione | 355 |
| **Totale** | **709** |

La suddivisione è stata effettuata per motore, utilizzando un seed deterministico.

È stato eseguito un solo split.

Il kernel C originale è stato compilato e valutato mantenendo:

$$
K_c=1.441
$$

senza modificare la logica decisionale.

### 5.2 Costruzione dell'ingresso

Gli ingressi forniti ad ASHI non corrispondevano direttamente ai sensori grezzi.

Una fase esterna ha costruito un indicatore scalare utilizzando:

- Deviazioni multicanale.
- Riferimenti derivati dai primi 25 cicli dei motori di calibrazione.
- Trattamento dei differenti regimi operativi.
- Trasformazione delle informazioni sensoriali in un unico segnale numerico.

Questa elaborazione contribuisce alle prestazioni osservate.

**Non è implementata all'interno del kernel ASHI-CORE.**

### 5.3 Comparazione con altri rilevatori

Le soglie dei comparatori sono state calibrate sui motori di calibrazione per avvicinarsi alla frequenza iniziale degli allarmi grezzi di ASHI.

I risultati riportati sono medie sui **355 motori di valutazione**.

| Rilevatore | Allarmi grezzi nel primo 25% | Persistenza nell'ultimo 25% |
|---|---:|---:|
| CUSUM | 7,00% | **94,52%** |
| Soglia fissa | 6,60% | **89,62%** |
| ASHI-CORE originale | 7,79% | **86,94%** |
| Z-score cumulativo calibrato | 7,94% | 84,08% |
| Z-score mobile, 30 campioni | 7,66% | 10,57% |
| EWMA z | 8,12% | 0,00% |

La persistenza finale rappresenta la frazione media dei cicli dell'ultimo quarto della traiettoria in cui risulta soddisfatta la regola di persistenza.

Non rappresenta l'accuratezza diagnostica di un guasto.

### 5.4 Differenze appaiate

**ASHI-CORE rispetto allo Z-score cumulativo calibrato:**

$$
\Delta P=86.94\%-84.08\%
$$

$$
\boxed{\Delta P\approx+2.86\ \text{punti percentuali}}
$$

Intervallo bootstrap al 95%:

$$
CI_{95\%}=[+2.25,\,+3.51]\ \text{pp}
$$

**ASHI-CORE rispetto a CUSUM:**

$$
\Delta P=86.94\%-94.52\%
$$

$$
\boxed{\Delta P\approx-7.57\ \text{punti percentuali}}
$$

Intervallo bootstrap al 95%:

$$
CI_{95\%}=[-9.34,\,-5.91]\ \text{pp}
$$

Le piccole differenze tra sottrazioni dei valori arrotondati e risultati appaiati dipendono dalla precisione numerica utilizzata nei calcoli originali.

### 5.5 Risultato osservato

Nel protocollo sperimentale adottato:

- ASHI-CORE ha superato lo Z-score cumulativo calibrato nella metrica di persistenza finale.
- CUSUM ha ottenuto una persistenza superiore ad ASHI.
- La soglia fissa ha ottenuto una persistenza superiore ad ASHI.
- Le baseline adattive EWMA e Z-score mobile hanno prodotto una persistenza finale inferiore.

CUSUM è stato utilizzato come **comparatore statistico**, non come rappresentazione di un prodotto industriale certificato.

Questi risultati non dimostrano una superiorità generale rispetto ai sistemi PHM commerciali o ai modelli moderni di apprendimento automatico.

### 5.6 Limiti dell'interpretazione

Il dataset non fornisce etichette verificate dell'istante di insorgenza del guasto.

Pertanto:

- Il primo quarto della traiettoria è utilizzato come proxy temporale iniziale.
- L'ultimo quarto è utilizzato come proxy temporale finale.
- I segmenti non costituiscono periodi fisicamente certificati come sani o degradati.

La persistenza degli allarmi non equivale a:

- Accuratezza diagnostica.
- Tempo di preavviso validato.
- Previsione della vita utile residua.
- Identificazione causale del degrado.

Inoltre, metodi adattivi come EWMA e Z-score mobile possono ridurre gli allarmi persistenti proprio perché aggiornano il riferimento durante il cambiamento del segnale.

Il confronto valuta quindi **la metrica selezionata**, non tutte le capacità dei rilevatori.

---

## 6. Riferimento adattivo e limite progettuale

La media e la deviazione standard del kernel vengono aggiornate continuamente.

Di conseguenza, anche i valori acquisiti durante il degrado contribuiscono al riferimento statistico.

Formalmente:

$$
\mu_t=f(x_1,x_2,\ldots,x_t)
$$

$$
\sigma_t=g(x_1,x_2,\ldots,x_t)
$$

Il riferimento non rimane quindi congelato rispetto a una fase iniziale.

Questa proprietà deriva direttamente dalla logica implementata e non dimostra che il kernel riconosca o corregga autonomamente il degrado.

Un eventuale confronto tra:

1. Riferimento cumulativo adattivo.
2. Riferimento iniziale congelato.

richiederebbe un esperimento dedicato.

La seconda modalità non è una capacità già dimostrata dal kernel originale.

---

## 7. Altri esperimenti e perimetro delle evidenze

L'archivio sperimentale consolidato conserva anche:

- Esperimenti esplorativi EEGMMIDB.
- Prove del kernel C su segnali EEG.
- Test di tipo watchdog.
- Confronti con baseline statistiche.
- Analisi NASA C-MAPSS.
- Test successivi di persistenza.
- Analisi comparative con operatori NeuroCore.

I protocolli e i risultati devono essere consultati nei rispettivi file sperimentali.

Nel loro insieme, questi esperimenti **non costituiscono una validazione clinica, robotica o interdominio del valore $K_c$**.

Un confronto esplorativo su EEGMMIDB ha utilizzato un'operazionalizzazione proxy degli operatori NeuroCore, non un'implementazione autenticata degli operatori originali.

Pertanto, tale esperimento non deve essere presentato come validazione degli operatori originali NeuroCore.

---

## 8. Riproducibilità

I principali file di riferimento del benchmark consolidato sono:

```text
ashicore_v210.c
FINAL_AUDIT.md
definitive_extra.py
definitive_protocol.json
definitive_summary.csv
definitive_by_fd.csv
definitive_per_engine.csv
definitive_paired_ci.csv
```

L'archivio di riferimento è:

```text
ASHI_CORE_DEFINITIVE_ALL_TESTS_2026-11-08.zip
```

I dataset grezzi NASA C-MAPSS non sono inclusi nell'archivio e devono essere acquisiti separatamente.

Le valutazioni derivano da uno split deterministico.

Non è stata effettuata una validazione indipendente su hardware reale.

---

## 9. Provenienza dello sviluppo

L'impostazione concettuale e le formule del progetto sono state fornite dal proponente.

La traduzione in codice C e parte delle attività di analisi sono state svolte con assistenza di strumenti di intelligenza artificiale.

Questa dichiarazione distingue:

- Paternità progettuale.
- Implementazione software assistita.
- Valutazione sperimentale.
- Validazione scientifica indipendente.

Non costituisce una verifica indipendente dell'originalità matematica.

---

## 10. Stato conclusivo

**ASHI-CORE v2.1.0** è un monitor statistico online, candidato a operare come layer opzionale e sostituibile nell'architettura NeuroCore.

Nel benchmark NASA C-MAPSS descritto ha prodotto risultati riproducibili nel protocollo adottato.

Sulla metrica di persistenza finale:

$$
P_{\mathrm{CUSUM}}>P_{\mathrm{ASHI}}>P_{\mathrm{Z\text{-}score\ cumulativo}}
$$

con:

$$
P_{\mathrm{ASHI}}=86.94\%
$$

I risultati disponibili non dimostrano:

- Superiorità generale rispetto allo stato dell'arte.
- Capacità autonoma di interpretazione fisica.
- Una legge universale di transizione.
- Efficacia operativa su sistemi robotici.
- Validazione indipendente in ambiente industriale.

**ASHI-CORE rimane un componente statistico sperimentale con un ruolo architetturale definito, prestazioni misurate e limiti documentati.**
