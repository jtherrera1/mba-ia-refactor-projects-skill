# Entregável - Desafio 03: Refatoração com IA

---

## A) Análise Manual

### 1. Projeto code-smells-project

#### 1.1. Classificação Critical

* No módulo [models.py](http://models.py) tem várias consultas, qualquer chamada pode injetar SQL arbitrário, permitindo extração de dados, exclusão de dados ou comprometimento total do banco de dados
* Senhas/chaves escritas diretamente no código-fonte
* Ainda retornado as credenciais na rota http://localhost:5000/health

#### 1.2. Classificação Alta
* São apagados dados das tabelas sem nenhuma restrição
* No [models.py](http://models.py), se abre um novo cursor para cada item achado do usuário, se recomenda criar só uma consulta para pegar o detalhe dos pedidos

#### 1.3. Classificação Média

* Regras de negócio de criação e atualização de produto espalhada
* As rotas chamam os models diretamente, acoplamento forte

#### 1.4. Classificação Baixa

* Seria bom usar ferramentas de logging no lugar de usar print
* Tem algumas conctenações usando str

---

### 2. Projeto ecommerce-api-legacy


#### 2.1. Classificação Critical

* Credentials estão hardcode
* Criação de senhas não usa um padrão seguro, função badCrypto
* O cache cresce sempre e não tem TTL


#### 2.2. Classificação Alta

* AppManager tem muitas responsabilidades
* Em algumas consultas pode ser aplicar Joins para melhorar a performance do processo
* As operações de apagar usuários deixa informações inconsistentes no projeto

#### 2.3. Classificação Média

* Expõe dados sensíveis de cartão dos usuários
* Regras negócio sem documentar para PAID e DENIED, talvez usar algum arquivo para padronizar o fluxo

#### 2.4. Classificação Baixa

* Dar mais informação dos erros nos logs
* Nomes pouco descriptivos "u", "e", "p", "cc"  no AppManager

---

### 3. Projeto task-manager-api

#### 3.1. Classificação Critical

* Tem algumas credenciais declaradas no código
* Expõe informações sensíveis do usuário como o password


#### 3.2. Classificação Alta

* Criação da password bem fraca
* Muita responsabilidade nas rotas
* O banco pode validar algumas propriedades das tasks em SQL sem precisar ser feito no código de forma hard para "overdue" e "status"

#### 3.3. Classificação Media

* Falta de paginação dependendo do tamanho pode ser necessário
* Não explora o banco para aplicar algumas remoções em cascata

#### 3.4. Classificação Baixa

* Algumas serializações poderia ser usando dict
* Algumas classes não são chamadas
* Falta de alguns padrões de formatação e qualidade de código

---

## B) Construção da Skill

### 1. Abordagem

Anti-patterns são abstratos e podem reconhecer qualquer linguagem de programação e tecnologia.

No caso das heurísticas, acho que até daria para deixar por linguagem e tecnologia. Identificar framework, banco de dados precisam ser especializados e para garantir a precisão para detectar cada artefato.

### 2. Processo de Construção

Comecei fazendo em "Github Copilot", e comecei a construção olhando primeiro o código dos projetos, e populando as referências. Influencia muito a completude da descrição e objetivo, fui descrevendo as fases de forma independente e ligação das referências como indica a ajuda do GitHub Copilot:

[https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

### 3. Anti-patterns Escolhidos

![](images/image16.png)


### 4. Lista Anti-Patterns alterada depois do feedback
Adição do anti-pattern "Deprecated/Obsolete APIs"

![](images/nova-lista-anti-pattern.png)


---

## C) Resultados

* De forma geral, a skill identifica de forma afetiva anti-patterns independente da linguagem de programação
* Em projetos dentro de uma empresa eu aplicaria por projeto, e especializaria a skill por linguagem
* Estratégias também deveriam ser espcializadas por linguagem, neste caso resolvi deixar junto por conveniência.
* O Playbook de anti-patterns é rico reutilizável, da para levar e usar em diferentes projetos
* A experência de aplicar em diferentes contextos ajuda a refletir como pode de fato levar a experência de problemas recorrentes de um projeto para outro, mesmo assim precisa especializar.
* Validações e evidências dos projetos funcionando, e checklist por projeto 

### Resumo por projeto


| Projeto  | Stack | Anti-patterns encontrados         |
|--------|--------|----------------|
| code-smells-project   | Python/Flask    | 13       |
| ecommerce-api-legacy  | Node.js/Express     | 11      |
| task-manager-api |Python/Flask   | 11 |


### 1. Projeto code-smells-project

#### 1.1. Antes da Refatoração

* Imagens com dados sensíveis dos usuário exposto
* Endpoints funcionando 
* Login quebrado
* Instalação do projeto e validação de endpoints

![](images/image7.png)
![](images/image4.png)
![](images/image17.png)
![](images/image3.png)
![](images/image1.png)

##### Estrutura do projeto (antes)

```txt
── code-smells-project/
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   ├── README.md
│   ├── loja.db
```

#### 1.2. Depois da Refatoração

* Validando as funcionalidade esperadas

![](images/image1.png)

---

### 2. Projeto ecommerce-api-legacy

#### 2.1. Antes da Refatoração

* Imagens com dados sensíveis dos usuário exposto
* Endpoints funcionando 
* Mostrando inconsistência de dados do Delete ao apagar um usuário com histórico de compara
* Sem uso de autorização para ver dados financieros
* Instalação do projeto e validação de endpoints


![](images/image11.png)
![](images/image9.png)
![](images/image13.png)

##### Estrutura do projeto (antes)

```txt
── ecommerce-api-legacy/
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   ├── utils.js
│   ├── api.http
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
```

#### 2.2. Depois da Refatoração

* Validando asas funcionalidade esperadas
* Validando autorização para ver dados financieros


![](images/image12.png)
![](images/image5.png)

---

### 3. Projeto task-manager-api

#### 3.1. Antes da Refatoração

* Endpoints funcionando 
* Instalação do projeto e validação de endpoints


![](images/image10.png)
![](images/image14.png)

##### Estrutura do projeto (antes)

```txt
── task-manager-api/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── task.py
│   │   ├── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── report_routes.py
│   │   ├── task_routes.py
│   │   ├── user_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── notification_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   ├── app.py
│   ├── database.py
│   ├── README.md
│   ├── requirements.txt
│   ├── seed.py
```

#### 3.2. Depois da Refatoração
* Validando as funcionalidade esperadas

![](images/image15.png)
![](images/image14.png)

---

### 4. Checklist de Validação (Phase 3)


#### 4.1. code-smells-project

![](images/code-smells-project.png)

#### 4.2. ecommerce-api-legacy

![](images/ecommerce-api-legacy.png)

#### 4.3. task-manager-api

![](images/task-manager-api.png)

---

### 5. Feedback - Resultado Phase 3

Precisiei rodar mais uma vez a skills para todos os projetos, assim evidenciar o comportamento com a mudanda de um novo anti-pattern. 

#### 5.1. code-smells-project

![](images/cs-ph3.png)

#### 5.2. ecommerce-api-legacy

![](images/eal-ph3.png)

#### 5.3. task-manager-api

![](images/tma-ph3.png)

---

## D) Como Executar


### 1. Github Copilot

No Copilot se adiciona as skills no path:
`.github/skills/<nome-skill>/SKILL.md`

Para executar, só chamar ele no chat:

![](images/image6.png)

### 2. Claude Code

#### 2.1. Execução

![](images/claude-code1.png)

#### 2.2. Uso de Créditos

![](images/claude-code2.png)


### 3. Skill funcionou
* Se apresenta na seção C de resultadaos as evidências antes e depois da refatoração
* Imagens da execução da faser 3 são apresentadas por projeto, na sub-seção 3 da Seção C de resultados
