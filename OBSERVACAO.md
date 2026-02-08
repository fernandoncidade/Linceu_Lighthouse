═══════════════════════════════════════════════════════════════════════════════
# LINCEU LIGHTHOUSE - SISTEMA DE MONITORAMENTO E ANÁLISE DE ARQUIVOS
═══════════════════════════════════════════════════════════════════════════════

VISÃO GERAL
-----------
Aplicação desktop desenvolvida em Python/PySide6 para monitoramento em tempo real
de operações em sistemas de arquivos (criação, modificação, exclusão, renomeação,
movimentação). Oferece análise estatística avançada, visualização de dados e 
exportação em múltiplos formatos.

TECNOLOGIAS PRINCIPAIS
----------------------
- Framework GUI: PySide6 (Qt6)
- Análise de Dados: pandas, numpy
- Visualização: matplotlib, seaborn, plotly
- Banco de Dados: SQLite3 (com otimizações WAL)
- Multithreading: QThread, concurrent.futures
- Internacionalização: Qt Linguist (6 idiomas)

═══════════════════════════════════════════════════════════════════════════════
## ESTRUTURA DE DIRETÓRIOS E MÓDULOS
═══════════════════════════════════════════════════════════════════════════════

├── main.py
├── LICENSE
├── MANUAL.md
├── OBSERVACAO.md
├── README.md
├── requirements.txt
│
📁 source/
│
├── src_01_InicializadorMain.py             → Funções de inicialização da aplicação (ajuste de CWD, definição de AppUserModelID no Windows, criação da QApplication, configuração do ícone e do sistema de tradução, inicialização dos componentes principais e do writer de BD).
├── src_02_SplashAppStarter.py              → Módulo que cria a QApplication e a splash screen com barra de progresso e log embutido; carregamento robusto de ícone, inicialização de traduções, reporte dinâmico de importações durante startup e disparo da janela principal de forma segura; também inicializa o writer assíncrono de banco quando disponível.
│
├── 📁 gui/ ─────────────────── CAMADA DE INTERFACE GRÁFICA
│   ├── ic_01_InterfaceMonitor.py           → Janela principal da aplicação
│   ├── ic_02_Inicializador.py              → Inicialização de componentes GUI
│   ├── ic_03_Configurador.py               → Configuração de layouts e widgets
│   ├── ic_04_Atualizador.py                → Atualização de interface
│   ├── ic_05_GerenciadorProgresso.py       → Barras de progresso
│   ├── ic_06_GerenciadorMensagens.py       → Sistema de notificações
│   ├── ic_07_ManipuladorTabela.py          → Operações em tabelas
│   ├── ic_08_Internacionalizador.py        → Sistema de traduções
│   ├── ic_09_GerenciadorDesempenho.py      → Gráficos de CPU/RAM/Disco
│   ├── ic_10_EstruturaDiretoriosWidget.py  → Visualização em árvore
│   │
│   ├── 📁 GerenciadorDesempenho/ (16 módulos)
│   │   ├── gdesemp_01_criar_chart.py                   → Criação de gráficos Qt Charts
│   │   ├── gdesemp_02_obter_percentual_disco.py        → Leitura de I/O disco
│   │   ├── gdesemp_03_atualizar.py                     → Coleta de métricas psutil
│   │   ├── gdesemp_04_atualizar_series.py              → Atualização de dados dos gráficos
│   │   ├── gdesemp_05_on_pin_toggled.py                → Handler de fixar/destacar
│   │   ├── gdesemp_06_update_shared_dialog_title.py    → Atualização de título
│   │   ├── gdesemp_07_rebuild_tab_mapping.py           → Reconstrução de mapeamento
│   │   ├── gdesemp_08_repin_all_from_shared.py         → Reafixar todos os gráficos
│   │   ├── gdesemp_09_detach_chart.py                  → Destacar gráfico individual
│   │   ├── gdesemp_10_pin_chart.py                     → Fixar gráfico no painel
│   │   ├── gdesemp_11_aplicar_tema.py                  → Temas claro/escuro
│   │   ├── gdesemp_12_stop.py                          → Parar monitoramento
│   │   ├── gdesemp_13_alternar_graficos_desempenho.py  → Toggle visualização
│   │   ├── gdesemp_14_atualizar_traducoes.py           → Atualização de textos
│   │   ├── gdesemp_15_update_disk_drive_mapping.py     → Mapear letras de unidade
│   │   └── gdesemp_16_update_disk_chart_title.py       → Atualizar título do gráfico
│   │
│   └── 📁 GerenciadorEstruturaDiretoriosWidget/ (16 módulos)
│       ├── gedw_01_configurar_atalhos.py               → Ctrl+C, Ctrl+V, Delete, F2
│       ├── gedw_02_mostrar_menu_contexto.py            → Menu de clique direito
│       ├── gedw_03_obter_selecionados.py               → Obter itens selecionados
│       ├── gedw_04_copiar_selecionados.py              → Copiar para clipboard
│       ├── gedw_05_cortar_selecionados.py              → Cortar para clipboard
│       ├── gedw_06_colar_items.py                      → Colar da clipboard
│       ├── gedw_07_excluir_selecionados.py             → Exclusão de arquivos/pastas
│       ├── gedw_08_renomear_selecionado.py             → Renomear arquivo/pasta
│       ├── gedw_09_criar_nova_pasta.py                 → Criar nova pasta
│       ├── gedw_10_criar_novo_arquivo.py               → Criar novo arquivo
│       ├── gedw_11_abrir_item.py                       → Abrir arquivo/pasta
│       ├── gedw_12_changeEvent.py                      → Handler de mudança de idioma
│       ├── gedw_13_customize_icons.py                  → Customização de ícones
│       ├── gedw_14_atualizar_status.py                 → Atualizar status visual
│       ├── gedw_15_alternar_estrutura_diretorios.py    → Toggle visualização
│       └── gedw_16_obter_status_diretorios.py          → Obter status de arquivos/pastas
│
├── 📁 services/ ───────────── CAMADA DE LÓGICA DE NEGÓCIO
│   ├── ob_01_Observador.py               → Monitoramento via ReadDirectoryChangesW
│   ├── ob_02_BaseEvento.py               → Classe base para eventos
│   ├── ob_03_DiretorioScanner.py         → Escaneamento recursivo inicial
│   ├── ob_04_EventoAdicionado.py         → Processamento de criações
│   ├── ob_05_EventoExcluido.py           → Processamento de exclusões
│   ├── ob_06_EventoModificado.py         → Detecção de modificações
│   ├── ob_07_EventoRenomeado.py          → Detecção de renomeações
│   ├── ob_08_EventoMovido.py             → Detecção de movimentações
│   ├── ob_09_GerenciadorColunas.py       → Configuração de colunas visíveis
│   ├── ob_10_GerenciadorTabela.py        → Operações em tabelas de dados
│   │
│   ├── 📁 GerenciamentoBaseEvento/ (20 módulos)
│   │   ├── gbank_01_set_callback.py                        → Definir callback de eventos
│   │   ├── gbank_02_criar_banco_de_dados.py                → Schema SQLite + índices
│   │   ├── gbank_03_processar_exclusao.py                  → Processar eventos de exclusão
│   │   ├── gbank_04_registrar_evento_especifico.py         → Registro por tipo
│   │   ├── gbank_05_obter_metadados_arquivo_excluido.py    → Recuperar metadados
│   │   ├── gbank_06_registrar_evento_no_banco.py           → Inserção otimizada
│   │   ├── gbank_07_atualizar_interface_apos_evento.py     → Atualização de UI
│   │   ├── gbank_08_scan_directory.py                      → Escanear diretório inicial
│   │   ├── gbank_09_get_tipo_from_snapshot.py              → Obter tipo do snapshot
│   │   ├── gbank_10_is_directory.py                        → Verificar se é diretório
│   │   ├── gbank_11_limpar_registros.py                    → Limpeza de banco de dados
│   │   ├── gbank_12_obter_tipo_anterior.py                 → Obter tipo anterior do arquivo
│   │   ├── gbank_13_notificar_evento.py                    → Notificação de eventos
│   │   ├── gbank_14_remover_exclusao_temporaria.py         → Limpar exclusões temporárias
│   │   ├── gbank_15_criar_evento_exclusao.py               → Criar evento de exclusão
│   │   ├── gbank_16_criar_evento_padrao.py                 → Criar evento genérico
│   │   ├── gbank_17_atualizar_interface_apos_exclusao.py   → Update após delete
│   │   ├── gbank_18_processar_eventos_movimentacao.py      → Lógica complexa
│   │   ├── gbank_19_inserir_evento_movido.py               → Inserção de movimentação
│   │   └── gbank_20_db_writer.py                           → Thread dedicada para escrita
│   │
│   ├── 📁 GerenciamentoDiretorioScanner/ (9 módulos)
│   │   ├── gscanner_01_process_batch.py        → Processamento em lote
│   │   ├── gscanner_02_scan_directory.py       → Varredura recursiva
│   │   ├── gscanner_03_processar_fila.py       → Processamento da fila
│   │   ├── gscanner_04_get_file_type.py        → Identificar tipo de arquivo
│   │   ├── gscanner_05_processar_item.py       → Extração de metadados
│   │   ├── gscanner_06_atualizar_progresso.py  → Atualizar barra de progresso
│   │   ├── gscanner_07_atualizar_interface.py  → Atualizar UI durante scan
│   │   ├── gscanner_08_finalizar_scan.py       → Finalização do scan
│   │   └── gscanner_09_scan_worker_run.py      → Worker thread
│   │
│   ├── 📁 GerenciamentoEventoModificado/ (7 módulos)
│   │   ├── gevmod_01_calcular_intervalo.py             → Debounce inteligente
│   │   ├── gevmod_02_calcular_intervalo_original.py    → Cálculo original de intervalo
│   │   ├── gevmod_03_is_arquivo_codigo_grande.py       → Detecção código-fonte
│   │   ├── gevmod_04_limpar_cache_metadados.py         → Limpeza de cache
│   │   ├── gevmod_05_processar.py                      → Pipeline de processamento
│   │   ├── gevmod_06_processar_massivo.py              → Processamento de operação massiva
│   │   └── gevmod_07_processar_normal.py               → Processamento normal
│   │
│   ├── 📁 GerenciamentoEventoMovido/ (9 módulos)
│   │   ├── gevmov_01_MovimentacaoWorker.py                 → Worker thread para movimentação
│   │   ├── gevmov_02_verificar_movimentacao.py             → Correlação de eventos
│   │   ├── gevmov_03_remover_exclusao.py                   → Limpeza de falsos positivos
│   │   ├── gevmov_04_atualizar_linha_recente.py            → Atualizar linha na tabela
│   │   ├── gevmov_05_atualizar_tabela_completa.py          → Refresh completo
│   │   ├── gevmov_06_inicializar_sistema_evento.py         → Inicialização de sistema
│   │   ├── gevmov_07_processar_exclusoes_pendentes.py      → Processar exclusões
│   │   ├── gevmov_08_adicionar_item_tabela.py              → Adicionar item na UI
│   │   └── gevmov_09_adicionar_evento.py                   → Integração com UI
│   │
│   ├── 📁 GerenciamentoMetadados/ (47 módulos)
│   │   ├── gmet_01_ExtrairMetadados.py                         → Extração genérica
│   │   ├── gmet_02_ExtrairMetadadosCodigoFonte.py              → Análise de código
│   │   ├── gmet_03_ExtrairMetadadosImagem.py                   → EXIF, dimensões
│   │   ├── gmet_04_ExtrairMetadadosAudio.py                    → Duração, bitrate
│   │   ├── gmet_05_ExtrairMetadadosVideo.py                    → Codec, resolução
│   │   ├── gmet_06_ExtrairMetadadosDocumento.py                → PDF, DOCX, TXT
│   │   ├── gmet_07_ExtrairMetadadosPlanilha.py                 → Excel, CSV, XLS
│   │   ├── gmet_08_ExtrairMetadadosApresentacao.py             → PPT, PPTX
│   │   ├── gmet_09_ExtrairMetadadosBancoDados.py               → SQLite, Access
│   │   ├── gmet_10_ExtrairMetadadosExecutavel.py               → EXE, DLL
│   │   ├── gmet_11_ExtrairMetadadosTemporario.py               → Arquivos temporários
│   │   ├── gmet_12_ExtrairMetadadosCompactados.py              → ZIP, RAR, 7Z
│   │   ├── gmet_13_ExtrairMetadadosBackup.py                   → Arquivos de backup
│   │   ├── gmet_14_ExtrairMetadadosLog.py                      → Arquivos de log
│   │   ├── gmet_15_ExtrairMetadadosConfig.py                   → Arquivos de configuração
│   │   ├── gmet_16_ExtrairMetadadosOlefile.py                  → Arquivos OLE
│   │   ├── gmet_17_ExtrairMetadadosDadosEstruturados.py        → Dados estruturados
│   │   ├── gmet_18_ExtrairMetadadosCompletos.py                → Extração completa
│   │   ├── gmet_19_GetTipoArquivo.py                           → Identificação de extensões
│   │   ├── gmet_20_GetTamanhoDiretorioArquivo.py               → Cálculo de tamanho
│   │   ├── gmet_21_GetFormataTamanho.py                        → Formatação de tamanho
│   │   ├── gmet_22_GetAtributosArquivo.py                      → Atributos Win32
│   │   ├── gmet_23_GetAutorArquivo.py                          → Autor/proprietário
│   │   ├── gmet_24_GetDimensoesArquivo.py                      → Dimensões de arquivo
│   │   ├── gmet_25_GetDuracaoArquivo.py                        → Duração de mídia
│   │   ├── gmet_26_GetTaxaBitsArquivo.py                       → Taxa de bits
│   │   ├── gmet_27_GetProtecaoArquivo.py                       → Verificação de assinatura
│   │   ├── gmet_28_AtualizarInterface.py                       → Atualizar após mudança
│   │   ├── gmet_29_SalvarEstadoTabela.py                       → Salvar estado
│   │   ├── gmet_30_RestaurarEstadoTabela.py                    → Restaurar estado
│   │   ├── gmet_31_CarregarConfiguracoes.py                    → Carregar config
│   │   ├── gmet_32_SalvarConfiguracoes.py                      → Salvar config
│   │   ├── gmet_33_ProcessarFilaMetadados.py                   → Processamento assíncrono
│   │   ├── gmet_34_CallbackMetadados.py                        → Callback de conclusão
│   │   ├── gmet_35_ConfigurarTabela.py                         → Configuração de tabela
│   │   ├── gmet_36_MostrarDialogoConfiguracao.py               → Diálogo de config
│   │   ├── gmet_37_InvalidarCacheDiretoriosRelacionados.py     → Invalidação
│   │   ├── gmet_38_GetMetadados.py                             → Obter metadados principal
│   │   ├── gmet_39_IdentificarTipoArquivo.py                   → Identificação de tipo
│   │   ├── gmet_40_AdicionarMetadadosAoItem.py                 → Adicionar metadados
│   │   ├── gmet_41_ProcessarColunaThread.py                    → Thread por coluna
│   │   ├── gmet_42_AdicionarItemParaColuna.py                  → Adicionar à fila
│   │   ├── gmet_43_AtualizarColunaInterface.py                 → Atualizar coluna
│   │   ├── gmet_44_ExtrairMetadadosEmLote.py                   → Extração em lote
│   │   ├── gmet_45_MetadadosExtraidosCallback.py               → Callback de extração
│   │   ├── gmet_46_GetSizeUnit.py                              → Conversão de unidade
│   │   └── gmet_47_GetTamanhoBytes.py                          → Tamanho em bytes
│   │
│   ├── 📁 GerenciamentoObservador/ (13 módulos)
│   │   ├── gob_01_DetectarOperacaoMassiva.py           → Detecção de operação massiva
│   │   ├── gob_02_Iniciar.py                           → Inicialização de threads
│   │   ├── gob_03_HandleScanError.py                   → Handler de erros de scan
│   │   ├── gob_04_IniciarMonitoramento.py              → Inicialização de threads
│   │   ├── gob_05_ProcessarBufferEventos.py            → Processamento de buffer
│   │   ├── gob_06_PararScan.py                         → Parar escaneamento
│   │   ├── gob_07_Parar.py                             → Parar observador
│   │   ├── gob_08_LimparEstado.py                      → Limpeza de estado
│   │   ├── gob_09_Monitorar.py                         → Loop principal Win32 API
│   │   ├── gob_10_ProcessarEventoInterno.py            → Processamento interno
│   │   ├── gob_11_ProcessarEvento.py                   → Processamento principal
│   │   ├── gob_12_ReiniciarMonitoramento.py            → Reinicialização
│   │   └── gob_13_PausarMonitoramentoEscaneamento.py   → Controle pausar/retomar
│   │
│   └── 📁 GerenciamentoTabela/ (47 módulos)
│       ├── gtab_01_detectar_tema_windows.py                        → Tema claro/escuro sistema
│       ├── gtab_02_calcular_cor_texto_ideal.py                     → Contraste automático
│       ├── gtab_03_configurar_tabela.py                            → Configuração inicial
│       ├── gtab_04_ajustar_larguras_colunas.py                     → Ajuste de largura
│       ├── gtab_05_aplicar_quebra_linha_cabecalho.py               → Quebra de linha
│       ├── gtab_06_aplicar_quebra_linha_todos_cabecalhos.py        → Aplicar todas
│       ├── gtab_07_ajustar_altura_cabecalho.py                     → Ajuste de altura
│       ├── gtab_08_redimensionar_cabecalho.py                      → Handler de redimensionamento
│       ├── gtab_09_atualizar_cabecalhos.py                         → Atualizar cabeçalhos
│       ├── gtab_10_atualizar_dados_tabela.py                       → Refresh de dados
│       ├── gtab_11_atualizar_linha_mais_recente.py                 → Update última linha
│       ├── gtab_12_atualizar_visualizacao_tabela.py                → Refresh visual
│       ├── gtab_13_atualizar_visibilidade_colunas.py               → Mostrar/ocultar
│       ├── gtab_14_invalidar_cache_cores.py                        → Limpar cache de cores
│       ├── gtab_15_obter_cores_operacao.py                         → Obter cores configuradas
│       ├── gtab_16_obter_indices_colunas.py                        → Mapear índices
│       ├── gtab_17_ativar_cores.py                                 → Ativar coloração
│       ├── gtab_18_ocultar_cores.py                                → Desativar coloração
│       ├── gtab_19_aplicar_cores_linha_especifica.py               → Colorir linha
│       ├── gtab_20_aplicar_cores_todas_colunas.py                  → Coloração baseada em regras
│       ├── gtab_21_redefinir_cores_todas_colunas.py                → Reset de cores
│       ├── gtab_22_remover_cor_coluna.py                           → Remover cor de coluna
│       ├── gtab_23_atualizar_cores_colunas.py                      → Atualizar cores
│       ├── gtab_24_set_coluna_colorir.py                           → Definir coluna colorida
│       ├── gtab_25_set_colunas_colorir_em_massa.py                 → Definir múltiplas
│       ├── gtab_26_remover_todas_cores_colunas.py                  → Remover todas cores
│       ├── gtab_27_salvar_configuracoes_cores.py                   → Persistir config
│       ├── gtab_28_carregar_configuracoes_cores.py                 → Carregar config
│       ├── gtab_29_eh_coluna_personalizada_colorida.py             → Verificar tipo
│       ├── gtab_30_mostrar_dialogo_configuracao.py                 → Diálogo de config
│       ├── gtab_31_ajustar_cor_selecao.py                          → Ajustar cor de seleção
│       ├── gtab_32_worker_thread.py                                → Thread worker genérica
│       ├── gtab_33_atualizar_estilo_tema.py                        → Aplicar tema claro/escuro
│       ├── gtab_34_monitor_tema_windows.py                         → Detecção de mudanças de tema
│       ├── gtab_35_iniciar_processamento_pesado.py                 → Processamento pesado
│       ├── gtab_36_aplicar_cores_todas_colunas_processamento.py    → Coloração
│       ├── gtab_37_processar_cores_em_background.py                → Processamento async
│       ├── gtab_38_on_cores_processadas.py                         → Callback de cores
│       ├── gtab_39_atualizar_cores_na_interface.py                 → Aplicar na UI
│       ├── gtab_40_atualizar_interface_pos_processamento.py        → Update final
│       ├── gtab_41_processar_selecao_background.py                 → Processar seleção
│       ├── gtab_42_shutdown_executors.py                           → Encerrar threads
│       ├── gtab_43_atualizar_cabecalhos.py                         → Atualizar após mudança
│       ├── gtab_44_on_idioma_alterado.py                           → Handler de idioma
│       ├── gtab_45_retraduzir_dados_existentes.py                  → Retradução
│       ├── gtab_46_executar_retraducao_agendada.py                 → Executar retradução
│       └── gtab_47_event_table_model.py                            → Model MVC customizado
│
├── 📁 ui/ ─────────────────── COMPONENTES DE INTERFACE AVANÇADOS
│   ├── ui_01_GerenciadorBotoes.py              → Botões de ação
│   ├── ui_02_GerenciadorBotoesUI.py            → Factory de botões
│   ├── ui_03_GerenciadorMenusUI.py             → Barra de menus
│   ├── ui_04_GerenciadorEventosUI.py           → Handlers de eventos
│   ├── ui_05_GerenciadorProgressoUI.py         → Feedback de progresso
│   ├── ui_06_GerenciadorEstatisticasUI.py      → Janela de estatísticas
│   ├── ui_07_GerenciadorDados.py               → Salvar/Carregar
│   ├── ui_08_GerenciadorEventosArquivo.py      → Eventos de arquivo
│   ├── ui_09_GerenciadorMonitoramento.py       → Controle de monitoramento
│   ├── ui_10_GerenciadorLimpeza.py             → Limpeza de dados
│   ├── ui_11_DialogoCores.py                   → Seletor de cores customizado
│   ├── ui_12_LocalizadorQt.py                  → Sistema de traduções
│   ├── ui_13_TradutorMetadadosQt.py            → Tradução de metadados
│   ├── ui_14_OpcoesSobre.py                    → Diálogo "Sobre"
│   ├── ui_15_Manual.py                         → Diálogo "Manual"
│   │
│   ├── 📁 GerenciamentoBotoes/ (6 módulos)
│   │   ├── geb_01_selecionar_diretorio.py                      → QFileDialog
│   │   ├── geb_02_alternar_analise_diretorio.py                → Start/Stop
│   │   ├── geb_03_exportar_dados.py                            → Excel, CSV, JSON, XML
│   │   ├── geb_04_exportar_para_sqlite.py                      → Exportação SQLite
│   │   ├── geb_05_limpar_dados.py                              → Limpeza de dados
│   │   └── geb_06_pausar_monitoramento_ou_escaneamento.py      → Pausar/retomar
│   │
│   ├── 📁 GerenciamentoDialogoCores/ (8 módulos)
│   │   ├── gdc_01_setup_ui.py                  → Layout do diálogo
│   │   ├── gdc_02_adicionar_grid_cores.py      → Paleta de cores
│   │   ├── gdc_03_selecionar_cor.py            → Selecionar cor da paleta
│   │   ├── gdc_04_abrir_seletor_avancado.py    → QColorDialog integrado
│   │   ├── gdc_05_accept.py                    → Confirmar seleção
│   │   ├── gdc_06_traduzir_dialogo_cores.py    → Tradução de diálogo
│   │   ├── gdc_07_obter_cor.py                 → Obter cor selecionada
│   │   └── gdc_08_atualizar_traducoes.py       → Atualizar textos
│   │
│   ├── 📁 GerenciamentoEstatisticasUI/ (31 módulos)
│   │   ├── geui_01_mostrar_estatisticas.py                             → Janela principal
│   │   ├── geui_02_salvar_todos_graficos.py                            → Salvar todos gráficos
│   │   ├── geui_03_limpar_referencia_dialog.py                         → Limpar referências
│   │   ├── geui_04_atualizar_graficos_apos_mudanca_idioma.py           → Update idioma
│   │   ├── geui_05_criar_painel_selecao.py                             → Criar painel de seleção
│   │   ├── geui_06_criar_painel_graficos.py                            → Criar painel de gráficos
│   │   ├── geui_07_criar_botao_toggle_painel.py                        → Botão expandir/recolher
│   │   ├── geui_08_criar_lista_graficos.py                             → Lista de gráficos disponíveis
│   │   ├── geui_09_criar_mapeamento_funcoes.py                         → Mapeamento de funções
│   │   ├── geui_10_popular_checkboxes.py                               → Popular checkboxes
│   │   ├── geui_11_verificar_estado_checkbox_todos.py                  → Verificar estado
│   │   ├── geui_12_alternar_todos_checkboxes.py                        → Selecionar/desselecionar
│   │   ├── geui_13_obter_estados_checkboxes.py                         → Obter estados atuais
│   │   ├── geui_14_gerar_todos_graficos.py                             → Geração assíncrona
│   │   ├── geui_15_atualizar_graficos.py                               → Atualizar gráficos
│   │   ├── geui_16_atualizar_graficos_sem_fechar.py                    → Hot reload
│   │   ├── geui_17_regenerar_graficos_existentes.py                    → Regenerar gráficos
│   │   ├── geui_18_salvar_graficos_selecionados.py                     → Salvar selecionados
│   │   ├── geui_19_toggle_painel_selecao.py                            → Expandir/recolher painel
│   │   ├── geui_20_atualizar_textos_painel_selecao.py                  → Atualizar textos
│   │   ├── geui_21_atualizar_textos_checkboxes.py                      → Atualizar checkboxes
│   │   ├── geui_22_atualizar_layout_apos_mudanca_botao.py              → Update layout
│   │   ├── geui_23_atualizar_checkboxes_graficos.py                    → Atualizar checkboxes
│   │   ├── geui_24_atualizar_abas_graficos.py                          → Atualizar abas
│   │   ├── geui_25_atualizar_dados_graficos_com_novos_titulos.py       → Update
│   │   ├── geui_26_calcular_largura_ideal.py                           → Calcular largura painel
│   │   ├── geui_27_ajustar_largura_painel_selecao.py                   → Ajustar largura
│   │   ├── geui_28_traduzir_botoes_detalhes.py                         → Traduzir botões
│   │   ├── geui_29_abrir_diretorio.py                                  → Abrir pasta de saída
│   │   ├── geui_30_botao_rotacionado.py                                → Widget de botão vertical
│   │   └── geui_31_worker_grafico.py                                   → Thread worker para gráficos
│   │
│   ├── 📁 GerenciamentoEventosUI/ (11 módulos)
│   │   ├── geve_01_alternar_filtro.py                  → Filtros de operação
│   │   ├── geve_02_alternar_visibilidade_coluna.py     → Mostrar/ocultar coluna
│   │   ├── geve_03_resetar_colunas.py                  → Restaurar colunas padrão
│   │   ├── geve_04_resetar_cores.py                    → Restaurar cores padrão
│   │   ├── geve_05_redefinir_todas_colunas_cores.py    → Reset completo
│   │   ├── geve_06_alterar_idioma.py                   → Troca de idioma
│   │   ├── geve_07_confirmar_mudanca_idioma.py         → Confirmar alteração
│   │   ├── geve_08_limpar_dados_monitorados.py         → Limpeza de dados
│   │   ├── geve_09_limpar_dados_interface.py           → Limpeza de UI
│   │   ├── geve_10_reiniciar_aplicativo.py             → Restart após mudança
│   │   └── geve_11_atualizar_interface.py              → Atualizar interface
│   │
│   ├── 📁 GerenciamentoLocalizadorQt/ (14 módulos)
│   │   ├── glqt_01_inicializar_tradutor_metadados.py       → Init tradutor
│   │   ├── glqt_02_criar_mapa_compatibilidade.py           → Mapa de compatibilidade
│   │   ├── glqt_03_carregar_tradutor.py                    → Carregamento de .qm
│   │   ├── glqt_04_set_idioma.py                           → Mudança de idioma
│   │   ├── glqt_05_get_text.py                             → Obter texto traduzido
│   │   ├── glqt_06_get_fallback_text.py                    → Fallback de tradução
│   │   ├── glqt_07_tr.py                                   → Método de tradução
│   │   ├── glqt_08_salvar_preferencia_idioma.py            → Salvar idioma
│   │   ├── glqt_09_carregar_preferencia_idioma.py          → Carregar idioma
│   │   ├── glqt_10_get_idiomas_disponiveis.py              → Lista de idiomas
│   │   ├── glqt_11_traduzir_tipo_operacao.py               → Tradução de operações
│   │   ├── glqt_12_traduzir_metadados.py                   → Traduzir metadados
│   │   ├── glqt_13_traduzir_tipo_operacao_fallback.py      → Fallback operação
│   │   └── glqt_14_criar_arquivos_traducao.py              → Criar arquivos .ts
│   │
│   ├── 📁 GerenciamentoMenusUI/ (23 módulos)
│   │   ├── gmui_01_MenuPersistente.py                      → Menu que não fecha automaticamente
│   │   ├── gmui_02_GerenciadorCores.py                     → Sistema de cores configuráveis
│   │   ├── gmui_03_SobreDialog.py                          → Diálogo "Sobre"
│   │   ├── gmui_04_criar_menu_principal.py                 → Criar menu principal
│   │   ├── gmui_05_configurar_menu_arquivo.py              → Menu Arquivo
│   │   ├── gmui_06_configurar_menu_configuracoes.py        → Menu Configurações
│   │   ├── gmui_07_configurar_menu_opcoes.py               → Menu Opções
│   │   ├── gmui_08_criar_submenu_cores.py                  → Submenu de personalização
│   │   ├── gmui_09_criar_icone_cor.py                      → Criar ícone colorido
│   │   ├── gmui_10_abrir_dialogo_cor.py                    → Abrir seletor de cor
│   │   ├── gmui_11_criar_submenu_colunas.py                → Submenu de colunas
│   │   ├── gmui_12_alternar_ordenacao_linhas.py            → Toggle ordenação
│   │   ├── gmui_13_criar_submenu_colunas_coloridas.py      → Submenu cores
│   │   ├── gmui_14_selecionar_todas_colunas.py             → Selecionar todas
│   │   ├── gmui_15_selecionar_todas_cores_colunas.py       → Colorir todas
│   │   ├── gmui_16_criar_submenu_exportacao.py             → Submenu exportação
│   │   ├── gmui_17_resetar_opcoes_exportacao.py            → Reset exportação
│   │   ├── gmui_18_criar_submenu_idiomas.py                → Submenu de idiomas
│   │   ├── gmui_19_get_texto_traduzido_para_idioma.py      → Get tradução
│   │   ├── gmui_20_confirmar_alteracao_idioma.py           → Confirmar mudança
│   │   ├── gmui_21_on_traducoes_carregadas.py              → Callback de tradução
│   │   ├── gmui_22_exibir_sobre.py                         → Diálogo informativo
│   │   └── gmui_23_toggle_desempenho.py                    → Toggle gráficos desempenho
│   │
│   ├── 📁 GerenciamentoTradutorMetadadosQt/ (9 módulos)
│   │   ├── gtmqt_01_verificar_idioma_cache.py          → Verificar cache
│   │   ├── gtmqt_02_traduzir_tipo_operacao.py          → Tradução de operações
│   │   ├── gtmqt_03_obter_chave_traducao_reversa.py    → Tradução reversa
│   │   ├── gtmqt_04_traduzir_metadados.py              → Tradução de metadados
│   │   ├── gtmqt_05_traduzir_tipo_arquivo.py           → Tradução de tipo
│   │   ├── gtmqt_06_traduzir_atributos.py              → Tradução de atributos
│   │   ├── gtmqt_07_traduzir_autor.py                  → Tradução de autor
│   │   ├── gtmqt_08_traduzir_protegido.py              → Tradução de status
│   │   └── gtmqt_09_traduzir_dimensoes.py              → Tradução de dimensões
│   │
│   └── 📁 Manual/ (7 módulos)
│       ├── common_Manual.py     → Utilitários do manual: dataclasses (ManualSection, ManualDetails, ManualBlock), função to_unicode_bold para conversão de texto em negrito Unicode e inicialização de _DATA_DIR via obter_caminho_persistente(); fornece a estrutura de dados usada por todos os documentos de idioma e pelo visualizador do manual.
│       ├── DOC_PT_BR.py         → Documento do manual em Português (pt_BR); define a estrutura de seções e detalhes (_DOC_PT_BR / _DOC) usando ManualSection/ManualDetails e referencia _DATA_DIR para assets locais.
│       ├── DOC_EN_US.py         → Documento do manual em Inglês (en_US); equivalente a DOC_PT_BR.py com textos traduzidos e mesma estrutura de seções.
│       ├── DOC_ES_ES.py         → Documento do manual em Espanhol (es_ES); versão traduzida do manual, importando common_Manual para compor seções e detalhes.
│       ├── DOC_FR_FR.py         → Documento do manual em Francês (fr_FR); contém as seções traduzidas e metadados do manual integrados com common_Manual.
│       ├── DOC_IT_IT.py         → Documento do manual em Italiano (it_IT); versão traduzida estruturada com ManualSection/ManualDetails.
│       └── DOC_DE_DE.py         → Documento do manual em Alemão (de_DE); versão traduzida estruturada com ManualSection/ManualDetails.
│
├── 📁 data/ ───────────────── GERAÇÃO DE ESTATÍSTICAS E GRÁFICOS
│   ├── st_01_GeradorEstatisticas.py      → Gerenciador principal
│   │
│   └── 📁 GeradorEstatisticas/ (18 módulos)
│       ├── gst_01_base_gerador.py                      → Classe base abstrata
│       ├── gst_02_grafico_pizza.py                     → Distribuição de operações
│       ├── gst_03_grafico_barras.py                    → Top 30 tipos de arquivo
│       ├── gst_04_grafico_timeline.py                  → Linha do tempo
│       ├── gst_05_grafico_treemap.py                   → Mapa de árvore
│       ├── gst_06_grafico_histograma.py                → Distribuição por hora
│       ├── gst_07_grafico_pareto.py                    → Análise 80/20
│       ├── gst_08_grafico_linha.py                     → Evolução temporal
│       ├── gst_09_grafico_boxplot.py                   → Distribuição de tamanhos
│       ├── gst_10_grafico_radar_eventos.py             → Eventos por hora/dia
│       ├── gst_11_grafico_heatmap.py                   → Mapa de calor temporal
│       ├── gst_12_grafico_scatter.py                   → Análise de tamanho vs tempo
│       ├── gst_13_grafico_sankey.py                    → Fluxo de operações
│       ├── gst_14_grafico_radar.py                     → Operações por tipo
│       ├── gst_15_grafico_dotplot.py                   → Distribuição de tamanhos
│       ├── gst_16_grafico_sankey_evento_caminho.py     → Fluxo evento→caminho
│       ├── gst_17_grafico_sankey_tipo_caminho.py       → Fluxo tipo→caminho
│       └── gst_18_grafico_arvore_diretorios.py         → Estrutura de pastas
│
├── 📁 tools/ ──────────────── FERRAMENTAS E UTILITÁRIOS DE UI
│   ├── fil_01_Filtros.py                       → Janela de filtros avançados
│   ├── fil_02_AdministradorCalendario.py       → Seletor de datas
│   ├── fil_03_AdministradorFiltros.py          → Lógica de filtragem
│   │
│   ├── 📁 GerenciamentoAdministradorFiltros/ (10 módulos)
│   │   ├── gadmfil_01_desconectar_sinais.py                            → Limpeza de sinais
│   │   ├── gadmfil_02_aplicar_filtros.py                               → Aplicação de regras
│   │   ├── gadmfil_03_limpar_filtros.py                                → Limpar todos filtros
│   │   ├── gadmfil_04_sincronizar_menu_principal_com_filtros.py        → Sincronizar menu principal com filtros
│   │   ├── gadmfil_05_atualizar_contagem.py                            → Atualizar contadores
│   │   ├── gadmfil_06_atualizar_contagem_eventos_monitorados.py        → Atualizar contagem eventos
│   │   ├── gadmfil_07_verificar_filtro_operacao.py                     → Verificar filtro
│   │   ├── gadmfil_08_atualizar_contagem_apos_idioma.py                → Atualizar contagem após idioma
│   │   ├── gadmfil_09_notificar_alteracao_idioma.py                    → Notificar alteração de idioma
│   │   └── gadmfil_10_salvar_estado_checkboxes.py                      → Persistir estado
│   │
│   └── 📁 GerenciamentoFiltros/ (10 módulos)
│       ├── gfil_01_on_idioma_alterado.py                   → Handler de mudança idioma
│       ├── gfil_02_desconectar_sinais.py                   → Limpeza de sinais
│       ├── gfil_03_atualizar_status.py                     → Atualizar status
│       ├── gfil_04_setup_ui.py                             → Layout da janela
│       ├── gfil_05_on_filtro_alterado.py                   → Handler de alteração
│       ├── gfil_06_sincronizar_com_menu_principal.py       → Sincronizar menu principal
│       ├── gfil_07_verificar_filtro_operacao.py            → Verificação de filtro
│       ├── gfil_08_atualizar_contagem.py                   → Atualizar contadores
│       ├── gfil_09_atualizar_interface.py                  → Refresh após mudanças
│       └── gfil_10_limpar_filtros.py                       → Limpar filtros
│
├── 📁 utils/ ──────────────── UTILITÁRIOS TRANSVERSAIS
│   ├── LogManager.py                     → Sistema centralizado de logs
│   │   • Configuração de níveis de log
│   │   • Rotação automática de arquivos
│   │   • Formatação customizada
│   │   • Thread-safe logging
│   │
│   ├── IconUtils.py                      → Gerenciamento de ícones
│   │   • Busca de ícones em múltiplos paths
│   │   • Suporte a executáveis empacotados
│   │   • Cache de ícones carregados
│   │   • Fallback para ícones padrão
│   │
│   ├── CaminhoPersistenteUtils.py        → Paths de configuração
│   │   • Diretório de dados do usuário
│   │   • Criação automática de estrutura
│   │   • Compatibilidade multiplataforma
│   │   • Paths seguros para escrita
│   │
│   └── ApplicationPathUtils.py           → Paths da aplicação
│       • Detecção de ambiente (dev/prod)
│       • Suporte a PyInstaller
│       • Carregamento de recursos
│       • Paths relativos e absolutos
│
├── 📁 locale/ ─────────────── INTERNACIONALIZAÇÃO
│   ├── compile_translations.py           → Script de compilação
│   │   • find_lrelease()                 → Localizar ferramenta Qt
│   │   • compile_with_lrelease()         → Compilar com lrelease
│   │   • parse_ts_file()                 → Parse XML .ts
│   │   • compile_ts_to_qm_fallback()     → Compilação fallback
│   │   • validate_ts_file()              → Validação de arquivo
│   │   • compile_translations()          → Compilar todos
│   │   • validate_translations()         → Validar traduções
│   │   • list_translations()             → Listar disponíveis
│   │   • clean_compiled()                → Limpar .qm
│   │   • show_stats()                    → Estatísticas de tradução
│   │
│   ├── linceu_pt_BR.ts                   → Português (base)
│   │   • 600+ strings traduzidas
│   │   • Contexto "LinceuLighthouse"
│   │   • Encoding UTF-8
│   │
│   ├── linceu_en_US.ts                   → English
│   │   • Interface completa
│   │   • Mensagens de erro
│   │   • Tooltips e hints
│   │
│   ├── linceu_es_ES.ts                   → Español
│   │   • Tradução nativa
│   │   • Termos técnicos
│   │   • Formatação de datas
│   │
│   ├── linceu_fr_FR.ts                   → Français
│   │   • Gramática francesa
│   │   • Acentuação correta
│   │   • Termos localizados
│   │
│   ├── linceu_it_IT.ts                   → Italiano
│   │   • Tradução italiana
│   │   • Termos técnicos IT
│   │   • Formatação local
│   │
│   └── linceu_de_DE.ts                   → Deutsch
│       • Tradução alemã
│       • Termos compostos
│       • Capitalização correta
│
└── 📁 mocks/
    └── find_VersionEditor.py             → Editor de Versões

═══════════════════════════════════════════════════════════════════════════════
## ARQUITETURA E PADRÕES DE DESIGN
═══════════════════════════════════════════════════════════════════════════════

PRINCÍPIOS SOLID APLICADOS
---------------------------
[S] Single Responsibility: Cada módulo tem uma responsabilidade única
    - gbank_06: apenas registro em banco
    - gmet_03: apenas extração de metadados de imagens
    
[O] Open/Closed: Extensível via herança (BaseGerador, BaseEvento)
    - Novos tipos de gráficos herdam de gst_01_base_gerador.py
    
[L] Liskov Substitution: Todos os geradores de gráfico são intercambiáveis
    
[I] Interface Segregation: Interfaces específicas (EventoAdicionado, EventoExcluido)
    
[D] Dependency Inversion: Injeção de dependências (loc, interface, db_path)

PADRÕES DE DESIGN IMPLEMENTADOS
--------------------------------
• Observer Pattern: Monitoramento de arquivos (ob_01_Observador.py)
• Factory Pattern: Criação de botões (ui_02_GerenciadorBotoesUI.py)
• Strategy Pattern: Diferentes estratégias de exportação (CSV, Excel, JSON)
• Singleton Pattern: LogManager, DatabaseWriter
• Model-View-Controller: EventTableModel + QTableView
• Template Method: BaseGerador define esqueleto, subclasses implementam detalhes
• Facade Pattern: GerenciadorEstatisticasUI simplifica acesso a gráficos

MULTITHREADING E PERFORMANCE
-----------------------------
• QThread para operações longas (escaneamento, geração de gráficos)
• ThreadPoolExecutor para processamento paralelo de metadados
• DatabaseWriter com thread dedicada para escrita assíncrona
• Debouncing inteligente para eventos de modificação
• Cache de metadados com invalidação seletiva
• Processamento em lote (batch processing) para inserções no banco

OTIMIZAÇÕES DE BANCO DE DADOS
------------------------------
• SQLite com modo WAL (Write-Ahead Logging)
• Índices em colunas frequentemente consultadas
• Transações em lote para inserções massivas
• PRAGMA otimizations (page_size, cache_size, mmap_size)
• Thread dedicada para operações de I/O

SISTEMA DE CORES E TEMAS
-------------------------
• Detecção automática de tema do Windows (claro/escuro)
• Cores personalizáveis por tipo de operação
• Cálculo automático de contraste para legibilidade
• Persistência de preferências de cores
• Aplicação de cores em tempo real sem necessidade de restart

═══════════════════════════════════════════════════════════════════════════════
## FLUXO DE EXECUÇÃO PRINCIPAL
═══════════════════════════════════════════════════════════════════════════════

1. INICIALIZAÇÃO (src_01_InicializadorMain.py)
   └─> QApplication.instance()
   └─> Internacionalizador.inicializar_sistema_traducao()
   └─> InterfaceMonitor.__init__()
       └─> Inicializador.inicializar_componentes()
       └─> Inicializador.inicializar_gerenciadores()
       └─> Configurador.setup_ui()
       └─> ManipuladorTabela.configurar_tabela()

2. SELEÇÃO DE DIRETÓRIO
   └─> GerenciadorBotoes.selecionar_diretorio()
       └─> QFileDialog.getExistingDirectory()
       └─> Observador.__init__(diretorio)

3. INÍCIO DO MONITORAMENTO
   └─> GerenciadorBotoes.alternar_analise_diretorio()
       └─> Observador.iniciar()
           ├─> DiretorioScanner.scan_directory() [Thread]
           │   └─> Processa arquivos existentes
           │   └─> Insere snapshot inicial no banco
           └─> Observador.monitorar() [Thread]
               └─> Loop Win32 ReadDirectoryChangesW
               └─> Detecta: CREATE, DELETE, MODIFY, RENAME, MOVE

4. PROCESSAMENTO DE EVENTOS
   └─> Observador.processar_evento()
       ├─> EventoAdicionado.processar()
       ├─> EventoExcluido.processar()
       ├─> EventoModificado.processar()
       ├─> EventoRenomeado.processar()
       └─> EventoMovido.verificar_movimentacao()
           └─> BaseEvento.notificar_evento()
               └─> BaseEvento.registrar_evento_no_banco()
                   └─> DatabaseWriter.enqueue_event()
                       └─> Inserção assíncrona em lote

5. ATUALIZAÇÃO DA INTERFACE
   └─> InterfaceMonitor.inserir_evento_streaming()
       └─> GerenciadorTabela.atualizar_linha_mais_recente()
           ├─> Aplica cores baseadas no tipo de operação
           ├─> Calcula contraste automático
           └─> Atualiza contadores

6. GERAÇÃO DE ESTATÍSTICAS
   └─> GerenciadorEstatisticasUI.mostrar_estatisticas()
       └─> GeradorEstatisticas._gerar_todos_graficos()
           └─> GraficoWorker.run() [Thread]
               ├─> Consulta dados do banco
               ├─> Gera 18 tipos de gráficos
               └─> Renderiza em FigureCanvasQTAgg

7. EXPORTAÇÃO DE DADOS
   └─> GerenciadorBotoes.exportar_dados()
       ├─> Excel: pandas.to_excel()
       ├─> CSV: pandas.to_csv()
       ├─> JSON: json.dump()
       ├─> XML: ElementTree
       └─> SQLite: conexão direta

8. MUDANÇA DE IDIOMA
   └─> GerenciadorEventosUI.alterar_idioma()
       └─> LocalizadorQt.set_idioma()
           ├─> QTranslator.load("linceu_XX.qm")
           ├─> Retraduz interface completa
           ├─> Retraduz dados da tabela
           └─> Atualiza gráficos abertos

═══════════════════════════════════════════════════════════════════════════════
## TRATAMENTO DE ERROS E LOGGING
═══════════════════════════════════════════════════════════════════════════════

ESTRATÉGIA DE LOGGING
---------------------
• Nível DEBUG: Operações detalhadas (loops, iterações)
• Nível INFO: Eventos importantes (início de scan, salvamento)
• Nível WARNING: Situações anormais mas recuperáveis
• Nível ERROR: Erros que não interrompem a aplicação
• Nível CRITICAL: Erros fatais

TRATAMENTO DE EXCEÇÕES
-----------------------
• Try-except em todas as operações críticas
• Logging detalhado com exc_info=True
• Fallbacks para operações falhadas
• Mensagens de erro amigáveis ao usuário (QMessageBox)
• Graceful degradation (continua funcionando com funcionalidade reduzida)

═══════════════════════════════════════════════════════════════════════════════
## REQUISITOS E DEPENDÊNCIAS
═══════════════════════════════════════════════════════════════════════════════

BIBLIOTECAS PRINCIPAIS
-----------------------
PySide6>=6.5.0           # Framework Qt6
pandas>=2.0.0            # Análise de dados
matplotlib>=3.7.0        # Visualização de gráficos
seaborn>=0.12.0          # Gráficos estatísticos
plotly==5.22.0           # Gráficos interativos (Sankey)
Pillow>=10.0.0           # Processamento de imagens
tinytag>=1.10.0          # Metadados de áudio
pymediainfo>=6.0.0       # Metadados de vídeo
PyPDF2>=3.0.0            # Metadados de PDF
openpyxl>=3.1.0          # Leitura/escrita Excel
python-docx>=0.8.11      # Metadados de DOCX
chardet>=5.1.0           # Detecção de encoding
squarify>=0.4.3          # Gráficos treemap
psutil>=5.9.0            # Monitoramento de sistema
pywin32>=305             # API Windows

REQUISITOS DE SISTEMA
----------------------
• Windows 10/11 (64-bit)
• Python 3.10+
• 4GB RAM mínimo (8GB recomendado)
• 100MB espaço em disco

═══════════════════════════════════════════════════════════════════════════════
## FUNCIONALIDADES PRINCIPAIS
═══════════════════════════════════════════════════════════════════════════════

MONITORAMENTO EM TEMPO REAL
----------------------------
✓ Detecção de criação de arquivos/pastas
✓ Detecção de exclusão de arquivos/pastas
✓ Detecção de modificação de conteúdo
✓ Detecção de renomeação
✓ Detecção de movimentação entre pastas
✓ Distinção entre operações de arquivo vs diretório
✓ Debouncing inteligente para arquivos grandes
✓ Suporte a operações massivas (batch)

EXTRAÇÃO DE METADADOS (47 módulos especializados)
--------------------------------------------------
✓ Código-fonte: linhas, classes, funções, imports
✓ Imagens: dimensões, EXIF, formato, DPI
✓ Áudio: duração, bitrate, artista, álbum
✓ Vídeo: codec, resolução, taxa de frames, duração
✓ Documentos: páginas, palavras, autor, data criação
✓ Planilhas: número de sheets, linhas, colunas
✓ Apresentações: número de slides
✓ Compactados: arquivos contidos, tamanho descompactado
✓ Bancos de dados: tabelas, registros
✓ Executáveis: versão, assinatura digital, arquitetura
✓ Logs: primeira/última entrada, número de linhas
✓ Configurações: formato detectado

VISUALIZAÇÃO DE DADOS (18 tipos de gráficos)
---------------------------------------------
✓ Pizza: Distribuição de operações
✓ Barras: Top tipos de arquivo
✓ Timeline: Linha do tempo de eventos
✓ Treemap: Hierarquia de tipos
✓ Histograma: Distribuição por hora do dia
✓ Pareto: Análise 80/20 de operações
✓ Linha: Evolução temporal diária
✓ Boxplot: Distribuição de tamanhos
✓ Radar: Eventos por hora/dia/tipo
✓ Heatmap: Mapa de calor temporal
✓ Scatter: Tamanho vs tempo
✓ Sankey: Fluxo de operações/tipos/caminhos
✓ Dotplot: Distribuição de tamanhos
✓ Árvore: Estrutura de diretórios

FILTROS AVANÇADOS
-----------------
✓ Por tipo de operação (moved, renamed, added, deleted, modified, scanned)
✓ Por tipo de arquivo (extensão)
✓ Por intervalo de datas
✓ Por nome/texto contido
✓ Combinação de múltiplos filtros
✓ Taxa de filtragem em tempo real
✓ Sincronização com menu principal

EXPORTAÇÃO DE DADOS
-------------------
✓ Excel (.xlsx) - com formatação
✓ CSV (.csv) - delimitado por vírgula
✓ JSON (.json) - estruturado
✓ XML (.xml) - hierárquico
✓ SQLite (.db) - banco de dados completo
✓ Texto (.txt) - simples
✓ Opções: apenas colunas visíveis, apenas filtros ativos, apenas seleção

MONITORAMENTO DE DESEMPENHO
----------------------------
✓ Uso de CPU em tempo real
✓ Uso de RAM em tempo real
✓ I/O de disco (leitura/escrita por segundo)
✓ Múltiplos discos suportados
✓ Gráficos destacáveis (detach)
✓ Atualização configurável (intervalo)
✓ Tema claro/escuro sincronizado com sistema

VISUALIZAÇÃO DE ESTRUTURA
--------------------------
✓ Árvore de diretórios navegável
✓ Operações: copiar, colar, recortar, excluir, renomear
✓ Criação de novas pastas/arquivos
✓ Menu de contexto completo
✓ Atalhos de teclado (Ctrl+C, Ctrl+V, Del, F2)
✓ Abertura de arquivos no aplicativo padrão
✓ Sincronização com eventos de monitoramento

INTERNACIONALIZAÇÃO
--------------------
✓ 6 idiomas suportados
✓ Tradução completa de interface
✓ Tradução de metadados
✓ Tradução de tipos de operação
✓ Mudança de idioma em tempo real (sem restart)
✓ Persistência de preferência de idioma
✓ Fallback para inglês quando tradução não disponível

PERSONALIZAÇÃO
--------------
✓ Cores configuráveis por tipo de operação
✓ Colunas visíveis configuráveis
✓ Colunas coloridas configuráveis
✓ Ordenação de linhas ativável
✓ Opções de exportação personalizáveis
✓ Tema claro/escuro automático
✓ Persistência de todas as configurações

═══════════════════════════════════════════════════════════════════════════════
## BOAS PRÁTICAS IMPLEMENTADAS
═══════════════════════════════════════════════════════════════════════════════

CÓDIGO LIMPO (Clean Code)
--------------------------
✓ Nomes descritivos e autoexplicativos
✓ Funções pequenas e focadas (< 50 linhas)
✓ Evitar números mágicos (usar constantes)
✓ Comentários apenas quando necessário
✓ Documentação no código (docstrings)
✓ Formatação consistente
✓ Evitar duplicação de código (DRY)

PRINCÍPIOS SOLID
----------------
✓ Single Responsibility Principle (SRP)
✓ Open/Closed Principle (OCP)
✓ Liskov Substitution Principle (LSP)
✓ Interface Segregation Principle (ISP)
✓ Dependency Inversion Principle (DIP)

TESTES E QUALIDADE
-------------------
✓ Try-except em todas operações críticas
✓ Logging detalhado em múltiplos níveis
✓ Validação de entrada de dados
✓ Verificação de estados antes de operações
✓ Graceful degradation
✓ Mensagens de erro amigáveis

PERFORMANCE
-----------
✓ Lazy loading de metadados
✓ Cache de resultados frequentes
✓ Processamento assíncrono
✓ Batch processing
✓ Índices otimizados no banco
✓ Uso eficiente de memória

MANUTENIBILIDADE
----------------
✓ Modularização extrema (200+ módulos)
✓ Separação de responsabilidades
✓ Baixo acoplamento
✓ Alta coesão
✓ Padrões de nomenclatura consistentes
✓ Estrutura de diretórios lógica

═══════════════════════════════════════════════════════════════════════════════
## INICIALIZAÇÃO E PONTO DE ENTRADA
═══════════════════════════════════════════════════════════════════════════════

📄 source/src_01_InicializadorMain.py
│
├── _ajustar_cwd()                        → Ajustar diretório de trabalho
│   • Detecta se está empacotado (PyInstaller)
│   • Define CWD para localização do executável
│   • Fallback para diretório do script
│
├── _definir_appusermodelid()             → Define ID do app no Windows
│   • Permite ícone personalizado na taskbar
│   • Agrupa janelas do mesmo app
│   • Compatível com Windows 7+
│
└── iniciar_aplicacao()                   → Função principal de entrada
    ├── Inicializa QApplication
    ├── Define ícone da aplicação
    ├── Configura sistema de traduções
    ├── Cria e exibe InterfaceMonitor
    ├── Inicia DatabaseWriter
    └── Retorna código de saída

FLUXO DE INICIALIZAÇÃO
----------------------
1. main.py chama iniciar_aplicacao()
2. Ajusta diretório de trabalho
3. Cria QApplication
4. Define AppUserModelID (Windows)
5. Carrega ícone da aplicação
6. Inicializa sistema de traduções
7. Carrega preferência de idioma
8. Cria janela principal (InterfaceMonitor)
9. Configura todos os componentes
10. Exibe janela
11. Entra no loop de eventos Qt
12. Retorna código de saída ao encerrar

═══════════════════════════════════════════════════════════════════════════════
## PONTOS DE ENTRADA E NAVEGAÇÃO
═══════════════════════════════════════════════════════════════════════════════

INICIALIZAÇÃO
-------------
main.py → src_01_InicializadorMain.py → InterfaceMonitor

COMPONENTES PRINCIPAIS
----------------------
GUI Principal:         gui/ic_01_InterfaceMonitor.py
Observador:            services/ob_01_Observador.py
Banco de Dados:        services/ob_02_BaseEvento.py
Metadados:             services/ob_09_GerenciadorColunas.py
Tabela:                services/ob_10_GerenciadorTabela.py
Estatísticas:          ui/ui_06_GerenciadorEstatisticasUI.py
Filtros:               tools/fil_01_Filtros.py
Traduções:             ui/ui_12_LocalizadorQt.py

PARA ADICIONAR NOVOS RECURSOS
------------------------------
• Novo tipo de gráfico: Herdar de data/GeradorEstatisticas/gst_01_base_gerador.py
• Novo tipo de evento: Herdar de services/ob_02_BaseEvento.py
• Nova coluna: Adicionar getter em services/ob_09_GerenciadorColunas.py
• Novo idioma: Criar linceu_XX.ts em source/locale/
• Novo filtro: Adicionar em tools/GerenciamentoAdministradorFiltros/

PARA REPORTAR BUGS OU CONTRIBUIR
---------------------------------
1. Verifique logs em: %APPDATA%/Linceu_Lighthouse/logs/
2. Consulte documentação em: docs/ (se disponível)
3. Entre em contato: [informações de contato]

═══════════════════════════════════════════════════════════════════════════════
## ESTRUTURA DE DEPENDÊNCIAS
═══════════════════════════════════════════════════════════════════════════════

DEPENDÊNCIAS DE ALTO NÍVEL
---------------------------
InterfaceMonitor (GUI Principal)
    ├─> Inicializador (Setup inicial)
    ├─> Configurador (Layouts e widgets)
    ├─> GerenciadorMenusUI (Menus e ações)
    ├─> GerenciadorBotoes (Ações de botões)
    ├─> GerenciadorEventosUI (Handlers de eventos)
    ├─> GerenciadorTabela (Operações de tabela)
    ├─> GerenciadorEstatisticasUI (Visualização de dados)
    ├─> LocalizadorQt (Traduções)
    ├─> Observador (Monitoramento)
    │   ├─> BaseEvento (Eventos base)
    │   ├─> EventoAdicionado
    │   ├─> EventoExcluido
    │   ├─> EventoModificado
    │   ├─> EventoRenomeado
    │   ├─> EventoMovido
    │   ├─> DiretorioScanner
    │   └─> GerenciadorColunas
    └─> DatabaseWriter (Escrita assíncrona)

DEPENDÊNCIAS DE METADADOS
--------------------------
GerenciadorColunas
    └─> 47 Módulos de Extração de Metadados
        ├─> Código-fonte (Python, JS, C++, etc.)
        ├─> Imagens (JPEG, PNG, BMP, PSD, etc.)
        ├─> Áudio (MP3, FLAC, WAV, etc.)
        ├─> Vídeo (MP4, MKV, AVI, etc.)
        ├─> Documentos (PDF, DOCX, TXT, etc.)
        ├─> Planilhas (XLSX, CSV, XLS, etc.)
        ├─> Apresentações (PPTX, PPT, etc.)
        ├─> Compactados (ZIP, RAR, 7Z, etc.)
        ├─> Bancos de dados (SQLite, Access, etc.)
        ├─> Executáveis (EXE, DLL, etc.)
        ├─> Temporários (TMP, TEMP, etc.)
        ├─> Backup (BAK, OLD, etc.)
        ├─> Log (LOG, TXT, etc.)
        └─> Configuração (INI, CFG, JSON, etc.)

DEPENDÊNCIAS DE VISUALIZAÇÃO
-----------------------------
GerenciadorEstatisticasUI
    └─> GeradorEstatisticas
        ├─> 18 Tipos de Gráficos
        │   ├─> Pizza
        │   ├─> Barras
        │   ├─> Timeline
        │   ├─> Treemap
        │   ├─> Histograma
        │   ├─> Pareto
        │   ├─> Linha
        │   ├─> Boxplot
        │   ├─> Radar
        │   ├─> Heatmap
        │   ├─> Scatter
        │   ├─> Sankey (3 variações)
        │   ├─> Dotplot
        │   └─> Árvore de Diretórios
        └─> Matplotlib/Seaborn/Plotly

═══════════════════════════════════════════════════════════════════════════════
## CONSIDERAÇÕES FINAIS
═══════════════════════════════════════════════════════════════════════════════

MODULARIDADE EXTREMA
--------------------
O projeto possui mais de 200 módulos especializados, cada um com uma
responsabilidade única e bem definida. Esta abordagem facilita:
• Manutenção e depuração
• Testes unitários
• Extensibilidade
• Reutilização de código
• Trabalho em equipe

PERFORMANCE E ESCALABILIDADE
-----------------------------
O sistema foi projetado para lidar com milhares de eventos por segundo:
• Thread dedicada para escrita no banco (DatabaseWriter)
• Processamento assíncrono de metadados
• Cache inteligente com invalidação seletiva
• Batch processing para operações massivas
• Debouncing para eventos frequentes
• Pool de threads para operações paralelas

INTERNACIONALIZAÇÃO COMPLETA
-----------------------------
Suporte nativo a 6 idiomas com tradução completa de:
• Interface de usuário
• Mensagens de erro
• Tooltips e hints
• Tipos de operação
• Metadados de arquivos
• Tipos de arquivo
• Atributos de arquivo

OBSERVAÇÕES IMPORTANTES
------------------------
• Versões específicas de bibliotecas devem ser mantidas:
  - futures==3.0.5
  - kaleido==0.2.1
  - plotly==5.22.0

• O sistema foi projetado especificamente para Windows 10/11

• Requer Python 3.10+ para compatibilidade total

• Banco de dados SQLite com otimizações WAL para melhor performance

• Sistema de logs com rotação automática em %APPDATA%/Linceu_Lighthouse/logs/

ESTRUTURA DE ARQUIVOS CRÍTICOS
-------------------------------
• monitoramento.db: Banco de dados principal (SQLite)
• language_config.json: Preferência de idioma
• colunas_coloridas.json: Configuração de cores
• cores_operacoes.json: Cores por tipo de operação
• config.json: Configurações gerais

Para informações detalhadas sobre cada módulo, consulte os comentários
inline no código-fonte correspondente.

═══════════════════════════════════════════════════════════════════════════════
## NOTAS FINAIS
═══════════════════════════════════════════════════════════════════════════════

Este projeto demonstra arquitetura modular bem planejada, seguindo princípios
SOLID e padrões de design estabelecidos. A separação clara entre camadas
(GUI, Services, UI, Data, Tools, Utils) facilita manutenção e extensibilidade.

O uso intensivo de threads e processamento assíncrono garante interface
responsiva mesmo durante operações pesadas. O sistema de internacionalização
completo torna a aplicação acessível a usuários de diferentes idiomas.

Para mais informações, consulte a documentação específica de cada módulo.

# Manter as Bibliotecas abaixo, nas seguintes versões:
# futures 3.0.5
# kaleido 0.2.1
# plotly 5.22.0
