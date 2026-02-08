from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_EN_US: tuple[ManualSection, ...] = (
	ManualSection(
		id="overview",
		title="Overview",
		paragraphs=(
			"Linceu Lighthouse helps you inspect, monitor and analyze files and folders across multiple locations on your computer."
			" It centralizes item information and provides tools to filter, generate statistics and extract metadata.",
		),
	),
	ManualSection(
		id="main-screen",
		title="Main Screen — Elements",
		bullets=(
			to_unicode_bold("Toolbar:") + " Quick access to Add Directory, Start Scan, Stop, Refresh and Preferences.",
			to_unicode_bold("Directory selector:") + " Area to add, remove or switch monitored folders.",
			to_unicode_bold("Item table:") + " Central list with columns (Name, Type, Size, Date, Event) supporting sort and filter.",
			to_unicode_bold("Details panel:") + " Shows metadata and quick actions for the selected item.",
			to_unicode_bold("Messages & progress:") + " Displays notifications, operation logs and progress bars.",
			to_unicode_bold("Statistics:") + " Area for charts and reports generated from collected data.",
		),
	),
	ManualSection(
		id="getting-started",
		title="Getting Started",
		bullets=(
			"Open the application using the shortcut or executable.",
			"Click " + to_unicode_bold("Add Directory") + " and choose the folder to monitor.",
			"Run an initial scan with " + to_unicode_bold("Start") + "/" + to_unicode_bold("Scan") + ".",
			"Wait for the process to finish; items will appear with available metadata.",
			"Enable " + to_unicode_bold("Continuous monitoring") + " to detect changes automatically.",
		),
	),
	ManualSection(
		id="operation-modes",
		title="Operation Modes",
		bullets=(
			to_unicode_bold("Single Scan:") + " Immediate check of the selected folder(s).",
			to_unicode_bold("Continuous Monitoring:") + " Watch for real-time changes and update the table automatically.",
			to_unicode_bold("Batch Processing:") + " Extract metadata or run actions on multiple files at once.",
		),
	),
	ManualSection(
		id="understanding-table",
		title="Understanding the Item Table",
		paragraphs=(
			"Each column shows a property of the item. Use sorting, filtering and selection to find and inspect items efficiently.",
		),
		bullets=(
			to_unicode_bold("Name:") + " File or folder name; double-click to open.",
			to_unicode_bold("Type:") + " Detected type (image, video, document, folder).",
			to_unicode_bold("Size:") + " Shown in human-readable units (KB/MB/GB).",
			to_unicode_bold("Date:") + " Last modification or recorded event date.",
			to_unicode_bold("Event:") + " Detected action (created, modified, moved, deleted).",
		),
	),
	ManualSection(
		id="details-panel",
		title="Details Panel & Metadata",
		paragraphs=(
			"Selecting an item displays relevant metadata and quick actions (open folder, copy path, refresh metadata).",
		),
		bullets=(
			to_unicode_bold("Full path:") + " File location on disk.",
			to_unicode_bold("Author / Creator:") + " When present in metadata.",
			to_unicode_bold("Dimensions:") + " For images (width × height).",
			to_unicode_bold("Duration:") + " For audio/video files.",
			to_unicode_bold("Bitrate:") + " For media files, if available.",
			to_unicode_bold("Permissions:") + " Indicates protection or write restrictions.",
		),
	),
	ManualSection(
		id="file-actions",
		title="File Actions",
		bullets=(
			to_unicode_bold("Open:") + " Open with the system default app (double-click or Open button).",
			to_unicode_bold("Copy / Move:") + " Use copy/paste or drag-and-drop to move files between folders.",
			to_unicode_bold("Rename / Delete:") + " Use the context menu; permanent actions require confirmation.",
			to_unicode_bold("Restore:") + " When available, recover recent deletions using restore functionality.",
			to_unicode_bold("Properties:") + " View full metadata and event history for the file.",
		),
	),
	ManualSection(
		id="search-filters",
		title="Search and Filters",
		bullets=(
			to_unicode_bold("Search:") + " Enter terms in the search box to find items by name or content.",
			to_unicode_bold("Filters:") + " Apply filters by type, size, date or event to narrow results.",
			to_unicode_bold("Combine filters:") + " Use multiple filters together for precise results.",
		),
	),
	ManualSection(
		id="save-restore",
		title="Saving and Restoring Views",
		bullets=(
			to_unicode_bold("Save state:") + " Store current column layout and filters as a profile.",
			to_unicode_bold("Restore state:") + " Load a saved profile to recover layout and filters.",
		),
	),
	ManualSection(
		id="batch-processing",
		title="Batch Processing",
		paragraphs=(
			"Select multiple items to extract metadata or perform batch actions. Progress and controls are available to pause or cancel.",
		),
		bullets=(
			to_unicode_bold("Start extraction:") + " Choose items and run batch metadata extraction.",
			to_unicode_bold("Monitor progress:") + " Track via the progress bar and messages panel.",
			to_unicode_bold("Pause/Cancel:") + " Use the provided controls to interrupt processing.",
		),
	),
	ManualSection(
		id="reports-statistics",
		title="Reports & Statistics",
		paragraphs=(
			"The statistics section produces charts for file types, disk usage and event trends. Export images or CSV for external use.",
		),
		bullets=(
			to_unicode_bold("Generate charts:") + " Select metrics to visualize distributions and trends.",
			to_unicode_bold("Export:") + " Save charts as images or export data as CSV.",
		),
	),
	ManualSection(
		id="directory-structure",
		title="Directory Structure",
		bullets=(
			to_unicode_bold("Directory tree:") + " Navigate folders to select monitored locations and review status.",
			to_unicode_bold("Tree actions:") + " Create, rename or delete folders from the context menu.",
		),
	),
	ManualSection(
		id="event-monitoring",
		title="Event Monitoring",
		bullets=(
			to_unicode_bold("Event types:") + " Creation, modification, removal and movement.",
			to_unicode_bold("Real-time view:") + " Recent events are highlighted for quick inspection.",
			to_unicode_bold("Notifications:") + " Configure visual or sound alerts in Preferences.",
		),
	),
	ManualSection(
		id="preferences",
		title="Preferences",
		paragraphs=(
			"Adjust language, scan behavior, notifications and update preferences. Review these settings after installation.",
		),
		bullets=(
			to_unicode_bold("Language:") + " Choose the UI language.",
			to_unicode_bold("Scan behavior:") + " Configure schedule, depth and exclusions.",
			to_unicode_bold("Notifications:") + " Enable or disable alerts.",
			to_unicode_bold("Updates:") + " Choose automatic or manual checks.",
		),
	),
	ManualSection(
		id="common-issues",
		title="Common Issues & Fixes",
		bullets=(
			to_unicode_bold("Scan stuck or error:") + " Wait briefly; if it persists, restart the scan or the application.",
			to_unicode_bold("Items missing:") + " Verify the folder is added and the app has read permission.",
			to_unicode_bold("Unable to open file:") + " Ensure an associated application exists for the file type.",
			to_unicode_bold("Missing metadata:") + " Not all files include metadata; try refreshing or batch processing.",
		),
	),
	ManualSection(
		id="shortcuts",
		title="Shortcuts",
		bullets=(
			"Ctrl+C / Ctrl+V: Copy / Paste",
			"Del: Delete selected",
			"F3 / Ctrl+F: Focus search",
			"Ctrl+S: Save table state (if available)",
		),
	),
	ManualSection(
		id="best-practices",
		title="Best Practices",
		bullets=(
			"Run an initial scan on a small folder before large operations.",
			"Save states and settings before batch tasks.",
			"Use filters to focus on relevant items.",
		),
	),
	ManualSection(
		id="logs-and-diagnostics",
		title="Logs & diagnostics",
		bullets=(
			f"The application logs can help diagnose issues; check the log file generated by the app at: {_DATA_DIR}",
		),
	),
	ManualSection(
		id="faq",
		title="Frequently Asked Questions",
		details=(
			ManualDetails(
				summary="Where are my data saved?",
				paragraphs=(
					f"Tasks and configuration files are stored in: {_DATA_DIR}",
					"Check that directory to find persistence files and logs.",
				),
			),
		),
	),
	ManualSection(
		id="support",
		title="How to get help and support",
		bullets=(
			"Check the About section inside the application for official information and release notes.",
			f"For complex issues, generate logs and send them to support. Log files are located at: {_DATA_DIR}",
			"Send the log files and a detailed description of the issue to the support email: linceu_lighthouse@outlook.com.",
		),
	),
)
