
# 📦 RELEASE NOTES

<p align="center">
  <b>Selecione o idioma / Select language / Selecciona idioma / Sélectionnez la langue / Seleziona la lingua / Sprache auswählen:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> •
  <a href="#enus">🇺🇸 English (US)</a> •
  <a href="#eses">🇪🇸 Español (ES)</a> •
  <a href="#frfr">🇫� Français (FR)</a> •
  <a href="#itit">🇮🇹 Italiano (IT)</a> •
  <a href="#dede">🇩🇪 Deutsch (DE)</a>
</p>

---

## 🇧🇷 Português (BR)

<details>
<summary>Clique para expandir as notas de versão em Português</summary>

**Versão 0.0.6.0**

Nesta nova versão, foram implementadas as seguintes melhorias e funcionalidades:

- Novo Diagrama — Gráfico de Fluxo (Sankey):
  - Adicionado um gráfico de fluxo (Sankey) para análise dos dados monitorados, permitindo visualizar conexões e fluxos entre categorias/metadados.
  - A interface é interativa: o usuário pode explorar nós e links do diagrama para detalhar origem, destino e magnitude dos fluxos.
  - Visualização complementar com gráfico de barras para comparação clara da distribuição dos dados.

---

**Versão 0.0.5.0**

Aprimoramento da Experiência do Usuário:
- Pausa de Estágios do Monitoramento:
  - Agora é possível pausar qualquer estágio do monitoramento.
  - Durante a pausa, a coleta de dados é temporariamente interrompida, permitindo ajustes sem processar novos eventos.
  - A funcionalidade pode ser ativada/desativada a qualquer momento, oferecendo maior controle operacional.

---

**Versão 0.0.4.0**

Correções de Bugs:
- Correção no comando de iniciar/parar análise:
  - Resolvido erro ao parar durante o escaneamento inicial, evitando falhas inesperadas.
- Seletor de Cores Avançado:
  - Corrigido o problema que impedia a abertura da janela de diálogo do seletor de cores nas configurações.

---

**Versão 0.0.3.0**

Robustez e Estabilidade:
- Verificações de existência adicionadas antes de acessar métodos e propriedades.
- O método _invalidar_cache_cores_ é chamado somente se presente.
- Remoção do atributo indefinido _cor_selecao_future_.

Otimizações de Interface e Processos:
- Controle de retradução otimizado ao trocar idioma.
- Refatoração dos métodos de atualização de cabeçalhos, dados e visibilidade de colunas.
- Ajustes no gerenciamento de índices de colunas e integração entre atualizações.

Correções e Melhorias Gerais:
- Diversos ajustes em métodos de processamento para maior estabilidade e desempenho.

---

**Versão 0.0.2.0**

Refatoração do Sistema de Internacionalização:
- Sistema de idiomas reescrito usando recursos nativos do Qt/PySide6, com ganho de responsividade.
- Recomenda-se definir o idioma antes de iniciar o monitoramento; trocar idioma durante monitoramento ativo pode causar travamentos.

Melhorias de UI/UX:
- Janela de aviso bilíngue ao trocar idioma.
- Janelas secundárias não-modais.
- Menus redesenhados para melhor organização dos metadados.
- Calendário do filtro de datas agora é internacionalizado.

Análise de Dados e Monitoramento:
- Expansão das colunas de tamanho em 15 novas colunas para maior granularidade.
- Módulo de análise estatística reformulado para suportar novas colunas.
- Aprimorada identificação de tipos de arquivo por extensão.

</details>

---

## 🇺🇸 English (US)

<details>
<summary>Click to expand release notes in English</summary>

**Version 0.0.6.0**

New in this release:

- Sankey Flow Diagram:
  - Added a Sankey flow chart to analyze monitored data, visualizing connections and flow magnitudes between categories/metadata.
  - Interactive interface allows users to explore nodes and links for origin, destination and magnitude details.
  - Complementary bar chart view for clear distribution comparison.

---

**Version 0.0.5.0**

User Experience Improvements:
- Monitoring Stage Pause:
  - You can now pause any monitoring stage.
  - While paused, data collection is temporarily stopped so the user can make adjustments without new events being processed.
  - Pause can be toggled at any time for finer control.

---

**Version 0.0.4.0**

Bug Fixes:
- Start/Stop Analysis Command:
  - Fixed issue occurring when stopping during the initial scan; application now handles this without unexpected crashes.
- Advanced Color Picker:
  - Fixed problem that prevented the advanced color picker dialog from opening.

---

**Version 0.0.3.0**

Stability & Robustness:
- Added existence checks before accessing object methods/properties.
- _invalidar_cache_cores_ now called only if present.
- Removed undefined attribute _cor_selecao_future_.

Interface & Process Optimizations:
- Optimized retranslation control when changing language.
- Refactored header, data and column visibility update methods.
- Fixed column index management and improved integration of updates.

General Fixes:
- Multiple processing method adjustments for better stability and performance.

---

**Version 0.0.2.0**

Internationalization Refactor:
- Complete rewrite of translation system using native Qt/PySide6 resources for better responsiveness.
- Important: set language before starting monitoring; avoid changing language during an active monitoring session.

UI/UX Improvements:
- Bilingual confirmation dialog for language switch.
- Secondary windows are non-modal.
- Redesigned menus and translated date-picker calendar.

Data Analysis & Monitoring:
- Expanded size-related columns into 15 new columns for finer filters.
- Statistical analysis module updated to support new metadata columns.
- Improved file-type detection by extension.

</details>

---

## 🇪🇸 Español (ES)

<details>
<summary>Haz clic para expandir las notas de la versión en Español</summary>

**Versión 0.0.6.0**

Novedades en esta versión:

- Diagrama de Flujo Sankey:
  - Se agregó un diagrama de flujo (Sankey) para analizar los datos monitoreados, visualizando conexiones y magnitudes de flujo entre categorías/metadatos.
  - La interfaz es interactiva: los usuarios pueden explorar nodos y enlaces para ver origen, destino y magnitud.
  - Vista complementaria con gráfico de barras para comparar la distribución de los datos.

---

**Versión 0.0.5.0**

Mejoras en la Experiencia de Usuario:
- Pausa en Etapas de Monitoreo:
  - Ahora se puede pausar cualquier etapa del monitoreo.
  - Mientras está en pausa, la recolección de datos se detiene temporalmente para permitir ajustes sin procesar nuevos eventos.
  - La pausa puede activarse/desactivarse en cualquier momento para un control más preciso.

---

**Versión 0.0.4.0**

Correcciones de Errores:
- Comando Iniciar/Detener Análisis:
  - Corregido el problema que ocurría al detener durante el escaneo inicial; la aplicación ahora maneja esto sin cierres inesperados.
- Selector de Color Avanzado:
  - Corregido el problema que impedía abrir el diálogo del selector de color en la configuración.

---

**Versión 0.0.3.0**

Estabilidad y Robustez:
- Añadidas comprobaciones de existencia antes de acceder a métodos/propiedades de objetos.
- _invalidar_cache_cores_ ahora se llama solo si está presente.
- Eliminado el atributo indefinido _cor_selecao_future_.

Optimización de Interfaz y Procesos:
- Control de retraducción optimizado al cambiar de idioma.
- Refactorización de los métodos de actualización de cabeceras, datos y visibilidad de columnas.
- Ajustes en la gestión de índices de columnas e integración de actualizaciones.

Correcciones Generales:
- Varios ajustes en métodos de procesamiento para mayor estabilidad y rendimiento.

---

**Versión 0.0.2.0**

Refactorización de Internacionalización:
- Reescritura completa del sistema de traducción usando recursos nativos de Qt/PySide6 para mayor respuesta.
- Importante: configure el idioma antes de iniciar el monitoreo; evite cambiar el idioma durante una sesión de monitoreo activa.

Mejoras de UI/UX:
- Diálogo bilingüe de confirmación al cambiar idioma.
- Ventanas secundarias no modales.
- Menús rediseñados y calendario del selector de fechas traducido.

Análisis de Datos y Monitoreo:
- Columnas relacionadas con tamaños ampliadas a 15 nuevas columnas para filtros más finos.
- Módulo de análisis estadístico actualizado para soportar las nuevas columnas de metadatos.
- Mejora en la detección de tipos de archivo por extensión.

</details>

---

## 🇫🇷 Français (FR)

<details>
<summary>Cliquez pour afficher les notes de version en Français</summary>

**Version 0.0.6.0**

Nouveautés dans cette version :

- Diagramme de flux Sankey :
  - Ajout d'un diagramme de flux (Sankey) pour analyser les données surveillées, visualisant les connexions et l'amplitude des flux entre catégories/métadonnées.
  - L'interface est interactive : l'utilisateur peut explorer les nœuds et les liens pour obtenir des détails sur l'origine, la destination et l'amplitude.
  - Vue complémentaire en histogramme (barres) pour comparer clairement la distribution des données.

---

**Version 0.0.5.0**

Améliorations de l'expérience utilisateur :
- Pause des étapes de surveillance :
  - Il est désormais possible de mettre en pause n'importe quelle étape de la surveillance.
  - Pendant la pause, la collecte de données est temporairement arrêtée, permettant d'effectuer des ajustements sans traiter de nouveaux événements.
  - La fonction de pause peut être activée ou désactivée à tout moment pour un meilleur contrôle.

---

**Version 0.0.4.0**

Corrections de bugs :
- Commande Démarrer/Arrêter l'analyse :
  - Correction du problème survenant lors de l'arrêt pendant l'analyse initiale ; l'application gère désormais cela sans plantages inattendus.
- Sélecteur de couleurs avancé :
  - Correction du problème empêchant l'ouverture de la boîte de dialogue du sélecteur de couleurs dans les paramètres.

---

**Version 0.0.3.0**

Robustesse et stabilité :
- Ajout de vérifications d'existence avant d'accéder aux méthodes/propriétés des objets.
- _invalidar_cache_cores_ appelé uniquement s'il est présent.
- Suppression de l'attribut indéfini _cor_selecao_future_.

Optimisations de l'interface et des processus :
- Contrôle de la retraduction optimisé lors du changement de langue.
- Refactorisation des méthodes de mise à jour des en-têtes, des données et de la visibilité des colonnes.
- Ajustements de la gestion des indices de colonnes et intégration des mises à jour.

Corrections générales :
- Divers ajustements des méthodes de traitement pour une meilleure stabilité et performance.

---

**Version 0.0.2.0**

Refonte de l'internationalisation :
- Réécriture complète du système de traduction en utilisant les ressources natives de Qt/PySide6 pour une meilleure réactivité.
- Important : définissez la langue avant de démarrer la surveillance ; évitez de changer la langue pendant une session de surveillance active.

Améliorations UI/UX :
- Boîte de dialogue bilingue de confirmation pour le changement de langue.
- Fenêtres secondaires non modales.
- Menus repensés et calendrier du sélecteur de date traduit.

Analyse des données et surveillance :
- Colonnes liées à la taille étendues en 15 nouvelles colonnes pour des filtres plus fins.
- Module d'analyse statistique mis à jour pour prendre en charge les nouvelles colonnes de métadonnées.
- Amélioration de la détection des types de fichiers par extension.

</details>

---

## 🇮🇹 Italiano (IT)

<details>
<summary>Espandi le note di rilascio in Italiano</summary>

**Versione 0.0.6.0**

Novità in questa release:

- Diagramma di flusso Sankey:
  - Aggiunto un diagramma Sankey per analizzare i dati monitorati, visualizzando connessioni e magnitudini di flusso tra categorie/metadati.
  - L'interfaccia è interattiva: l'utente può esplorare nodi e collegamenti per dettagli su origine, destinazione e magnitudo.
  - Vista complementare con grafico a barre per un confronto chiaro delle distribuzioni.

---

**Versione 0.0.5.0**

Miglioramenti dell'esperienza utente:
- Pausa delle fasi di monitoraggio:
  - Ora è possibile mettere in pausa qualsiasi fase del monitoraggio.
  - Durante la pausa, la raccolta dei dati viene temporaneamente interrotta per consentire regolazioni senza elaborare nuovi eventi.
  - La funzione di pausa può essere attivata/disattivata in qualsiasi momento per un controllo più preciso.

---

**Versione 0.0.4.0**

Correzioni di bug:
- Comando Avvia/Arresta Analisi:
  - Risolto il problema che si verificava quando si interrompeva durante la scansione iniziale; l'applicazione ora gestisce questa situazione senza arresti imprevisti.
- Selettore Colori Avanzato:
  - Risolto il problema che impediva l'apertura della finestra di dialogo del selettore colori nelle impostazioni.

---

**Versione 0.0.3.0**

Robustezza e stabilità:
- Aggiunte verifiche di esistenza prima di accedere a metodi/proprietà degli oggetti.
- _invalidar_cache_cores_ chiamato solo se presente.
- Rimosso l'attributo non definito _cor_selecao_future_.

Ottimizzazioni di interfaccia e processi:
- Controllo della retraduzione ottimizzato durante il cambio lingua.
- Refactoring dei metodi di aggiornamento di intestazioni, dati e visibilità delle colonne.
- Regolazioni nella gestione degli indici delle colonne e integrazione degli aggiornamenti.

Correzioni generali:
- Vari aggiustamenti nei metodi di elaborazione per una maggiore stabilità e prestazioni.

---

**Versione 0.0.2.0**

Refactor dell'internazionalizzazione:
- Riscrittura completa del sistema di traduzione utilizzando le risorse native di Qt/PySide6 per una maggiore reattività.
- Importante: impostare la lingua prima di avviare il monitoraggio; evitare di cambiare lingua durante una sessione di monitoraggio attiva.

Miglioramenti UI/UX:
- Dialogo bilingue di conferma per il cambio lingua.
- Finestre secondarie non modali.
- Menu ridisegnati e calendario del selettore date tradotto.

Analisi dei dati e monitoraggio:
- Colonne relative alle dimensioni ampliate in 15 nuove colonne per filtri più dettagliati.
- Modulo di analisi statistica aggiornato per supportare le nuove colonne di metadati.
- Migliorata la rilevazione dei tipi di file per estensione.

</details>

---

## 🇩🇪 Deutsch (DE)

<details>
<summary>Erweiterte Versionshinweise auf Deutsch anzeigen</summary>

**Version 0.0.6.0**

Neu in dieser Version:

- Sankey-Flussdiagramm:
  - Hinzugefügt: ein Sankey-Flussdiagramm zur Analyse der überwachten Daten, das Verbindungen und Flussstärken zwischen Kategorien/Metadaten visualisiert.
  - Interaktive Oberfläche ermöglicht es Benutzern, Knoten und Verbindungen zu erkunden, um Herkunft, Ziel und Stärke der Flüsse zu sehen.
  - Ergänzende Balkendiagramm-Ansicht für einen klaren Vergleich der Verteilung.

---

**Version 0.0.5.0**

Verbesserungen der Benutzererfahrung:
- Pausieren von Überwachungsphasen:
  - Sie können jetzt jede Phase der Überwachung pausieren.
  - Während der Pause wird die Datensammlung vorübergehend gestoppt, damit der Benutzer Anpassungen vornehmen kann, ohne neue Ereignisse zu verarbeiten.
  - Die Pause kann jederzeit ein- oder ausgeschaltet werden, um feinere Steuerung zu ermöglichen.

---

**Version 0.0.4.0**

Fehlerbehebungen:
- Start/Stopp-Analyse-Befehl:
  - Problem behoben, das beim Stoppen während des ersten Scanvorgangs auftrat; die Anwendung behandelt dies jetzt ohne unerwartete Abstürze.
- Erweiterter Farbwähler:
  - Problem behoben, das das Öffnen des Dialogs des erweiterten Farbwählers in den Einstellungen verhinderte.

---

**Version 0.0.3.0**

Stabilität & Robustheit:
- Vor dem Zugriff auf Methoden/Eigenschaften von Objekten wurden Existenzprüfungen hinzugefügt.
- _invalidar_cache_cores_ wird jetzt nur noch aufgerufen, wenn es vorhanden ist.
- Entferntes undefiniertes Attribut _cor_selecao_future_.

Optimierungen von Oberfläche und Prozessen:
- Optimierte Neuzuordnungssteuerung beim Sprachwechsel.
- Refactoring von Methoden zur Aktualisierung von Kopfzeilen, Daten und Spaltensichtbarkeit.
- Anpassungen im Management der Spaltenindizes und verbesserte Integration von Aktualisierungen.

Allgemeine Fehlerbehebungen:
- Mehrere Anpassungen in Verarbeitungmethoden für bessere Stabilität und Leistung.

---

**Version 0.0.2.0**

Refaktorierung der Internationalisierung:
- Vollständige Neuschreibung des Übersetzungssystems unter Verwendung nativer Qt/PySide6-Ressourcen für bessere Reaktionsfähigkeit.
- Wichtig: Stellen Sie die Sprache ein, bevor Sie die Überwachung starten; vermeiden Sie das Ändern der Sprache während einer aktiven Überwachungssitzung.

UI/UX Verbesserungen:
- Zweisprachiges Bestätigungsdialog beim Sprachwechsel.
- Sekundäre Fenster sind nicht modal.
- Überarbeitete Menüs und übersetzter Datumswähler-Kalender.

Datenanalyse & Überwachung:
- Größenbezogene Spalten wurden in 15 neue Spalten erweitert, für feinere Filter.
- Statistikanalyse-Modul aktualisiert, um neue Metadatenspalten zu unterstützen.
- Verbesserte Dateityp-Erkennung nach Erweiterung.

</details>
