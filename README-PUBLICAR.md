# FOCAL HOSPEDADO — GitHub + Render (sem CORS)

Este pacote reúne o site Focal completo e uma API Python para consultar o arquivo SQLite público do projeto [ardotheedu/api-enem](https://github.com/ardotheedu/api-enem). Não usa `api.enem.dev` em tempo de execução.

## Publicar o site (sem escrever código)

1. Entre em https://github.com/new. Escolha `focal-enem`, repositório **Public**; crie-o.
2. Extraia este ZIP no computador. Dentro da pasta extraída, selecione os arquivos (incluindo `index.html`, `app.js`, `server.py`, `build.py` e `render.yaml`). No GitHub, use **Add file > Upload files** e envie **os arquivos para a raiz do repositório**, não o ZIP. Clique em **Commit changes**.
3. Entre em https://dashboard.render.com. Clique em **New > Blueprint**; conecte a sua conta do GitHub, selecione o repositório `focal-enem` e confira que o arquivo `render.yaml` foi detectado.
4. Clique em **Apply** ou **Deploy Blueprint** (o nome pode variar). O Render configurará um serviço web Python no plano Free com os comandos do `render.yaml`.
5. Na primeira implantação, o build fará o download do banco SQLite público; o site e a API passarão a ter o mesmo endereço HTTPS. O site terá URL `https://<nome>.onrender.com` definida no seu painel Render.
6. Para testar, abra `/health` (deve retornar `{"ok":true,"database":true}`), depois `/api/years` (lista de anos do banco) e `/api/questions?year=2023&area=mat` (resposta JSON). No site, vá a **Banco de questões > Questões oficiais** e selecione um ano disponível.

Você não precisa provisionar PostgreSQL, pagar uma API nem configurar CORS.

### Limites e transparência

- O banco de origem não necessariamente contém todos os anos, áreas, imagens ou questões do ENEM. O Focal mostra apenas **anos realmente presentes** no SQLite. O repositório de origem inclui questões de 2023; consulte `/api/years` para verificar a edição hospedada.
- Enunciados com imagens relativas podem exigir curadoria futura; nem todos os arquivos complementares estão no banco SQLite.
- O app continua guardando progresso no navegador (`localStorage`), não em contas de usuários. Mudanças de domínio/dispositivo não migram o histórico automaticamente; use o recurso de backup.
- O serviço gratuito Render pode hibernar após 15 minutos sem acesso, levando mais tempo para responder na primeira visita. O servidor não deve gravar alterações no banco do repositório. Dados de progresso locais não são afetados pela hibernação do serviço.
- A base SQLite é obtida do GitHub **durante cada build**. Caso o GitHub não esteja acessível no momento do deploy, a implantação falhará e o Render mostrará o erro nos logs; isso não é um problema de CORS.
- A licença do código do repositório `ardotheedu/api-enem` é MIT. A disponibilidade dos enunciados e das imagens no projeto não significa que as provas estejam licenciadas pela MIT; verifique os direitos antes de redistribuição comercial.

### Desenvolvimento no computador (opcional)

Instale Python 3.10+ e execute:

```bash
python build.py
python server.py
```

Abra http://localhost:10000.

### Rotas

- `GET /health` status do serviço
- `GET /api/years` lista de anos e total por ano
- `GET /api/questions?year=2023&area=mat` lista questões por ano e área
  - `area` aceita `mat`, `ling`, `nat`, `hum`; `limit` 1-200; `page` a partir de 1

### Créditos

- Focal: projeto independente, sem vínculo com Inep, MEC ou quaisquer provedores.
- SQLite de questões e inspiração para estrutura de respostas: [ardotheedu/api-enem](https://github.com/ardotheedu/api-enem), código sob MIT, arquivos de provas sujeitos a seus próprios direitos.
- Provas e gabaritos oficiais: [Inep](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem/provas-e-gabaritos).