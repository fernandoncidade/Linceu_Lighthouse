from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_FR_FR: tuple[ManualSection, ...] = (
	ManualSection(
		id="vue-generale",
		title="Vue d'ensemble",
		paragraphs=(
			"Linceu Lighthouse vous aide à inspecter, surveiller et analyser des fichiers et dossiers à travers plusieurs emplacements de votre ordinateur."
			" Il centralise les informations des éléments et fournit des outils pour filtrer, générer des statistiques et extraire les métadonnées.",
		),
	),
	ManualSection(
		id="ecran-principal",
		title="Écran principal — Éléments",
		bullets=(
			to_unicode_bold("Barre d'outils:") + " Accès rapide à : Ajouter un répertoire, Démarrer l'analyse, Arrêter, Actualiser et Préférences.",
			to_unicode_bold("Sélecteur de répertoires:") + " Zone pour ajouter, supprimer ou basculer les dossiers surveillés.",
			to_unicode_bold("Table des éléments:") + " Liste centrale avec colonnes (Nom, Type, Taille, Date, Événement) supportant tri et filtre.",
			to_unicode_bold("Panneau de détails:") + " Affiche les métadonnées et actions rapides pour l'élément sélectionné.",
			to_unicode_bold("Messages & progression:") + " Affiche notifications, journaux d'opération et barres de progression.",
			to_unicode_bold("Statistiques:") + " Zone pour graphiques et rapports générés à partir des données collectées.",
		),
	),
	ManualSection(
		id="demarrage",
		title="Commencer",
		bullets=(
			"Ouvrez l'application via le raccourci ou l'exécutable.",
			"Cliquez sur " + to_unicode_bold("Ajouter un répertoire") + " et choisissez le dossier à surveiller.",
			"Lancez une analyse initiale avec " + to_unicode_bold("Démarrer") + "/" + to_unicode_bold("Analyser") + ".",
			"Patientez ; les éléments apparaîtront avec les métadonnées disponibles.",
			"Activez " + to_unicode_bold("Surveillance continue") + " pour détecter les changements automatiquement.",
		),
	),
	ManualSection(
		id="modes-fonctionnement",
		title="Modes de fonctionnement",
		bullets=(
			to_unicode_bold("Analyse unique:") + " Vérification immédiate du/des dossier(s) sélectionné(s).",
			to_unicode_bold("Surveillance continue:") + " Surveillance des changements en temps réel et mise à jour automatique de la table.",
			to_unicode_bold("Traitement par lots:") + " Extraction de métadonnées ou exécution d'actions sur plusieurs fichiers simultanément.",
		),
	),
	ManualSection(
		id="comprendre-table",
		title="Comprendre la table des éléments",
		paragraphs=(
			"Chaque colonne représente une propriété de l'élément. Utilisez le tri, les filtres et la sélection pour trouver et inspecter efficacement les éléments.",
		),
		bullets=(
			to_unicode_bold("Nom:") + " Nom du fichier ou dossier ; double-clic pour ouvrir.",
			to_unicode_bold("Type:") + " Type détecté (image, vidéo, document, dossier).",
			to_unicode_bold("Taille:") + " Affiché en unités lisibles (KB/MB/GB).",
			to_unicode_bold("Date:") + " Date de la dernière modification ou de l'événement enregistré.",
			to_unicode_bold("Événement:") + " Action détectée (créé, modifié, déplacé, supprimé).",
		),
	),
	ManualSection(
		id="panneau-details",
		title="Panneau de détails et métadonnées",
		paragraphs=(
			"La sélection d'un élément affiche les métadonnées pertinentes et des actions rapides (ouvrir dossier, copier le chemin, actualiser les métadonnées).",
		),
		bullets=(
			to_unicode_bold("Chemin complet:") + " Emplacement du fichier sur le disque.",
			to_unicode_bold("Auteur / Créateur:") + " Si présent dans les métadonnées.",
			to_unicode_bold("Dimensions:") + " Pour les images (largeur × hauteur).",
			to_unicode_bold("Durée:") + " Pour les fichiers audio/vidéo.",
			to_unicode_bold("Débit:") + " Pour les médias, si disponible.",
			to_unicode_bold("Permissions:") + " Indique la protection ou les restrictions d'écriture.",
		),
	),
	ManualSection(
		id="actions-fichiers",
		title="Actions sur les fichiers",
		bullets=(
			to_unicode_bold("Ouvrir:") + " Ouvrir avec l'application par défaut du système (double-clic ou bouton Ouvrir).",
			to_unicode_bold("Copier / Déplacer:") + " Utilisez copier/coller ou glisser-déposer pour déplacer des fichiers entre dossiers.",
			to_unicode_bold("Renommer / Supprimer:") + " Utilisez le menu contextuel ; les actions permanentes nécessitent une confirmation.",
			to_unicode_bold("Restaurer:") + " Lorsque disponible, récupérer les suppressions récentes via la fonction de restauration.",
			to_unicode_bold("Propriétés:") + " Voir les métadonnées complètes et l'historique des événements du fichier.",
		),
	),
	ManualSection(
		id="recherche-filtres",
		title="Recherche et filtres",
		bullets=(
			to_unicode_bold("Recherche:") + " Utilisez la zone de recherche pour trouver des éléments par nom ou terme.",
			to_unicode_bold("Filtres:") + " Appliquez des filtres par type, taille, date ou événement pour affiner les résultats.",
			to_unicode_bold("Combiner les filtres:") + " Combinez plusieurs filtres pour des résultats précis.",
		),
	),
	ManualSection(
		id="sauvegarder-restaurer",
		title="Sauvegarder et restaurer la vue",
		bullets=(
			to_unicode_bold("Sauvegarder l'état:") + " Enregistrez la disposition actuelle des colonnes et les filtres comme profil.",
			to_unicode_bold("Restaurer l'état:") + " Chargez un profil enregistré pour retrouver la disposition et les filtres.",
		),
	),
	ManualSection(
		id="traitement-lots",
		title="Traitement par lots",
		paragraphs=(
			"Sélectionnez plusieurs éléments pour extraire des métadonnées ou effectuer des actions par lots. La progression et les contrôles permettent de mettre en pause ou d'annuler.",
		),
		bullets=(
			to_unicode_bold("Démarrer l'extraction:") + " Choisissez des éléments et lancez l'extraction des métadonnées par lot.",
			to_unicode_bold("Surveiller la progression:") + " Suivez via la barre de progression et le panneau de messages.",
			to_unicode_bold("Pause/Annuler:") + " Utilisez les contrôles pour interrompre le traitement.",
		),
	),
	ManualSection(
		id="rapports-statistiques",
		title="Rapports et statistiques",
		paragraphs=(
			"La section statistiques produit des graphiques sur les types de fichiers, l'utilisation du disque et les tendances d'événements. Exportez images ou CSV pour une analyse externe.",
		),
		bullets=(
			to_unicode_bold("Générer des graphiques:") + " Sélectionnez des métriques pour visualiser des distributions et tendances.",
			to_unicode_bold("Exporter:") + " Enregistrez les graphiques en images ou exportez les données en CSV.",
		),
	),
	ManualSection(
		id="structure-repertoires",
		title="Structure des répertoires",
		bullets=(
			to_unicode_bold("Arbre des répertoires:") + " Naviguez pour sélectionner les dossiers surveillés et vérifier leur statut.",
			to_unicode_bold("Actions sur l'arbre:") + " Créez, renommez ou supprimez des dossiers via le menu contextuel.",
		),
	),
	ManualSection(
		id="monitorage-evenements",
		title="Surveillance des événements",
		bullets=(
			to_unicode_bold("Types d'événements:") + " Création, modification, suppression et déplacement.",
			to_unicode_bold("Vue temps réel:") + " Les événements récents sont mis en évidence pour une inspection rapide.",
			to_unicode_bold("Notifications:") + " Configurez des alertes visuelles ou sonores dans Préférences.",
		),
	),
	ManualSection(
		id="preferences-fr",
		title="Préférences",
		paragraphs=(
			"Ajustez la langue, le comportement d'analyse, les notifications et les mises à jour. Vérifiez ces options après l'installation.",
		),
		bullets=(
			to_unicode_bold("Langue:") + " Choisissez la langue de l'interface.",
			to_unicode_bold("Analyse:") + " Configurez la fréquence, la profondeur et les exclusions.",
			to_unicode_bold("Notifications:") + " Activez ou désactivez les alertes.",
			to_unicode_bold("Mises à jour:") + " Choisissez vérification automatique ou manuelle.",
		),
	),
	ManualSection(
		id="problemes-communs-fr",
		title="Problèmes courants et solutions",
		bullets=(
			to_unicode_bold("Analyse bloquée ou erreur:") + " Patientez ; si cela persiste, redémarrez l'analyse ou l'application.",
			to_unicode_bold("Éléments manquants:") + " Vérifiez que le dossier a été ajouté et que l'application dispose des droits de lecture.",
			to_unicode_bold("Impossible d'ouvrir:") + " Assurez-vous qu'une application est associée au type de fichier.",
			to_unicode_bold("Métadonnées manquantes:") + " Tous les fichiers n'incluent pas de métadonnées ; essayez d'actualiser ou de traiter par lots.",
		),
	),
	ManualSection(
		id="raccourcis-fr",
		title="Raccourcis",
		bullets=(
			"Ctrl+C / Ctrl+V: Copier / Coller",
			"Del: Supprimer",
			"F3 / Ctrl+F: Rechercher",
			"Ctrl+S: Sauvegarder l'état de la table (si disponible)",
		),
	),
	ManualSection(
		id="bonnes-pratiques-fr",
		title="Bonnes pratiques",
		bullets=(
			"Effectuez une première analyse sur un petit dossier avant les opérations volumineuses.",
			"Sauvegardez états et configurations avant les traitements par lots.",
			"Utilisez des filtres pour vous concentrer sur les éléments pertinents.",
		),
	),
	ManualSection(
		id="logs-diagnostic-fr",
		title="Journaux et diagnostic",
		bullets=(
			f"Les journaux de l'application peuvent aider à diagnostiquer les problèmes ; consultez le fichier journal généré par l'application ici : {_DATA_DIR}",
		),
	),
	ManualSection(
		id="faq-fr",
		title="Questions fréquentes (FAQ)",
		details=(
			ManualDetails(
				summary="Où mes données sont-elles enregistrées ?",
				paragraphs=(
					f"Les tâches et fichiers de configuration sont stockés dans : {_DATA_DIR}",
					"Consultez ce répertoire pour trouver les fichiers de persistance et les journaux.",
				),
			),
		),
	),
	ManualSection(
		id="support-fr",
		title="Comment obtenir de l'aide et du support",
		bullets=(
			"Consultez la section À propos dans l'application pour les informations officielles et les notes de version.",
			f"Pour les problèmes complexes, générez des journaux et envoyez-les au support. Les fichiers journaux se trouvent ici : {_DATA_DIR}",
			f"Envoyez les journaux et une description détaillée du problème à l'email de support : linceu_lighthouse@outlook.com.",
		),
	),
)
