from source.ui.Manual.common_Manual import ManualSection, ManualDetails, to_unicode_bold, _DATA_DIR

_DOC_PT_BR: tuple[ManualSection, ...] = (
	ManualSection(
		id="visao-geral",
		title="Visão Geral",
		paragraphs=(
			"Linceu Lighthouse permite inspecionar, monitorar e analisar arquivos e pastas em múltiplas localizações do seu computador."
			" Apresenta uma lista central com informações e ações para organizar, filtrar, gerar estatísticas e extrair metadados.",
		),
	),
	ManualSection(
		id="tela-principal",
		title="Tela Principal — Elementos",
		bullets=(
			to_unicode_bold("Barra de ferramentas:") + " Acesso rápido a: Adicionar Diretório, Iniciar Scan, Parar, Atualizar e Preferências.",
			to_unicode_bold("Seleção de diretórios:") + " Área para adicionar, remover ou alternar pastas monitoradas.",
			to_unicode_bold("Tabela de itens:") + " Lista central com colunas (Nome, Tipo, Tamanho, Data, Evento) e suporte a ordenação/filtragem.",
			to_unicode_bold("Painel de detalhes:") + " Exibe metadados e ações rápidas para o item selecionado.",
			to_unicode_bold("Mensagens e progresso:") + " Mostra notificações, logs de operação e barras de progresso.",
			to_unicode_bold("Estatísticas:") + " Área para gráficos e relatórios gerados a partir dos dados coletados.",
		),
	),
	ManualSection(
		id="como-comecar",
		title="Como Começar",
		bullets=(
			"Abra o aplicativo pelo atalho ou executável.",
			"Clique em " + to_unicode_bold("Adicionar Diretório") + " e escolha a pasta a ser monitorada.",
			"Execute um scan inicial com " + to_unicode_bold("Iniciar") + "/" + to_unicode_bold("Scan") + ".",
			"Aguarde; os itens serão listados com os metadados disponíveis.",
			"Ative " + to_unicode_bold("Monitoramento contínuo") + " para atualizações automáticas.",
		),
	),
	ManualSection(
		id="modos-operacao",
		title="Modos de Operação",
		bullets=(
			to_unicode_bold("Scan Único:") + " Verificação imediata da pasta selecionada.",
			to_unicode_bold("Monitoramento contínuo:") + " Observação em tempo real de alterações e atualização automática da tabela.",
			to_unicode_bold("Processamento em lote:") + " Extração de metadados ou ações para múltiplos arquivos simultaneamente.",
		),
	),
	ManualSection(
		id="entendendo-tabela",
		title="Entendendo a Tabela de Itens",
		paragraphs=(
			"Cada coluna representa uma propriedade do item. Use ordenação, filtragem e seleção para localizar e analisar itens rapidamente.",
		),
		bullets=(
			to_unicode_bold("Nome:") + " Nome do arquivo ou pasta; duplo clique abre o item.",
			to_unicode_bold("Tipo:") + " Tipo detectado (imagem, vídeo, documento, pasta).",
			to_unicode_bold("Tamanho:") + " Exibido em unidades legíveis (KB/MB/GB).",
			to_unicode_bold("Data:") + " Data da última modificação ou evento registrado.",
			to_unicode_bold("Evento:") + " Indica ações detectadas (criado, modificado, movido, excluído).",
		),
	),
	ManualSection(
		id="painel-detalhes",
		title="Painel de Detalhes e Metadados",
		paragraphs=(
			"Quando um item é selecionado, o painel lateral mostra metadados relevantes e ações rápidas (abrir pasta, copiar caminho, atualizar metadados).",
		),
		bullets=(
			to_unicode_bold("Caminho completo:") + " Local do arquivo no disco.",
			to_unicode_bold("Autor / Criador:") + " Se presente nos metadados.",
			to_unicode_bold("Dimensões:") + " Para imagens (largura × altura).",
			to_unicode_bold("Duração:") + " Para áudio/vídeo.",
			to_unicode_bold("Taxa de bits:") + " Para mídias, quando disponível.",
			to_unicode_bold("Permissões:") + " Indica proteção contra alterações.",
		),
	),
	ManualSection(
		id="acoes-sobre-arquivos",
		title="Ações sobre Arquivos",
		bullets=(
			to_unicode_bold("Abrir:") + " Abra com o aplicativo padrão (duplo clique ou botão).",
			to_unicode_bold("Copiar / Mover:") + " Use copiar/colar ou arrastar para mover arquivos entre pastas.",
			to_unicode_bold("Renomear / Excluir:") + " Acesse via menu de contexto; confirmações são solicitadas para ações permanentes.",
			to_unicode_bold("Restaurar:") + " Quando disponível, recupere exclusões recentes pela função de restauração.",
			to_unicode_bold("Propriedades:") + " Visualize metadados completos e histórico de eventos do arquivo.",
		),
	),
	ManualSection(
		id="pesquisa-filtros",
		title="Pesquisa e Filtros",
		bullets=(
			to_unicode_bold("Pesquisa:") + " Use a caixa de busca para localizar itens por nome ou termo.",
			to_unicode_bold("Filtros:") + " Aplique filtros por tipo, tamanho, data ou evento para reduzir resultados.",
			to_unicode_bold("Combinar filtros:") + " Combine filtros para refinar a seleção.",
		),
	),
	ManualSection(
		id="salvando-restaurando",
		title="Salvar e Restaurar Visualização",
		bullets=(
			to_unicode_bold("Salvar estado:") + " Armazene a configuração atual de colunas e filtros como perfil.",
			to_unicode_bold("Restaurar:") + " Carregue um perfil para recuperar layout e filtros salvos.",
		),
	),
	ManualSection(
		id="processamento-lote",
		title="Processamento em Lote",
		paragraphs=(
			"Selecione vários itens para extrair metadados ou executar ações em massa. O progresso é exibido e a operação pode ser pausada ou cancelada.",
		),
		bullets=(
			to_unicode_bold("Iniciar extração:") + " Selecione itens e escolha 'Extrair Metadados em Lote'.",
			to_unicode_bold("Monitorar progresso:") + " Acompanhe pela barra de progresso e pelo painel de mensagens.",
			to_unicode_bold("Cancelar/Pausar:") + " Use os controles de processo para interromper ou pausar a operação.",
		),
	),
	ManualSection(
		id="relatorios-estatisticas",
		title="Relatórios e Estatísticas",
		paragraphs=(
			"A seção de estatísticas gera gráficos sobre tipos de arquivo, uso de disco e eventos. Exporte imagens ou CSV para análise externa.",
		),
		bullets=(
			to_unicode_bold("Gerar gráficos:") + " Selecione métricas para visualizar distribuições e tendências.",
			to_unicode_bold("Exportar:") + " Salve gráficos como imagens ou exporte dados em CSV.",
		),
	),
	ManualSection(
		id="interface-estrutura-diretorios",
		title="Estrutura de Diretórios",
		bullets=(
			to_unicode_bold("Árvore de diretórios:") + " Navegue para selecionar pastas e avaliar seu status.",
			to_unicode_bold("Ações na árvore:") + " Crie, renomeie ou exclua pastas pelo menu de contexto.",
		),
	),
	ManualSection(
		id="monitoramento-eventos",
		title="Monitoramento de Eventos",
		bullets=(
			to_unicode_bold("Tipos de evento:") + " Criação, modificação, remoção e movimentação.",
			to_unicode_bold("Visualização em tempo real:") + " Eventos recentes são destacados para análise imediata.",
			to_unicode_bold("Notificações:") + " Configure alertas visuais ou sonoros nas Preferências.",
		),
	),
	ManualSection(
		id="preferencias-configuracoes",
		title="Preferências",
		paragraphs=(
			"No painel de Preferências ajuste idioma, comportamento de scan, notificações e atualizações. Revise essas opções ao configurar o aplicativo.",
		),
		bullets=(
			to_unicode_bold("Idioma:") + " Escolha o idioma da interface.",
			to_unicode_bold("Scan:") + " Configure periodicidade, profundidade e exclusões.",
			to_unicode_bold("Notificações:") + " Ative ou desative alertas.",
			to_unicode_bold("Atualizações:") + " Defina verificação automática ou manual.",
		),
	),
	ManualSection(
		id="problemas-comuns",
		title="Problemas Comuns e Soluções",
		bullets=(
			to_unicode_bold("Scan travado ou erro:") + " Aguarde; se persistir, reinicie o scan ou o aplicativo.",
			to_unicode_bold("Itens ausentes:") + " Verifique se a pasta foi adicionada corretamente e as permissões de leitura.",
			to_unicode_bold("Falha ao abrir:") + " Confirme que existe um aplicativo associado ao tipo de arquivo.",
			to_unicode_bold("Metadados faltando:") + " Nem todos os arquivos têm metadados; use 'Atualizar metadados' ou processamento em lote.",
		),
	),
	ManualSection(
		id="atalhos-uteis",
		title="Atalhos",
		bullets=(
			"Ctrl+C / Ctrl+V: Copiar / Colar",
			"Del: Excluir",
			"F3 / Ctrl+F: Buscar",
			"Ctrl+S: Salvar estado da tabela (se disponível)",
		),
	),
	ManualSection(
		id="boas-praticas",
		title="Boas Práticas",
		bullets=(
			"Faça um scan inicial em uma pasta pequena antes de operações maiores.",
			"Salve estados e configurações antes de processos em lote.",
			"Use filtros para focar apenas nos itens relevantes.",
		),
	),
	ManualSection(
		id="logs-e-diagnostico",
		title="Logs e diagnóstico",
		bullets=(
			f"Os logs de execução podem ajudar a diagnosticar problemas; verifique o arquivo de log gerado pela aplicação em: {_DATA_DIR}",
		),
	),
	ManualSection(
		id="faq",
		title="Perguntas frequentes (FAQ)",
		details=(
			ManualDetails(
				summary="Onde meus dados são salvos?",
				paragraphs=(
					f"As tarefas e arquivos de configuração são armazenados no diretório: {_DATA_DIR}",
					"Consulte esse diretório para localizar arquivos de persistência e logs.",
				),
			),
		),
	),
	ManualSection(
		id="suporte",
		title="Como obter ajuda e suporte",
		bullets=(
			"Consulte a seção 'Sobre' dentro do aplicativo para informações oficiais e notas de versão.",
			f"Para problemas mais complexos, gere logs e envie-os ao suporte. Os arquivos de log estão em: {_DATA_DIR}",
			"Envie os arquivos de log e uma descrição detalhada do problema para o email de suporte: linceu_lighthouse@outlook.com.",
		),
	),
)
