from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_ES_ES: tuple[ManualSection, ...] = (
	ManualSection(
		id="vision-general",
		title="Visión General",
		paragraphs=(
			"Linceu Lighthouse le ayuda a inspeccionar, monitorizar y analizar archivos y carpetas en varias ubicaciones de su equipo."
			" Centraliza la información de los elementos y ofrece herramientas para filtrar, generar estadísticas y extraer metadatos.",
		),
	),
	ManualSection(
		id="pantalla-principal",
		title="Pantalla Principal — Elementos",
		bullets=(
			to_unicode_bold("Barra de herramientas:") + " Acceso rápido a: Añadir Directorio, Iniciar Escaneo, Detener, Actualizar y Preferencias.",
			to_unicode_bold("Selector de directorios:") + " Área para añadir, eliminar o cambiar carpetas monitorizadas.",
			to_unicode_bold("Tabla de elementos:") + " Lista central con columnas (Nombre, Tipo, Tamaño, Fecha, Evento) con ordenación/filtrado.",
			to_unicode_bold("Panel de detalles:") + " Muestra metadatos y acciones rápidas para el elemento seleccionado.",
			to_unicode_bold("Mensajes y progreso:") + " Muestra notificaciones, registros de operación y barras de progreso.",
			to_unicode_bold("Estadísticas:") + " Área para gráficos e informes generados a partir de los datos recopilados.",
		),
	),
	ManualSection(
		id="comenzando",
		title="Cómo empezar",
		bullets=(
			"Abra la aplicación desde el acceso directo o ejecutable.",
			"Haga clic en " + to_unicode_bold("Añadir Directorio") + " y elija la carpeta a monitorizar.",
			"Ejecute un escaneo inicial con " + to_unicode_bold("Iniciar") + "/" + to_unicode_bold("Escaneo") + ".",
			"Espere a que finalice; los elementos aparecerán con los metadatos disponibles.",
			"Active " + to_unicode_bold("Monitorización continua") + " para detectar cambios automáticamente.",
		),
	),
	ManualSection(
		id="modos-operacion",
		title="Modos de operación",
		bullets=(
			to_unicode_bold("Escaneo único:") + " Verificación inmediata de la(s) carpeta(s) seleccionada(s).",
			to_unicode_bold("Monitorización continua:") + " Vigilar cambios en tiempo real y actualizar la tabla automáticamente.",
			to_unicode_bold("Procesamiento por lotes:") + " Extraer metadatos o ejecutar acciones en varios archivos a la vez.",
		),
	),
	ManualSection(
		id="tabla-elementos",
		title="Entendiendo la tabla de elementos",
		paragraphs=(
			"Cada columna muestra una propiedad del elemento. Use ordenación, filtros y selección para localizar e inspeccionar elementos eficazmente.",
		),
		bullets=(
			to_unicode_bold("Nombre:") + " Nombre de archivo o carpeta; doble clic para abrir.",
			to_unicode_bold("Tipo:") + " Tipo detectado (imagen, vídeo, documento, carpeta).",
			to_unicode_bold("Tamaño:") + " Mostrado en unidades legibles (KB/MB/GB).",
			to_unicode_bold("Fecha:") + " Fecha de la última modificación o evento registrado.",
			to_unicode_bold("Evento:") + " Acción detectada (creado, modificado, movido, eliminado).",
		),
	),
	ManualSection(
		id="panel-detalles",
		title="Panel de detalles y metadatos",
		paragraphs=(
			"Al seleccionar un elemento, el panel lateral muestra metadatos relevantes y acciones rápidas (abrir carpeta, copiar ruta, actualizar metadatos).",
		),
		bullets=(
			to_unicode_bold("Ruta completa:") + " Ubicación del archivo en disco.",
			to_unicode_bold("Autor / Creador:") + " Cuando esté presente en los metadatos.",
			to_unicode_bold("Dimensiones:") + " Para imágenes (ancho × alto).",
			to_unicode_bold("Duración:") + " Para audio/video.",
			to_unicode_bold("Tasa de bits:") + " Para medios, cuando esté disponible.",
			to_unicode_bold("Permisos:") + " Indica protección o restricciones de escritura.",
		),
	),
	ManualSection(
		id="acciones-archivo",
		title="Acciones sobre archivos",
		bullets=(
			to_unicode_bold("Abrir:") + " Abrir con la aplicación predeterminada del sistema (doble clic o botón Abrir).",
			to_unicode_bold("Copiar / Mover:") + " Use copiar/pegar o arrastrar y soltar para mover archivos entre carpetas.",
			to_unicode_bold("Renombrar / Eliminar:") + " Use el menú contextual; las acciones permanentes requieren confirmación.",
			to_unicode_bold("Restaurar:") + " Cuando esté disponible, recupere eliminaciones recientes mediante la función de restauración.",
			to_unicode_bold("Propiedades:") + " Ver metadatos completos e historial de eventos del archivo.",
		),
	),
	ManualSection(
		id="busqueda-filtros",
		title="Búsqueda y filtros",
		bullets=(
			to_unicode_bold("Buscar:") + " Use la caja de búsqueda para localizar elementos por nombre o término.",
			to_unicode_bold("Filtros:") + " Aplique filtros por tipo, tamaño, fecha o evento para reducir resultados.",
			to_unicode_bold("Combinar filtros:") + " Combine filtros para refinar la selección.",
		),
	),
	ManualSection(
		id="guardar-restaurar",
		title="Guardar y restaurar vista",
		bullets=(
			to_unicode_bold("Guardar estado:") + " Almacene la configuración actual de columnas y filtros como perfil.",
			to_unicode_bold("Restaurar estado:") + " Cargue un perfil guardado para recuperar el diseño y filtros.",
		),
	),
	ManualSection(
		id="procesamiento-lote",
		title="Procesamiento por lotes",
		paragraphs=(
			"Seleccione varios elementos para extraer metadatos o ejecutar acciones en lote. El progreso y los controles permiten pausar o cancelar.",
		),
		bullets=(
			to_unicode_bold("Iniciar extracción:") + " Elija elementos y ejecute la extracción de metadatos por lote.",
			to_unicode_bold("Monitorear progreso:") + " Supervise mediante la barra de progreso y el panel de mensajes.",
			to_unicode_bold("Pausar/Cancelar:") + " Use los controles para interrumpir el procesamiento.",
		),
	),
	ManualSection(
		id="informes-estadisticas",
		title="Informes y estadísticas",
		paragraphs=(
			"La sección de estadísticas produce gráficos sobre tipos de archivos, uso de disco y tendencias de eventos. Exporte imágenes o CSV para uso externo.",
		),
		bullets=(
			to_unicode_bold("Generar gráficos:") + " Seleccione métricas para visualizar distribuciones y tendencias.",
			to_unicode_bold("Exportar:") + " Guarde gráficos como imágenes o exporte datos en CSV.",
		),
	),
	ManualSection(
		id="estructura-directorios",
		title="Estructura de directorios",
		bullets=(
			to_unicode_bold("Árbol de directorios:") + " Navegue para seleccionar carpetas monitorizadas y revisar su estado.",
			to_unicode_bold("Acciones en el árbol:") + " Cree, renombre o elimine carpetas desde el menú contextual.",
		),
	),
	ManualSection(
		id="monitorizacion-eventos",
		title="Monitorización de eventos",
		bullets=(
			to_unicode_bold("Tipos de evento:") + " Creación, modificación, eliminación y movimiento.",
			to_unicode_bold("Vista en tiempo real:") + " Los eventos recientes se resaltan para inspección rápida.",
			to_unicode_bold("Notificaciones:") + " Configure alertas visuales o sonoras en Preferencias.",
		),
	),
	ManualSection(
		id="preferencias",
		title="Preferencias",
		paragraphs=(
			"Ajuste idioma, comportamiento de escaneo, notificaciones y actualizaciones. Revise estas opciones después de la instalación.",
		),
		bullets=(
			to_unicode_bold("Idioma:") + " Elija el idioma de la interfaz.",
			to_unicode_bold("Escaneo:") + " Configure periodicidad, profundidad y exclusiones.",
			to_unicode_bold("Notificaciones:") + " Active o desactive alertas.",
			to_unicode_bold("Actualizaciones:") + " Elija comprobaciones automáticas o manuales.",
		),
	),
	ManualSection(
		id="problemas-comunes",
		title="Problemas comunes y soluciones",
		bullets=(
			to_unicode_bold("Escaneo bloqueado o error:") + " Espere brevemente; si persiste, reinicie el escaneo o la aplicación.",
			to_unicode_bold("Elementos faltantes:") + " Verifique que la carpeta esté añadida y que la aplicación tenga permisos de lectura.",
			to_unicode_bold("No se puede abrir:") + " Asegúrese de que exista una aplicación asociada al tipo de archivo.",
			to_unicode_bold("Metadatos faltantes:") + " No todos los archivos incluyen metadatos; intente actualizar o procesar por lotes.",
		),
	),
	ManualSection(
		id="atajos",
		title="Atajos",
		bullets=(
			"Ctrl+C / Ctrl+V: Copiar / Pegar",
			"Del: Eliminar",
			"F3 / Ctrl+F: Buscar",
			"Ctrl+S: Guardar estado de la tabla (si está disponible)",
		),
	),
	ManualSection(
		id="buenas-practicas",
		title="Buenas prácticas",
		bullets=(
			"Ejecute un escaneo inicial en una carpeta pequeña antes de operaciones grandes.",
			"Guarde estados y configuraciones antes de tareas por lotes.",
			"Use filtros para centrarse en elementos relevantes.",
		),
	),
	ManualSection(
		id="logs-diagnostico",
		title="Registros y diagnóstico",
		bullets=(
			f"Los registros de la aplicación pueden ayudar a diagnosticar problemas; consulte el archivo de registro generado por la aplicación en: {_DATA_DIR}",
		),
	),
	ManualSection(
		id="faq-es",
		title="Preguntas frecuentes (FAQ)",
		details=(
			ManualDetails(
				summary="¿Dónde se guardan mis datos?",
				paragraphs=(
					f"Las tareas y archivos de configuración se almacenan en: {_DATA_DIR}",
					"Consulte ese directorio para localizar archivos de persistencia y registros.",
				),
			),
		),
	),
	ManualSection(
		id="soporte",
		title="Cómo obtener ayuda y soporte",
		bullets=(
			"Consulte la sección Acerca de dentro de la aplicación para información oficial y notas de la versión.",
			f"Para problemas complejos, genere registros y envíelos al soporte. Los archivos de registro están en: {_DATA_DIR}",
			f"Envíe los registros y una descripción detallada del problema al correo de soporte: linceu_lighthouse@outlook.com.",
		),
	),
)
