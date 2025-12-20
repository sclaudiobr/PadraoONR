## PadraoONR
[![N|Solid](https://github.com/sclaudiobr/PadraoONR/blob/main/icon.png)](https://github.com/sclaudiobr/PadraoONR)

### _Complemento QGIS para Geração Automática de Atributos em Shapefile_
#### Esta aplicação gera automaticamente campos de atributos da tabela em um shapefile, facilitando o preenchimento correto dos dados exigidos pelo sistema de Registro Digital de Imóveis - RGI Digital
# 1 - Instalação Manual
#### a) Faça o download do pacote
#### b) Abra o QGIS > Complementos> Instalar e Gerenciar Complementos > Instalar a patir do zip
#### c) Selecione o arquivo PadraoONR.zip
#### d) Instalar
# 2 - Uso
#### a) Abra ou crie um arquivo de polígono a área
#### b) Selecione a Camada desejada
#### c) Click na Ferramenta PadraoONR

## 3- Modelo de atributos

| CAMPO | TIPO | FORMATO/COMPRIMENTO | DESCRIÇÃO | EXEMPLO |
| ------ | ------ |------ | ------ |------ |
|MATRICULA|Alfanumérico|50 caracteres|Número da matrícula do imóvel|10001|
|DAT_MAT|Numérico|DD/MM/AAAA|Data da matrícula|02/06/2025|
|LIV_MAT|Numérico|5 dígitos|Livro da matrícula|2|
|FOL_MAT|Numérico|5 dígitos|Folha da matrícula|103|
|ATRANSCRI|Alfanumérico|100 caracteres|Número da transcrição do imóvel|TR987654|
|CNM|Numérico|000000.0.0000000-00|Código Nacional da Matrícula|123456.7.8901234-56|
|CNS|Alfanumérico|10 caracteres|Código Nacional da Serventia|000000|
|ENDERECO|Alfanumérico|200 caracteres|Endereço do imóvel|Rodovia BR 000, km 00|
|NUMERO|Numérico|10 dígitos|Número do imóvel|123|
|CEP|Numérico|8 dígitos|CEP rural do imóvel|01001000|
|MUNICIPIO|Alfanumérico|100 caracteres|Município onde o imóvel está localizado|São Paulo|
|UF|Alfanumérico|2 caracteres|Unidade da Federação (UF)|SP|
|NOME_TIT|Alfanumérico|150 caracteres|Nome(s) do(s) proprietário(s)|João Silva, Maria Souza|
|CPF_CNPJ|Numérico|18 caracteres|CPF ou CNPJ dos proprietários|000000000-00, 000000000-00|
|CONF_MAT|Numérico|50 caracteres|Números das matrículas confrontantes|10001,10010,210001|
|CONF_NOME|Alfanumérico|150 caracteres|Nomes dos confrontantes|Fulano, Sicrano, Beltrano|
|REL_JUR|Alfanumérico|50 caracteres|Tipo de relação jurídica|propriedade, usufruto, promessa c&v|
|DAT_INI|Numérico|DD/MM/AAAA|Data de início da relação jurídica|02/06/2024|
|DAT_FIM|Numérico|DD/MM/AAAA|Data de término da relação jurídica|02/06/2025|
|PER_REL|Numérico|6,2 (6 dígitos, 2 decimais)|Percentual da relação jurídica|33.33|

#### _Fonte_: Manauais de Uso 
https://mapa.onr.org.br/sigri/manual/manual-geracao-automatica-atributos-shapefile-script-python
