from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_IT_IT: tuple[ManualSection, ...] = (
	ManualSection(
		id="panoramica",
		title="Panoramica",
		paragraphs=(
			"Linceu Lighthouse ti aiuta a ispezionare, monitorare e analizzare file e cartelle in più posizioni del tuo computer."
			" Centralizza le informazioni degli elementi e fornisce strumenti per filtrare, generare statistiche ed estrarre metadati.",
		),
	),
	ManualSection(
		id="schermata-principale",
		title="Schermata Principale — Elementi",
		bullets=(
			to_unicode_bold("Barra strumenti:") + " Accesso rapido a: Aggiungi Cartella, Avvia Scansione, Interrompi, Aggiorna e Preferenze.",
			to_unicode_bold("Selettore cartelle:") + " Area per aggiungere, rimuovere o cambiare le cartelle monitorate.",
			to_unicode_bold("Tabella elementi:") + " Elenco centrale con colonne (Nome, Tipo, Dimensione, Data, Evento) con supporto a ordinamento/filtri.",
			to_unicode_bold("Pannello dettagli:") + " Mostra metadati e azioni rapide per l'elemento selezionato.",
			to_unicode_bold("Messaggi & progresso:") + " Mostra notifiche, log e barre di progresso.",
			to_unicode_bold("Statistiche:") + " Area per grafici e report generati dai dati raccolti.",
		),
	),
	ManualSection(
		id="iniziare",
		title="Come Iniziare",
		bullets=(
			"Apri l'applicazione tramite collegamento o eseguibile.",
			"Clicca " + to_unicode_bold("Aggiungi Cartella") + " e scegli la cartella da monitorare.",
			"Esegui una scansione iniziale con " + to_unicode_bold("Avvia") + "/" + to_unicode_bold("Scansione") + ".",
			"Attendi; gli elementi appariranno con i metadati disponibili.",
			"Abilita " + to_unicode_bold("Monitoraggio continuo") + " per rilevare automaticamente le modifiche.",
		),
	),
	ManualSection(
		id="modalita-operazione",
		title="Modalità di Funzionamento",
		bullets=(
			to_unicode_bold("Scansione singola:") + " Controllo immediato delle cartelle selezionate.",
			to_unicode_bold("Monitoraggio continuo:") + " Osservazione in tempo reale delle modifiche e aggiornamento automatico della tabella.",
			to_unicode_bold("Elaborazione batch:") + " Estrazione dei metadati o esecuzione di azioni su più file contemporaneamente.",
		),
	),
	ManualSection(
		id="capire-tabella",
		title="Comprendere la Tabella degli Elementi",
		paragraphs=(
			"Ogni colonna mostra una proprietà dell'elemento. Usa ordinamento, filtri e selezione per trovare e ispezionare gli elementi rapidamente.",
		),
		bullets=(
			to_unicode_bold("Nome:") + " Nome file o cartella; doppio clic per aprire.",
			to_unicode_bold("Tipo:") + " Tipo rilevato (immagine, video, documento, cartella).",
			to_unicode_bold("Dimensione:") + " Visualizzata in unità leggibili (KB/MB/GB).",
			to_unicode_bold("Data:") + " Ultima modifica o data evento registrata.",
			to_unicode_bold("Evento:") + " Azione rilevata (creato, modificato, spostato, eliminato).",
		),
	),
	ManualSection(
		id="pannello-dettagli",
		title="Pannello Dettagli e Metadati",
		paragraphs=(
			"La selezione di un elemento mostra i metadati rilevanti e azioni rapide (apri cartella, copia percorso, aggiorna metadati).",
		),
		bullets=(
			to_unicode_bold("Percorso completo:") + " Posizione del file sul disco.",
			to_unicode_bold("Autore / Creatore:") + " Se presente nei metadati.",
			to_unicode_bold("Dimensioni:") + " Per le immagini (larghezza × altezza).",
			to_unicode_bold("Durata:") + " Per audio/video.",
			to_unicode_bold("Bitrate:") + " Per i media, se disponibile.",
			to_unicode_bold("Permessi:") + " Indica protezioni o restrizioni di scrittura.",
		),
	),
	ManualSection(
		id="azioni-file",
		title="Azioni sui File",
		bullets=(
			to_unicode_bold("Apri:") + " Apri con l'app predefinita di sistema (doppio clic o pulsante Apri).",
			to_unicode_bold("Copia / Sposta:") + " Usa copia/incolla o trascina e rilascia per spostare file tra cartelle.",
			to_unicode_bold("Rinomina / Elimina:") + " Usa il menu contestuale; le azioni permanenti richiedono conferma.",
			to_unicode_bold("Ripristina:") + " Quando disponibile, recupera eliminazioni recenti con la funzione di ripristino.",
			to_unicode_bold("Proprietà:") + " Visualizza metadati completi e cronologia eventi del file.",
		),
	),
	ManualSection(
		id="ricerca-filtri",
		title="Ricerca e Filtri",
		bullets=(
			to_unicode_bold("Ricerca:") + " Inserisci termini nella casella di ricerca per trovare elementi per nome o contenuto.",
			to_unicode_bold("Filtri:") + " Applica filtri per tipo, dimensione, data o evento per restringere i risultati.",
			to_unicode_bold("Combina filtri:") + " Usa più filtri insieme per risultati precisi.",
		),
	),
	ManualSection(
		id="salva-ripristina",
		title="Salvataggio e Ripristino Vista",
		bullets=(
			to_unicode_bold("Salva stato:") + " Salva layout colonne e filtri correnti come profilo.",
			to_unicode_bold("Ripristina:") + " Carica un profilo salvato per recuperare layout e filtri.",
		),
	),
	ManualSection(
		id="elaborazione-batch",
		title="Elaborazione Batch",
		paragraphs=(
			"Seleziona più elementi per estrarre metadati o eseguire azioni batch. Sono disponibili progresso e controlli per mettere in pausa o annullare.",
		),
		bullets=(
			to_unicode_bold("Avvia estrazione:") + " Seleziona elementi ed esegui l'estrazione metadati batch.",
			to_unicode_bold("Monitora progresso:") + " Segui tramite barra di progresso e pannello messaggi.",
			to_unicode_bold("Pausa/Annulla:") + " Usa i controlli forniti per interrompere l'elaborazione.",
		),
	),
	ManualSection(
		id="rapporti-statistiche",
		title="Report e Statistiche",
		paragraphs=(
			"La sezione statistiche produce grafici su tipi di file, utilizzo disco e trend eventi. Esporta immagini o CSV per analisi esterne.",
		),
		bullets=(
			to_unicode_bold("Genera grafici:") + " Seleziona metriche per visualizzare distribuzioni e trend.",
			to_unicode_bold("Esporta:") + " Salva grafici come immagini o esporta dati in CSV.",
		),
	),
	ManualSection(
		id="struttura-directory",
		title="Struttura Directory",
		bullets=(
			to_unicode_bold("Albero directory:") + " Naviga per selezionare cartelle monitorate e verificare il loro stato.",
			to_unicode_bold("Azioni nell'albero:") + " Crea, rinomina o elimina cartelle dal menu contestuale.",
		),
	),
	ManualSection(
		id="monitoraggio-eventi",
		title="Monitoraggio Eventi",
		bullets=(
			to_unicode_bold("Tipi di evento:") + " Creazione, modifica, rimozione e spostamento.",
			to_unicode_bold("Vista tempo reale:") + " Eventi recenti sono evidenziati per ispezione rapida.",
			to_unicode_bold("Notifiche:") + " Configura avvisi visivi o sonori nelle Preferenze.",
		),
	),
	ManualSection(
		id="preferenze-it",
		title="Preferenze",
		paragraphs=(
			"Regola lingua, comportamento di scansione, notifiche e aggiornamenti. Controlla queste impostazioni dopo l'installazione.",
		),
		bullets=(
			to_unicode_bold("Lingua:") + " Scegli la lingua dell'interfaccia.",
			to_unicode_bold("Scansione:") + " Configura periodicità, profondità ed esclusioni.",
			to_unicode_bold("Notifiche:") + " Abilita o disabilita gli avvisi.",
			to_unicode_bold("Aggiornamenti:") + " Scegli controlli automatici o manuali.",
		),
	),
	ManualSection(
		id="problemi-comuni-it",
		title="Problemi Comuni e Soluzioni",
		bullets=(
			to_unicode_bold("Scansione bloccata o errore:") + " Attendi; se persiste, riavvia la scansione o l'applicazione.",
			to_unicode_bold("Elementi mancanti:") + " Verifica che la cartella sia stata aggiunta e che l'app abbia permessi di lettura.",
			to_unicode_bold("Impossibile aprire:") + " Assicurati che esista un'app associata al tipo di file.",
			to_unicode_bold("Metadati mancanti:") + " Non tutti i file includono metadati; prova ad aggiornare o elaborare in batch.",
		),
	),
	ManualSection(
		id="scorciatoie-it",
		title="Scorciatoie",
		bullets=(
			"Ctrl+C / Ctrl+V: Copia / Incolla",
			"Del: Elimina selezionati",
			"F3 / Ctrl+F: Ricerca",
			"Ctrl+S: Salva stato tabella (se disponibile)",
		),
	),
	ManualSection(
		id="buone-pratiche-it",
		title="Buone Pratiche",
		bullets=(
			"Esegui una scansione iniziale su una cartella piccola prima di operazioni grandi.",
			"Salva stati e impostazioni prima di attività batch.",
			"Usa filtri per concentrarti sugli elementi rilevanti.",
		),
	),
	ManualSection(
		id="log-diagnostica-it",
		title="Log e diagnostica",
		bullets=(
			f"I log dell'applicazione possono aiutare a diagnosticare problemi; controlla il file di log generato dall'app qui: {_DATA_DIR}",
		),
	),
	ManualSection(
		id="faq-it",
		title="Domande Frequenti (FAQ)",
		details=(
			ManualDetails(
				summary="Dove vengono salvati i miei dati?",
				paragraphs=(
					f"Attività e file di configurazione sono memorizzati in: {_DATA_DIR}",
					"Controlla quella cartella per trovare file di persistenza e log.",
				),
			),
		),
	),
	ManualSection(
		id="supporto-it",
		title="Come ottenere aiuto e supporto",
		bullets=(
			"Controlla la sezione Informazioni nell'applicazione per informazioni ufficiali e note di rilascio.",
			f"Per problemi complessi, genera i log e inviali al supporto. I file di log si trovano in: {_DATA_DIR}",
			f"Invia i file di log e una descrizione dettagliata del problema all'email di supporto: linceu_lighthouse@outlook.com.",
		),
	),
)
