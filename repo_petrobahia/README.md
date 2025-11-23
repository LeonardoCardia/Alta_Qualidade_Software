# Sistema de Gerenciamento de Pedidos PetroBahia

Um sistema profissional de gerenciamento de pedidos em Python seguindo os princípios SOLID e as melhores práticas da indústria.

## Índice

- [Visão Geral](#visão-geral)
- [Resumo da Refatoração](#resumo-da-refatoração)
- [Arquitetura](#arquitetura)
- [Implementação dos Princípios SOLID](#implementação-dos-princípios-solid)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Testes](#testes)

## Visão Geral

Este sistema fornece uma solução completa para gerenciar pedidos de clientes com cálculo automático de descontos baseado nos níveis de hierarquia dos clientes. A base de código foi completamente refatorada a partir de uma implementação legada para seguir os princípios SOLID, padrões de arquitetura limpa e práticas modernas de engenharia de software.

## Resumo da Refatoração

O projeto passou por uma refatoração arquitetural completa para resolver a dívida técnica e melhorar a manutenibilidade, testabilidade e extensibilidade. O código legado foi preservado no diretório `src/legacy/` para referência.

### Principais Melhorias

1. **Implementação de Arquitetura Limpa**
   - Separação de responsabilidades em camadas distintas: Domínio, Serviços, Infraestrutura e Casos de Uso
   - Eliminação do acoplamento forte entre componentes
   - Introdução de injeção de dependência para melhor testabilidade

2. **Aplicação dos Princípios SOLID**
   - Aplicação dos cinco princípios SOLID em toda a base de código
   - Criação de interfaces focadas e classes base abstratas
   - Implementação da inversão de dependência para todas as dependências entre camadas

3. **Melhoria da Qualidade do Código**
   - Integração de formatação automatizada com Black e isort
   - Adição de análise estática com Pylint (alcançando pontuação 9.93/10)
   - Implementação de testes unitários abrangentes com 76% de cobertura de código
   - Adição de type hints para melhor suporte da IDE e documentação

4. **Infraestrutura de Testes**
   - Criação de 75 testes unitários abrangentes usando pytest
   - Implementação de fixtures de teste e mocks para testes isolados
   - Adição de relatórios de cobertura de código com pytest-cov
   - Todos os testes passam com taxa de sucesso de 100%

## Arquitetura

O sistema segue um padrão de arquitetura em camadas:

```
┌─────────────────────────────────────┐
│      Camada de Casos de Uso         │  ← Regras de negócio da aplicação
├─────────────────────────────────────┤
│       Camada de Serviços            │  ← Implementação da lógica de negócio
├─────────────────────────────────────┤
│    Camada de Infraestrutura         │  ← Dependências externas
├─────────────────────────────────────┤
│       Camada de Domínio             │  ← Regras de negócio empresariais
└─────────────────────────────────────┘
```

### Responsabilidades das Camadas

**Camada de Domínio** (`src/domain/`)
- Contém as entidades de negócio principais (Client, Order, OrderItem)
- Define interfaces de repositórios e serviços
- Sem dependências de outras camadas

**Camada de Serviços** (`src/services/`)
- Implementa lógica de negócio para validação, descontos, impostos e email
- Depende apenas de abstrações do domínio
- Fornece componentes de negócio reutilizáveis

**Camada de Infraestrutura** (`src/infrastructure/`)
- Implementa mecanismos de persistência (repositórios baseados em arquivo)
- Gerencia dependências externas
- Implementações concretas das interfaces do domínio

**Camada de Casos de Uso** (`src/use_cases/`)
- Orquestra fluxos de trabalho de negócio
- Implementa regras de negócio específicas da aplicação
- Coordena entre serviços e repositórios

## Implementação dos Princípios SOLID

### Princípio da Responsabilidade Única (SRP)
Cada classe tem uma responsabilidade clara:
- `EmailValidator`: Valida apenas o formato de email
- `TaxCalculator`: Gerencia apenas cálculos de impostos
- `FileClientRepository`: Gerencia apenas a persistência de clientes

### Princípio Aberto/Fechado (OCP)
Classes são abertas para extensão mas fechadas para modificação:
- `TierDiscountCalculator` aceita taxas de desconto personalizadas sem modificação
- Novas estratégias de desconto podem ser adicionadas implementando a interface `DiscountCalculator`
- Novos níveis de cliente podem ser adicionados através de configuração

### Princípio da Substituição de Liskov (LSP)
Todas as implementações substituem adequadamente suas interfaces base:
- `FileClientRepository` implementa completamente a interface `ClientRepository`
- `ConsoleEmailService` pode ser substituído por qualquer implementação de `EmailSender`
- Todos os serviços respeitam seus contratos de interface

### Princípio da Segregação de Interface (ISP)
Interfaces são focadas e mínimas:
- `ClientReader` e `ClientWriter` são separados
- `EmailSender` tem um único método focado
- Serviços dependem apenas das interfaces que utilizam

### Princípio da Inversão de Dependência (DIP)
Módulos de alto nível dependem de abstrações:
- Casos de uso dependem de interfaces de serviços, não de implementações concretas
- Serviços são injetados através de construtores
- Fácil trocar implementações para teste ou produção

## Funcionalidades

### Funcionalidades de Negócio
- Registro de clientes com validação completa
- Prevenção de clientes duplicados (validação por email único)
- Sistema de desconto baseado em nível (Gold: 20%, Silver: 10%, Bronze: 5%)
- Descontos baseados em quantidade (10+ itens: 20%, 5-9 itens: 10%)
- Cálculo de impostos (taxa configurável)
- Processamento de pedidos com múltiplos itens
- Geração automatizada de resumo de pedidos

### Funcionalidades Técnicas
- Arquitetura limpa com clara separação de responsabilidades
- Cobertura abrangente de testes unitários (75 testes, 76% de cobertura)
- Formatação automatizada de código (Black, isort)
- Análise estática de código (Pylint)
- Type hints em toda a base de código
- Entidades de domínio imutáveis usando dataclasses
- Injeção de dependência para testabilidade

## Estrutura do Projeto

```
repo_petrobahia/
├── src/
│   ├── domain/                    # Entidades e interfaces de negócio principais
│   │   ├── entities.py           # Entidades Client, Order, OrderItem
│   │   ├── repositories.py       # Interfaces de repositório
│   │   └── services.py           # Interfaces de serviço
│   ├── services/                  # Implementações de lógica de negócio
│   │   ├── discount.py           # Serviços de cálculo de desconto
│   │   ├── email.py              # Serviços de email
│   │   ├── tax.py                # Serviço de cálculo de impostos
│   │   └── validation.py         # Serviços de validação
│   ├── infrastructure/            # Dependências externas
│   │   └── repositories.py       # Implementação de repositório baseado em arquivo
│   ├── use_cases/                 # Regras de negócio da aplicação
│   │   ├── client_management.py  # Caso de uso de registro de cliente
│   │   ├── order_processing.py   # Casos de uso de processamento de pedido
│   │   └── price_calculation.py  # Caso de uso de cálculo de preço
│   ├── main.py                    # Ponto de entrada da aplicação
│   └── legacy/                    # Código legado original (preservado)
│       ├── clients.py
│       ├── order_service.py
│       └── price_calculator.py
├── tests/                         # Suíte de testes abrangente
│   ├── test_entities.py          # Testes de entidades
│   ├── test_validation.py        # Testes de validação
│   ├── test_discount.py          # Testes de cálculo de desconto
│   ├── test_tax.py               # Testes de cálculo de impostos
│   ├── test_email.py             # Testes de serviço de email
│   ├── test_repositories.py      # Testes de repositório
│   ├── test_client_management.py # Testes de caso de uso de gerenciamento de cliente
│   ├── test_order_processing.py  # Testes de processamento de pedido
│   └── test_price_calculation.py # Testes de cálculo de preço
├── clientes.txt                   # Arquivo de dados de clientes (formato CSV)
├── pyproject.toml                 # Configuração do projeto
├── conftest.py                    # Configuração do Pytest
└── README.md                      # Este arquivo
```

## Instalação

### Pré-requisitos

- Python 3.12 ou superior
- Gerenciador de pacotes pip

### Configuração

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd repo_petrobahia
```

2. Instale as dependências:
```bash
pip install pylint black isort pytest pytest-cov
```

3. Configure o arquivo de dados de clientes (`clientes.txt`) com formato CSV:
```csv
Nome do Cliente,email@example.com,nivel
Ana Paula,ana@petrobahia.com,silver
Carlos Silva,carlos@petrobahia.com,gold
```

## Uso

### Executando o Sistema

Execute o sistema de demonstração:

```bash
cd repo_petrobahia
python src/main.py
```

O sistema irá:
1. Carregar clientes existentes do arquivo `clientes.txt`
2. Registrar novos clientes (validando duplicatas por email)
3. Processar pedidos com cálculo automático de descontos
4. Calcular preços finais com impostos

### Validação de Clientes

O sistema implementa validação robusta de clientes:

- **Email único**: Não permite cadastro de clientes com emails duplicados
- **Formato de email**: Valida o formato do email usando regex (padrão RFC)
- **Campos obrigatórios**: Nome, email e nível são obrigatórios e não podem estar vazios
- **Validação de nível**: Aceita gold, silver, bronze (case-insensitive)
- **Mensagens de erro**: Retorna mensagens claras quando a validação falha

### Taxas de Desconto por Nível

- **Gold**: 20% de desconto em todos os pedidos
- **Silver**: 10% de desconto em todos os pedidos
- **Bronze**: 5% de desconto em todos os pedidos
- **Níveis desconhecidos**: Sem desconto aplicado

### Taxas de Desconto por Quantidade

- **10+ itens**: 20% de desconto adicional
- **5-9 itens**: 10% de desconto adicional
- **Menos de 5 itens**: Sem desconto por quantidade

## Testes

### Executando os Testes

Execute a suíte completa de testes:

```bash
PYTHONPATH=src:$PYTHONPATH pytest tests/ -v
```

### Executando Testes com Cobertura

Gere um relatório de cobertura:

```bash
PYTHONPATH=src:$PYTHONPATH pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

O relatório de cobertura HTML estará disponível em `htmlcov/index.html`.

### Estatísticas de Testes

- Total de testes: 75
- Taxa de sucesso: 100%
- Cobertura de código: 76%
- Tempo de execução dos testes: ~0.5s

### Categorias de Testes

- **Testes de Entidades** (11 testes): Validação de entidades de domínio
- **Testes de Validação** (12 testes): Validação de email e cliente
- **Testes de Desconto** (21 testes): Cálculos de desconto por nível e quantidade
- **Testes de Impostos** (11 testes): Lógica de cálculo de impostos
- **Testes de Repositório** (7 testes): Persistência baseada em arquivo
- **Testes de Email** (3 testes): Funcionalidade do serviço de email
- **Testes de Casos de Uso** (10 testes): Orquestração de fluxo de trabalho de negócio

Pontuação atual do Pylint: **9.93/10**

### Métricas de Qualidade de Código

- **Linhas de Código**: ~300 (excluindo testes e legado)
- **Complexidade Ciclomática**: Baixa (funções bem estruturadas)
- **Cobertura de Testes**: 76%
- **Type Hints**: 100% de cobertura
- **Documentação**: Docstrings completas para todas as APIs públicas

### Padrões de Código

Este projeto segue as melhores práticas da indústria:

- **PEP 8**: Conformidade com o guia de estilo de código Python
- **Type Hints**: Cobertura completa de anotação de tipo
- **Docstrings**: Docstrings no estilo Google para todas as APIs públicas
- **Comprimento de Linha**: Máximo de 88 caracteres (padrão Black)
- **Cobertura de Testes**: Requisito mínimo de 70% de cobertura
- **Princípios SOLID**: Adesão rigorosa a todos os cinco princípios

## Migração do Código Legado

O código legado permanece em `src/legacy/` para referência. Principais diferenças:

### Problemas do Código Legado
- Acoplamento forte entre componentes
- Responsabilidades mistas em módulos únicos
- Difícil de testar (sem injeção de dependência)
- Sem type hints ou documentação abrangente
- Tratamento de erros limitado

### Benefícios da Refatoração
- Acoplamento fraco através de injeção de dependência
- Responsabilidade única para cada classe
- 100% testável com mocks e fixtures
- Type hints e documentação completos
- Tratamento e validação de erros abrangentes

## Considerações de Desempenho

A arquitetura refatorada mantém o desempenho enquanto melhora a manutenibilidade:

- **Validação de Entidades**: O(1) - Validação imediata na criação
- **Operações de Arquivo**: Otimizadas com context managers
- **Cálculos de Desconto**: O(1) - Buscas em dicionário
- **Execução de Testes**: <1s para a suíte completa
