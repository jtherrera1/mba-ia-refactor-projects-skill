================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy (Frankenstein LMS)
Stack:   JavaScript (Node.js) + Express 4.18.2
Files:   3 analyzed | ~180 lines of code

Summary
CRITICAL: 4 | HIGH: 4 | MEDIUM: 2 | LOW: 1

Findings

[CRITICAL] God Class
File: src/AppManager.js:1-141
Description: A classe AppManager centraliza em um único arquivo a inicialização
             do banco de dados, definição de rotas, lógica de negócio (checkout,
             matrícula, pagamento, auditoria) e acesso a dados — violação total
             do SRP e do padrão MVC.
Impact: Impossível testar em isolamento; qualquer mudança em uma responsabilidade
        afeta todas as demais; alta probabilidade de regressão.
Recommendation: Separar em camadas: UserRepository, CourseRepository,
                PaymentService, CheckoutController, routes/; aplicar SRP.

[CRITICAL] Hardcoded Secrets
File: src/utils.js:2-6
Description: Credenciais de banco de dados (dbUser, dbPass), chave de gateway de
             pagamento (paymentGatewayKey: "pk_live_1234567890abcdef") e usuário
             SMTP embutidos diretamente no código-fonte.
Impact: Credenciais expostas via repositório Git comprometem o ambiente de
        produção inteiro. Chave de pagamento vaza acesso financeiro crítico.
Recommendation: Mover todos os segredos para variáveis de ambiente (process.env)
                ou um Secret Manager; nunca versionar credenciais.

[CRITICAL] Plain Text Password / Broken Crypto
File: src/utils.js:17-23 | src/AppManager.js:18,68
Description: A função badCrypto usa base64 em loop (não é hashing) — base64 é
             reversível, não é seguro para senhas. O seed insere o usuário
             Leonan com senha '123' em texto puro. Qualquer dump do banco expõe
             todas as senhas.
Impact: Comprometimento total das credenciais de todos os usuários em caso de
        vazamento de banco de dados.
Recommendation: Substituir badCrypto por bcrypt ou argon2; aplicar salt único
                por usuário; nunca armazenar senhas reversíveis.

[CRITICAL] Broken Authentication
File: src/AppManager.js:80-129
Description: O endpoint GET /api/admin/financial-report é completamente público
             — qualquer cliente sem autenticação pode acessar dados financeiros
             de todos os cursos e alunos.
Impact: Exposição de dados sensíveis de receita e informações de estudantes
        para qualquer usuário não autenticado.
Recommendation: Implementar middleware de autenticação (JWT/session) e RBAC;
                proteger rotas /admin com requireRole('admin').

[HIGH] Callback Hell
File: src/AppManager.js:28-128
Description: Fluxo de checkout possui 5 níveis de callbacks aninhados (course →
             user → processPayment → enrollment → payment → audit_log). O
             financial-report possui 4 níveis (courses → enrollments → user →
             payment), tornando o fluxo ilegível e propenso a erros silenciosos.
Impact: Código extremamente difícil de debugar, manter e testar; erros em
        callbacks internos podem ser engolidos silenciosamente.
Recommendation: Promisificar a API do sqlite3 e reescrever com async/await;
                ou usar uma biblioteca como better-sqlite3 ou knex.

[HIGH] Global Mutable State
File: src/utils.js:9-10
Description: globalCache e totalRevenue são variáveis mutáveis no escopo do
             módulo, compartilhadas e modificadas por qualquer parte da aplicação
             que importe utils.js.
Impact: Comportamento imprevisível em concorrência; estado compartilhado torna
        testes impossíveis sem resetar o módulo; totalRevenue nunca é atualizado,
        tornando-o um dado fantasma.
Recommendation: Eliminar estado global; injetar dependências; usar cache
                localizado ou uma camada de serviço com estado encapsulado.

[HIGH] Fat Controller / No Service Layer
File: src/AppManager.js:28-137
Description: setupRoutes contém toda a lógica de negócio: criação de usuário,
             validação de cartão, processamento de pagamento, criação de matrícula
             e log de auditoria — tudo embutido diretamente no handler da rota.
Impact: Zero reuso; impossível chamar a lógica de checkout sem disparar uma
        requisição HTTP; impossível testar a regra de negócio isoladamente.
Recommendation: Extrair CheckoutService, PaymentService e EnrollmentService;
                controllers devem apenas orquestrar, não executar lógica.

[HIGH] Tight Coupling
File: src/AppManager.js:7 | src/app.js:8-9
Description: AppManager instancia sqlite3.Database(':memory:') diretamente no
             construtor sem injeção de dependência. app.js cria new AppManager()
             sem possibilidade de substituir a implementação do banco.
Impact: Impossível trocar o banco de dados ou usar um mock nos testes sem
        modificar a classe; alto acoplamento estrutural.
Recommendation: Injetar a instância do banco via construtor; criar uma camada
                de abstração (Repository Pattern) entre o domínio e o SQLite.

[MEDIUM] N+1 Query Problem
File: src/AppManager.js:88-128
Description: O financial-report executa: 1 query para listar cursos, depois para
             cada curso N queries para matrículas, e para cada matrícula 2 queries
             adicionais (usuário + pagamento) — total de 1 + N + 2*M queries onde
             N=cursos e M=total de matrículas.
Impact: Performance degrada exponencialmente com o crescimento dos dados;
        relatório com 10 cursos e 100 matrículas dispara ~211 queries.
Recommendation: Substituir por JOINs entre enrollments, users e payments;
                uma única query retorna todos os dados necessários.

[MEDIUM] Orphan Data
File: src/AppManager.js:131-136
Description: DELETE FROM users WHERE id = ? remove o usuário mas deixa registros
             órfãos nas tabelas enrollments e payments referenciando um user_id
             inexistente. O próprio response message admite: "as matrículas e
             pagamentos ficaram sujos no banco."
Impact: Inconsistência referencial; relatórios financeiros podem incluir dados
        de usuários deletados; violação de integridade do banco de dados.
Recommendation: Criar FOREIGN KEY com ON DELETE CASCADE nas tabelas dependentes;
                ou implementar soft delete com campo deleted_at.

[LOW] Print Logging (console.log em produção)
File: src/AppManager.js:45 | src/utils.js:13
Description: console.log é usado para logging de eventos de produção (processamento
             de cartão, cache) sem níveis de severidade, contexto estruturado
             ou destino configurável.
Impact: Logs sem nível, sem timestamp padronizado, sem contexto; dados sensíveis
        (número de cartão parcial) podem aparecer em logs de produção.
Recommendation: Adotar winston ou pino com níveis (info/warn/error), formato JSON
                estruturado e nunca logar dados de cartão/pagamento.

================================
Total: 11 findings
================================
