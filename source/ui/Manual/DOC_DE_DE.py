from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_DE_DE: tuple[ManualSection, ...] = (
    ManualSection(
        id="uebersicht",
        title="Übersicht",
        paragraphs=(
            "Linceu Lighthouse hilft Ihnen, Dateien und Ordner an mehreren Speicherorten Ihres Computers zu prüfen, zu überwachen und zu analysieren."
            " Es zentralisiert Elementinformationen und bietet Werkzeuge zum Filtern, Erstellen von Statistiken und Extrahieren von Metadaten.",
        ),
    ),
    ManualSection(
        id="hauptbildschirm",
        title="Hauptbildschirm — Elemente",
        bullets=(
            to_unicode_bold("Werkzeugleiste:") + " Schnellzugriff auf: Verzeichnis hinzufügen, Scan starten, Stopp, Aktualisieren und Einstellungen.",
            to_unicode_bold("Verzeichniswahl:") + " Bereich zum Hinzufügen, Entfernen oder Wechseln überwachten Ordnern.",
            to_unicode_bold("Elementtabelle:") + " Zentrales Listing mit Spalten (Name, Typ, Größe, Datum, Ereignis) mit Sortier-/Filterunterstützung.",
            to_unicode_bold("Detailbereich:") + " Zeigt Metadaten und Schnellaktionen für das ausgewählte Element an.",
            to_unicode_bold("Meldungen & Fortschritt:") + " Zeigt Benachrichtigungen, Betriebsprotokolle und Fortschrittsbalken an.",
            to_unicode_bold("Statistiken:") + " Bereich für Diagramme und Berichte, die aus gesammelten Daten erzeugt werden.",
        ),
    ),
    ManualSection(
        id="erste-schritte",
        title="Erste Schritte",
        bullets=(
            "Starten Sie die Anwendung über die Verknüpfung oder die ausführbare Datei.",
            "Klicken Sie auf " + to_unicode_bold("Verzeichnis hinzufügen") + " und wählen Sie den zu überwachenden Ordner aus.",
            "Führen Sie einen ersten Scan mit " + to_unicode_bold("Start") + "/" + to_unicode_bold("Scan") + " durch.",
            "Warten Sie; die Elemente werden mit den verfügbaren Metadaten angezeigt.",
            "Aktivieren Sie " + to_unicode_bold("Kontinuierliche Überwachung") + " für automatische Aktualisierungen.",
        ),
    ),
    ManualSection(
        id="betriebsmodi",
        title="Betriebsmodi",
        bullets=(
            to_unicode_bold("Einmaliger Scan:") + " Sofortige Überprüfung des/der ausgewählten Ordners/Ordner.",
            to_unicode_bold("Kontinuierliche Überwachung:") + " Beobachtet Änderungen in Echtzeit und aktualisiert die Tabelle automatisch.",
            to_unicode_bold("Stapelverarbeitung:") + " Extrahiert Metadaten oder führt Aktionen für mehrere Dateien gleichzeitig aus.",
        ),
    ),
    ManualSection(
        id="tabelle-verstehen",
        title="Verstehen der Elementtabelle",
        paragraphs=(
            "Jede Spalte zeigt eine Eigenschaft des Elements. Verwenden Sie Sortierung, Filter und Auswahl, um Elemente effizient zu finden und zu untersuchen.",
        ),
        bullets=(
            to_unicode_bold("Name:") + " Dateiname oder Ordner; Doppelklick öffnet das Element.",
            to_unicode_bold("Typ:") + " Erkannten Typ (Bild, Video, Dokument, Ordner).",
            to_unicode_bold("Größe:") + " In lesbaren Einheiten angezeigt (KB/MB/GB).",
            to_unicode_bold("Datum:") + " Letzte Änderung oder aufgezeichnetes Ereignisdatum.",
            to_unicode_bold("Ereignis:") + " Angezeigte Aktion (erstellt, geändert, verschoben, gelöscht).",
        ),
    ),
    ManualSection(
        id="detailbereich",
        title="Detailbereich & Metadaten",
        paragraphs=(
            "Wenn ein Element ausgewählt ist, zeigt der Seitenbereich relevante Metadaten und Schnellaktionen (Ordner öffnen, Pfad kopieren, Metadaten aktualisieren).",
        ),
        bullets=(
            to_unicode_bold("Vollständiger Pfad:") + " Speicherort der Datei auf der Festplatte.",
            to_unicode_bold("Autor / Ersteller:") + " Falls in den Metadaten vorhanden.",
            to_unicode_bold("Abmessungen:") + " Für Bilder (Breite × Höhe).",
            to_unicode_bold("Dauer:") + " Für Audio/Video.",
            to_unicode_bold("Bitrate:") + " Für Medien, falls verfügbar.",
            to_unicode_bold("Berechtigungen:") + " Zeigt Schutz- oder Schreibbeschränkungen an.",
        ),
    ),
    ManualSection(
        id="datei-aktionen",
        title="Aktionen für Dateien",
        bullets=(
            to_unicode_bold("Öffnen:") + " Öffnen mit der systemweiten Standardanwendung (Doppelklick oder Öffnen-Button).",
            to_unicode_bold("Kopieren / Verschieben:") + " Verwenden Sie Kopieren/Einfügen oder Drag & Drop, um Dateien zwischen Ordnern zu verschieben.",
            to_unicode_bold("Umbenennen / Löschen:") + " Über das Kontextmenü; permanente Aktionen erfordern eine Bestätigung.",
            to_unicode_bold("Wiederherstellen:") + " Falls verfügbar, zuletzt gelöschte Elemente wiederherstellen.",
            to_unicode_bold("Eigenschaften:") + " Vollständige Metadaten und Ereignishistorie der Datei anzeigen.",
        ),
    ),
    ManualSection(
        id="suche-filter",
        title="Suche und Filter",
        bullets=(
            to_unicode_bold("Suche:") + " Verwenden Sie das Suchfeld, um Elemente nach Name oder Begriff zu finden.",
            to_unicode_bold("Filter:") + " Wenden Sie Filter nach Typ, Größe, Datum oder Ereignis an, um Ergebnisse einzugrenzen.",
            to_unicode_bold("Filter kombinieren:") + " Verwenden Sie mehrere Filter zusammen für präzise Ergebnisse.",
        ),
    ),
    ManualSection(
        id="speichern-wiederherstellen",
        title="Speichern und Wiederherstellen der Ansicht",
        bullets=(
            to_unicode_bold("Status speichern:") + " Speichern Sie die aktuelle Spaltenanordnung und Filter als Profil.",
            to_unicode_bold("Wiederherstellen:") + " Laden Sie ein gespeichertes Profil, um Layout und Filter wiederherzustellen.",
        ),
    ),
    ManualSection(
        id="stapelverarbeitung",
        title="Stapelverarbeitung",
        paragraphs=(
            "Wählen Sie mehrere Elemente aus, um Metadaten zu extrahieren oder Batch-Aktionen auszuführen. Fortschritt und Steuerungen sind verfügbar, um anzuhalten oder abzubrechen.",
        ),
        bullets=(
            to_unicode_bold("Extraktion starten:") + " Wählen Sie Elemente und führen Sie die Batch-Metadatenextraktion aus.",
            to_unicode_bold("Fortschritt überwachen:") + " Verfolgen Sie über Fortschrittsbalken und Meldungsbereich.",
            to_unicode_bold("Pause/Abbrechen:") + " Verwenden Sie die Steuerelemente, um die Verarbeitung zu unterbrechen.",
        ),
    ),
    ManualSection(
        id="berichte-statistiken",
        title="Berichte & Statistiken",
        paragraphs=(
            "Der Statistik-Bereich erstellt Diagramme zu Dateitypen, Festplattennutzung und Ereignistrends. Exportieren Sie Bilder oder CSV für die externe Analyse.",
        ),
        bullets=(
            to_unicode_bold("Diagramme erstellen:") + " Wählen Sie Metriken, um Verteilungen und Trends zu visualisieren.",
            to_unicode_bold("Exportieren:") + " Speichern Sie Diagramme als Bilder oder exportieren Sie Daten als CSV.",
        ),
    ),
    ManualSection(
        id="verzeichnisstruktur",
        title="Verzeichnisstruktur",
        bullets=(
            to_unicode_bold("Verzeichnisbaum:") + " Navigieren Sie, um überwachte Ordner auszuwählen und ihren Status zu prüfen.",
            to_unicode_bold("Baum-Aktionen:") + " Erstellen, Umbenennen oder Löschen von Ordnern über das Kontextmenü.",
        ),
    ),
    ManualSection(
        id="ereignis-ueberwachung",
        title="Ereignisüberwachung",
        bullets=(
            to_unicode_bold("Ereignistypen:") + " Erstellung, Änderung, Entfernung und Verschiebung.",
            to_unicode_bold("Echtzeitansicht:") + " Kürzliche Ereignisse werden zur schnellen Überprüfung hervorgehoben.",
            to_unicode_bold("Benachrichtigungen:") + " Konfigurieren Sie visuelle oder akustische Alarme in den Einstellungen.",
        ),
    ),
    ManualSection(
        id="einstellungen-de",
        title="Einstellungen",
        paragraphs=(
            "Passen Sie Sprache, Scan-Verhalten, Benachrichtigungen und Updates an. Überprüfen Sie diese Optionen nach der Installation.",
        ),
        bullets=(
            to_unicode_bold("Sprache:") + " Wählen Sie die UI-Sprache.",
            to_unicode_bold("Scan-Verhalten:") + " Konfigurieren Sie Zeitplan, Tiefe und Ausnahmen.",
            to_unicode_bold("Benachrichtigungen:") + " Aktivieren oder deaktivieren Sie Warnungen.",
            to_unicode_bold("Updates:") + " Wählen Sie automatische oder manuelle Prüfungen.",
        ),
    ),
    ManualSection(
        id="haeufige-probleme-de",
        title="Häufige Probleme und Lösungen",
        bullets=(
            to_unicode_bold("Scan hängt oder Fehler:") + " Warten Sie kurz; wenn es weiterhin besteht, starten Sie den Scan oder die Anwendung neu.",
            to_unicode_bold("Elemente fehlen:") + " Überprüfen Sie, ob der Ordner hinzugefügt wurde und die App Leserechte hat.",
            to_unicode_bold("Kann nicht öffnen:") + " Stellen Sie sicher, dass eine zugeordnete Anwendung für den Dateityp vorhanden ist.",
            to_unicode_bold("Metadaten fehlen:") + " Nicht alle Dateien enthalten Metadaten; versuchen Sie, zu aktualisieren oder per Batch zu verarbeiten.",
        ),
    ),
    ManualSection(
        id="kuerzel-de",
        title="Tastenkürzel",
        bullets=(
            "Strg+C / Strg+V: Kopieren / Einfügen",
            "Entf: Ausgewählte löschen",
            "F3 / Strg+F: Suche fokussieren",
            "Strg+S: Tabellenstatus speichern (falls verfügbar)",
        ),
    ),
    ManualSection(
        id="best-practices-de",
        title="Gute Praxis",
        bullets=(
            "Führen Sie einen ersten Scan in einem kleinen Ordner durch, bevor Sie große Vorgänge starten.",
            "Sichern Sie Zustände und Einstellungen vor Batch-Vorgängen.",
            "Verwenden Sie Filter, um sich auf relevante Elemente zu konzentrieren.",
        ),
    ),
    ManualSection(
        id="logs-diagnostik-de",
        title="Logs und Diagnose",
        bullets=(
            f"Die Anwendungsprotokolle können bei der Diagnose helfen; prüfen Sie die von der Anwendung erzeugte Logdatei hier: {_DATA_DIR}",
        ),
    ),
    ManualSection(
        id="faq-de",
        title="Häufig gestellte Fragen (FAQ)",
        details=(
            ManualDetails(
                summary="Wo werden meine Daten gespeichert?",
                paragraphs=(
                    f"Aufgaben und Konfigurationsdateien werden gespeichert in: {_DATA_DIR}",
                    "Prüfen Sie dieses Verzeichnis, um Persistenzdateien und Logs zu finden.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="support-de",
        title="Wie erhalte ich Hilfe und Support",
        bullets=(
            "Prüfen Sie den Abschnitt 'Über' in der Anwendung für offizielle Informationen und Versionshinweise.",
            f"Für komplexe Probleme erzeugen Sie Logs und senden Sie diese an den Support. Logdateien befinden sich unter: {_DATA_DIR}",
            f"Senden Sie die Logdateien und eine detaillierte Problembeschreibung an die Support-E-Mail: linceu_lighthouse@outlook.com.",
        ),
    ),
)
