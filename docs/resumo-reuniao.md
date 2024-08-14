# Resumo da Reunião

## Contexto
A Algar possui uma ferramenta desenvolvida pela equipe do Alan há cerca de 2-3 anos, com o objetivo de oferecer controle parental baseado em DNS para seus clientes. Essa ferramenta, inicialmente inovadora, apresenta agora várias falhas, como a interrupção frequente a cada 90 dias devido à mudança de senhas, além de problemas de coleta de dados e armazenamento de relatórios.

## Problemas Identificados
1. **Interrupção Frequente**: A aplicação para de funcionar a cada 90 dias devido à mudança de senhas de administração.
2. **Falhas na Coleta de Dados**: Existem problemas na coleta das variáveis e no tempo de espera, o que resulta em PDFs incorretos.
3. **Armazenamento Inadequado**: Os PDFs gerados não estão sendo armazenados, e a Anatel exige que pelo menos os últimos 90 dias de relatórios estejam disponíveis.
4. **Monitoramento e Automação Insuficientes**: Não há monitoramento adequado para garantir que todos os relatórios sejam gerados e enviados corretamente. Também falta automação no processo de renovação de senhas.

## Soluções Propostas
1. **Reconstrução da Ferramenta**: Desenvolver a ferramenta do zero, com foco em eficiência e cobertura das necessidades da Algar.
2. **Armazenamento e Backup**: Implementar um sistema de armazenamento seguro para os relatórios, garantindo que os últimos 90 dias estejam sempre disponíveis.
3. **Monitoramento Robusto**: Adicionar um monitoramento que verifique a geração e envio de relatórios, além de um sistema de notificação para falhas.
4. **Automatização do Processo**: Criar automações para evitar a necessidade de intervenção manual, como a renovação de senhas.

## Próximos Passos
- **Análise das APIs Existentes**: Verificar as APIs já utilizadas e identificar possíveis melhorias.
- **Desenvolvimento de Monitoramento**: Implementar um sistema de monitoramento para acompanhar o funcionamento da aplicação e o envio dos relatórios.
- **Consulta ao Alan**: Verificar com Alan os detalhes sobre o que foi desenvolvido e identificar áreas que precisam ser refinadas ou corrigidas.
- **Comunicação Contínua**: Manter uma comunicação ativa, possivelmente através de um grupo no Google Chat, para atualizações e colaboração contínua.

## Prioridade
Devido à criticidade do contrato com a Algar, avaliado em 4 milhões por ano, a prioridade é total para garantir a renovação do contrato e a conformidade com os requisitos da Anatel.

