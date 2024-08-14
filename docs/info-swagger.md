# Integração com API do Akamai

Este documento fornece detalhes sobre como integrar a API do Akamai no projeto existente. As informações foram extraídas do arquivo Swagger fornecido, que descreve os endpoints, parâmetros, e os modelos de dados utilizados pela API.

## Informações Gerais

- **Título da API**: Akamai Subscriber Services Manager
- **Versão da API**: 18.2.4.0 (build 202227)
- **Host da API**: `20200212era.eanuncia.demo.delivery:9090`
- **Base Path**: `/`

## Endpoints Principais

### Gerenciamento de Contas

1. **Get Account**
   - **Descrição**: Retorna serviços e detalhes do assinante.
   - **Método**: `GET`
   - **URL**: `/account/{subscriberId}`
   - **Parâmetros**:
     - `subscriberId` (path): ID do assinante (obrigatório).
   - **Resposta**: Detalhes da conta e dos serviços associados ao assinante.

2. **Delete Account**
   - **Descrição**: Deleta a conta de um assinante.
   - **Método**: `DELETE`
   - **URL**: `/account/{subscriberId}`
   - **Parâmetros**:
     - `subscriberId` (path): ID do assinante (obrigatório).
   - **Resposta**: Código de status HTTP indicando o sucesso ou falha da operação.

### Gerenciamento de Serviços de Assinantes

1. **Get Subscriber Service Info**
   - **Descrição**: Obtém informações sobre os serviços associados ao assinante.
   - **Método**: `GET`
   - **URL**: `/control/{subscriberId}`
   - **Parâmetros**:
     - `subscriberId` (path): ID do assinante (obrigatório).
   - **Resposta**: Informações detalhadas dos serviços do assinante.

2. **Activate Service**
   - **Descrição**: Ativa um serviço para um assinante.
   - **Método**: `POST`
   - **URL**: `/control/{subscriberId}/service`
   - **Parâmetros**:
     - `subscriberId` (path): ID do assinante (obrigatório).
     - `request` (body): Dados para ativar o serviço.
   - **Resposta**: Confirmação de que o serviço foi ativado com sucesso.

### Gerenciamento de Segurança

1. **Get Threat List**
   - **Descrição**: Retorna todas as ameaças dos servidores de feed Nominum.
   - **Método**: `GET`
   - **URL**: `/threat`
   - **Parâmetros**:
     - `locale` (query): Localização (opcional).
   - **Resposta**: Lista de ameaças conhecidas.

2. **Get Specific Threat**
   - **Descrição**: Retorna uma ameaça específica pelo seu ID.
   - **Método**: `GET`
   - **URL**: `/threat/{threatId}`
   - **Parâmetros**:
     - `threatId` (path): ID da ameaça (obrigatório).
     - `locale` (query): Localização (opcional).
   - **Resposta**: Detalhes da ameaça específica.

## Modelos de Dados Importantes

### Account
- **Descrição**: Representa uma conta de assinante.
- **Propriedades**:
  - `id`: ID da conta.
  - `https-termination`: Status do serviço de terminação HTTPS.
  - `personal-internet`: Status do serviço de Internet pessoal.
  - `secure-business`: Status do serviço de negócios seguros.
  - `subscriber-safety`: Status do serviço de segurança do assinante.
  - `time-zone`: Fuso horário associado à conta.

### ActivateServiceRequest
- **Descrição**: Dados necessários para ativar um serviço para um assinante.
- **Propriedades**:
  - `service`: Nome do serviço a ser ativado.
  - `service-profile`: Perfil de serviço a ser utilizado.
  - `time-zone`: Fuso horário para o serviço.

### ThreatCategoryDTO
- **Descrição**: Detalhes de uma categoria de ameaça.
- **Propriedades**:
  - `id`: ID da categoria de ameaça.
  - `name`: Nome da categoria de ameaça.
  - `description`: Descrição da ameaça.
  - `localized`: Indica se a descrição está localizada.
  - `source`: Fonte da ameaça.

## Passos para Integração

1. **Implementação dos Endpoints**:
   - Mapear os endpoints da API do Akamai no projeto existente.
   - Criar funções que façam chamadas HTTP para os endpoints descritos.

2. **Autenticação e Segurança**:
   - Garantir que as requisições à API do Akamai incluam as credenciais de autenticação necessárias.

3. **Transformação de Dados**:
   - Implementar a transformação dos dados recebidos da API do Akamai para o formato utilizado pelo sistema existente.

4. **Manutenção e Monitoramento**:
   - Implementar logs e monitoramento para garantir que a integração funcione corretamente e para detectar possíveis falhas de comunicação com a API do Akamai.
---
---