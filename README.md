# FOCAL — Plataforma de estudos para o ENEM

**Entrega consolidada (novembro/2026).** Site responsivo e estático, sem build ou instalação obrigatória. Visual preto/vermelho futurista, com ícones vetoriais (sem emojis).

## Abrir sem programar

- Arquivo único: abra `focal-completo.html` com dois cliques no Chrome ou Edge. Os dados, estilos e a aplicação estão embutidos no HTML. A maioria dos recursos funciona sem internet.
- Pacote completo: extraia o ZIP e abra `index.html`. Para publicar, envie a pasta a um serviço de hospedagem estática com HTTPS.
- Em hospedagem HTTPS, o pacote tem manifesto e service worker para cache dos arquivos essenciais, mas a consulta de sites externos continua exigindo conexão.

## Recursos disponíveis

- Questionário inicial e cronograma por nível (básico, intermediário, avançado), período (1–12 meses), dias por semana e duração diária.
- Painel de prioridades com incidência de conteúdos e sessões de estudos concluídas.
- **141 tópicos / 14 disciplinas**, cada um com uma orientação conceitual original, passos de revisão, vídeo por busca temática e notas salvas. 18 dos tópicos têm aprofundamento com exemplo resolvido e alerta de erro comum.
- **165 questões originais** com alternativas e gabarito: 78 exercícios de aplicação e 87 checagens conceituais introdutórias (checar a contagem sempre que acrescentar conteúdo). Não são questões oficiais do ENEM.
- Simulado configurável com escolha de área, quantidade, modo, gabarito comentado e histórico local. **Não calcula nota TRI.**
- **141 flashcards** com planejamento de revisão espaçada (um por tópico).
- Laboratório de redação: proposta de treino, redação em quatro partes, checklist inspirado nas cinco competências, salvamento e exportação em `.txt`. **Não atribui nota oficial nem automática.**
- Provas e gabaritos oficiais no portal do Inep, inclusive 2026; leitura de questões estruturadas via API comunitária `enem.dev` (2009–2023), se online. Filtros por ano/área; busca textual e sugestões por palavras-chave **não são classificação pedagógica validada por assunto**.
- Exportação e importação do progresso em arquivo `.json`: backup do cronograma, notas, respostas, redação, simulados e flashcards.
- Navegação responsiva; suporte a celular e desktop.

## Fontes e limites dos dados

- **SAS Educação — Raio-X ENEM 2026 (2009–2025):** https://prod-assets-saseducacao.s3.amazonaws.com/public/2026-04/RAIO-X_ENEM%20SAS.pdf?VersionId=1qwKGl_vetiOrP1ROPpo8oO823hRWGF9
- **Inep — Provas e gabaritos:** https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem/provas-e-gabaritos
- **Inep — Matriz de Referência:** https://www.gov.br/inep/pt-br/centrais-de-conteudo/acervo-linha-editorial/publicacoes-institucionais/avaliacoes-e-exames-da-educacao-basica/matrizes-de-referencia-enem/
- **API comunitária:** https://api.enem.dev/

Os números são contagens de ocorrências históricas por disciplina, não probabilidades de cair na próxima prova. O catálogo enfatiza tópicos mapeados no levantamento, não substitui a íntegra dos objetos de conhecimento da Matriz do Inep. Alguns exercícios de treino são básicos por intenção: preparam para o estilo contextualizado do ENEM, não reproduzem questões originais. Videos do YouTube são resultados de busca por tópico, não videoaulas revisadas individualmente. **Não há banco local integral de todas as questões oficiais categorizadas por assunto**, porque a classificação por subtema e a verificação editorial de cada item dependem de um trabalho adicional.

## Privacidade

Não existe cadastro nem backend próprios nesta entrega. Todas as respostas, rascunhos e configurações ficam no armazenamento local do navegador (localStorage). Usar outro aparelho ou limpar dados do site pode fazer o histórico desaparecer; faça backup pela tela "Meus dados". O arquivo JSON de backup contém informações que você escreveu; cuide dele como um arquivo pessoal.

## Estrutura do pacote

- `index.html`, `styles.css`, `data.js`, `app.js`: aplicação.
- `favicon.svg`, `icon-192.png`, `icon-512.png`, `manifest.webmanifest`, `sw.js`: identidade e instalação como PWA em hospedagem compatível.
- `catalogo-frequencias.csv`: catálogo de conteúdos e frequências.
- `README.md`: estas instruções.

Focal é um projeto independente, sem vínculo com Inep, MEC, SAS Educação ou YouTube.

## Atualização do acervo de questões (novembro de 2026)

A página **Questões oficiais do ENEM** tenta agora carregar primeiro o índice por imagens do repositório público independente `henriquedss0308-isa/questoes-enem`, com questões de 2017–2025 categorizadas por ano e disciplina. A classificação dos temas é comunitária e não foi validada pelo Focal; os enunciados são exibidos como imagens hospedadas externamente, que dependem de internet. As imagens não trazem correção comentada ou gabarito separado: consultar o gabarito no Inep. Para anos anteriores tenta a API `api.enem.dev`, que pode ser indisponível ou bloquear acesso pelo navegador. Caso ambos os serviços falhem, o banco de exercícios autorais permanece funcional, e o botão do Inep abre o PDF oficial. A URL externa é consumida apenas como JSON de um índice — nenhum código da fonte é executado.