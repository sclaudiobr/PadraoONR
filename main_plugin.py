# -*- coding: utf-8 -*-
"""
PadraoONR - Plugin QGIS para padronização de campos ONR
"""

import os
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QProgressDialog
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant, Qt, QCoreApplication
from qgis.core import QgsField, QgsVectorLayer, QgsMessageLog, Qgis

class PadraoONR:
    """Plugin principal para padronização de campos ONR"""
    
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        
    def tr(self, message):
        return QCoreApplication.translate('PadraoONR', message)
    
    def initGui(self):
        """Inicializa a interface do plugin"""
        # Caminho do ícone
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        
        # Verifica se o ícone existe
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            # Usa ícone padrão do QGIS se não encontrar
            icon = QIcon()
        
        # Cria ação principal
        self.action = QAction(icon, "Padronizar Campos ONR", self.iface.mainWindow())
        self.action.triggered.connect(self.executar)
        self.action.setStatusTip("Padroniza campos no padrão ONR")
        
        # Adiciona ao menu Vector
        self.iface.addPluginToMenu("ONR", self.action)
        
        # Adiciona à barra de ferramentas
        self.iface.addToolBarIcon(self.action)
        
        self.actions.append(self.action)
    
    def unload(self):
        """Remove o plugin da interface"""
        for action in self.actions:
            self.iface.removePluginMenu("ONR", action)
            self.iface.removeToolBarIcon(action)
    
    def executar(self):
        """Função principal de execução"""
        # Obtém camada ativa
        layer = self.iface.activeLayer()
        
        if not layer:
            QMessageBox.warning(
                self.iface.mainWindow(),
                "PadraoONR",
                "Nenhuma camada selecionada!\nSelecione uma camada vetorial."
            )
            return
        
        if not isinstance(layer, QgsVectorLayer):
            QMessageBox.warning(
                self.iface.mainWindow(),
                "PadraoONR", 
                "A camada selecionada não é vetorial!\nSelecione um shapefile ou camada vetorial."
            )
            return
        
        # Confirmação
        resposta = QMessageBox.question(
            self.iface.mainWindow(),
            "PadraoONR - Confirmação",
            f"Deseja padronizar os campos da camada '{layer.name()}'?\n\n"
            "⚠️ ATENÇÃO: Todos os campos existentes serão removidos e\n"
            "substituídos pelos campos padrão ONR.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta != QMessageBox.Yes:
            return
        
        try:
            # Diálogo de progresso
            progress = QProgressDialog(
                "Padronizando campos ONR...",
                "Cancelar",
                0, 100,
                self.iface.mainWindow()
            )
            progress.setWindowTitle("PadraoONR")
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            
            # 1. Iniciar edição
            progress.setLabelText("Iniciando edição...")
            if not layer.startEditing():
                raise Exception("Não foi possível iniciar a edição")
            
            progress.setValue(10)
            
            # 2. Remover campos existentes
            progress.setLabelText("Removendo campos existentes...")
            provider = layer.dataProvider()
            
            # Verifica se há features
            if layer.featureCount() > 0:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    "Aviso",
                    f"A camada possui {layer.featureCount()} registros.\n"
                    "Certifique-se de ter feito backup dos dados!"
                )
            
            # Remove todos os campos
            campos_para_remover = list(range(len(layer.fields())))
            if campos_para_remover:
                if not provider.deleteAttributes(campos_para_remover):
                    raise Exception("Falha ao remover campos existentes")
            
            layer.updateFields()
            progress.setValue(30)
            
            # 3. Definir campos ONR
            progress.setLabelText("Definindo campos ONR...")
            campos_onr = {
                # Identificação
                'MATRICULA': QVariant.String,      # Número da matrícula
                'DAT_MAT': QVariant.String,        # Data da matrícula
                'LIV_MAT': QVariant.Int,           # Livro da matrícula
                'FOL_MAT': QVariant.Int,           # Folha da matrícula
                'TRANSCRI': QVariant.String,       # Transcrição
                
                # Localização
                'CNM': QVariant.String,            # Código do município
                'CNS': QVariant.String,            # Código da situação
                'ENDERECO': QVariant.String,       # Endereço
                'NUMERO': QVariant.Int,            # Número
                'CEP': QVariant.String,            # CEP (alterado para String)
                'MUNICIPIO': QVariant.String,      # Município
                'UF': QVariant.String,             # UF
                
                # Titularidade
                'NOME_TIT': QVariant.String,       # Nome do titular
                'CPF_CNPJ': QVariant.String,       # CPF/CNPJ
                'REL_JUR': QVariant.String,        # Relação jurídica
                'DAT_INI': QVariant.String,        # Data início
                'DAT_FIM': QVariant.String,        # Data fim
                'PER_REL': QVariant.Int,           # Percentual relação
                
                # Imóvel
                'NOME_IMO': QVariant.String,       # Nome do imóvel
                'AREA_HA': QVariant.Double,        # Área em hectares
                'AREA_M2': QVariant.Double,        # Área em m²
                'PER_M': QVariant.Double,          # Perímetro em metros
                'PER_KM': QVariant.Double,         # Perímetro em km
                
                # Confrontações
                'CONF_MAT': QVariant.String,       # Confrontação matrícula
                'CONF_NOME': QVariant.String,      # Confrontação nome
                
                # Certificações
                'CCIR_SNCR': QVariant.String,      # CCIR/SNCR
                'SIGEF': QVariant.String,          # SIGEF
                'SNCI': QVariant.String,           # SNCI
                'CIB_NIRF': QVariant.String,       # CIB/NIRF
                
                # Tributação
                'ITBI': QVariant.Double,           # ITBI
                
                # Outros
                'CAR': QVariant.String,            # CAR
                'RIP': QVariant.Int,               # RIP
                'CIF': QVariant.Int                # CIF
            }
            
            # 4. Adicionar novos campos
            progress.setLabelText("Adicionando novos campos...")
            novos_campos = []
            
            for nome, tipo in campos_onr.items():
                if tipo == QVariant.Double:
                    campo = QgsField(nome, tipo, len=15, prec=6)
                elif tipo == QVariant.String:
                    campo = QgsField(nome, tipo, len=254)
                elif tipo == QVariant.Int:
                    campo = QgsField(nome, tipo, len=10)
                else:
                    campo = QgsField(nome, tipo)
                
                novos_campos.append(campo)
            
            progress.setValue(50)
            
            if not provider.addAttributes(novos_campos):
                raise Exception("Falha ao adicionar novos campos")
            
            layer.updateFields()
            progress.setValue(70)
            
            # 5. Salvar alterações
            progress.setLabelText("Salvando alterações...")
            if not layer.commitChanges():
                raise Exception("Falha ao salvar alterações")
            
            progress.setValue(100)
            progress.close()
            
            # Mensagem de sucesso
            QMessageBox.information(
                self.iface.mainWindow(),
                "PadraoONR - Sucesso",
                f"✅ Campos padronizados com sucesso!\n\n"
                f"Camada: {layer.name()}\n"
                f"Campos adicionados: {len(novos_campos)}\n\n"
                f"A tabela de atributos será aberta..."
            )
            
            # Abre tabela de atributos
            self.iface.showAttributeTable(layer)
            
            # Log
            QgsMessageLog.logMessage(
                f"Campos ONR padronizados na camada: {layer.name()}",
                "PadraoONR",
                Qgis.Info
            )
            
        except Exception as e:
            # Rollback em caso de erro
            if layer.isEditable():
                layer.rollBack()
            
            # Fecha progresso
            if 'progress' in locals():
                progress.close()
            
            # Mensagem de erro
            QMessageBox.critical(
                self.iface.mainWindow(),
                "PadraoONR - Erro",
                f"❌ Ocorreu um erro:\n\n{str(e)}"
            )
            
            # Log de erro
            QgsMessageLog.logMessage(
                f"Erro no PadraoONR: {str(e)}",
                "PadraoONR",
                Qgis.Critical
            )