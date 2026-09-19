# Ética, privacidade e vieses

## Decisão sobre dados pessoais

O Grupo 8 decidiu não associar localização, idade, sexo ou outros dados pessoais
às imagens e relatos utilizados na CardioAI. Essa ausência é intencional: reduz
risco de reidentificação e dificulta que o modelo use atributos demográficos como
atalhos no lugar de sinais clínicos.

Essa escolha não elimina todo viés. Ela impede, por exemplo, medir diretamente
diferenças de desempenho entre grupos de idade, sexo ou localização. Por isso, o
projeto não fará alegações de equidade demográfica.

## Avaliações possíveis nesta fase

- equilíbrio entre as classes `baixo_risco` e `alto_risco`;
- variedade de sintomas e construções linguísticas;
- falsos negativos de relatos de alto risco;
- dependência do modelo de palavras muito evidentes;
- relatos fora da cobertura da ontologia e do dataset.

## Limite de uso

O sistema é uma simulação acadêmica. Não deve orientar atendimento, substituir
profissionais de saúde nem ser aplicado a dados de pacientes sem validação
clínica, base legal, segurança e governança apropriadas.
