# PetTracker

Um sistema de rastreamento remoto da localização de animais, que permite uma visualização e recebimento de alertas provindos dos animais monitorados.

&nbsp;&nbsp;&nbsp;&nbsp;

## Estrutura do Projeto

### Descrição Geral da Solução

O **PetTracker** é um sistema de rastreamento remoto da localização de animais, desenvolvido para auxiliar no monitoramento e na gestão eficiente de territórios e populações de animais. A solução permite que usuários, sejam eles supervisores ou administradores, tenham acesso a uma plataforma centralizada para visualizar a posição dos animais em tempo real, bem como consultar registros históricos dessas localizações.

Através de um sistema flexível e adaptável, o **PetTracker** possibilita a identificação de padrões de movimentação dos animais, auxiliando na tomada de decisões estratégicas, como realocação de recursos, ajustes em áreas de pastagem e detecção de possíveis situações de risco. Além disso, conta com um mecanismo de alerta que notifica os responsáveis caso um animal ultrapasse os limites estabelecidos do território definido.

Para garantir uma ampla aplicabilidade, o sistema pode ser integrado a diferentes tecnologias de rastreamento, como antenas centralizadas utilizando protocolos de comunicação como LoRa ou ZigBee, ou ainda através de SIM Cards individuais com comunicação via redes móveis. A decisão sobre a melhor abordagem a ser utilizada pode variar conforme o cenário de aplicação, tornando o **PetTracker** uma solução versátil para diferentes setores, como agropecuária, zoológicos e reservas naturais.

### 1. Arquivo `main.py`
Este é o arquivo principal do projeto, responsável por iniciar o sistema e gerenciar a interface do usuário.

#### Classes de Usuário
- **UserRole**: Classe abstrata para definir o papel dos usuários.
- **RegularUser**: Classe para usuários comuns que podem visualizar territórios.
- **AdminUser**: Classe para administradores que têm acesso total ao sistema.

#### Função de Login
- `login_screen(facade)`: Gerencia a tela de login e autenticação de usuários.

### 2. Classes de Apoio
#### Classe `Tracker` (Arquivo: `_class/tracker.py`)
- Responsável por gerar e salvar a localização dos animais.
- Utiliza **threads** para realizar a geração contínua de localizações e o salvamento periódico no banco de dados.

#### Classe `Animal` (Arquivo: `_class/animal.py`)
- Representa um animal no sistema.
- Cada animal possui um rastreador (`Tracker`) que gera suas posições.

#### Classe `Territory` (Arquivo: `_class/territory.py`)
- Representa um território no sistema.
- Cada território pode ter vários animais associados.

### 3. Padrões de Design Utilizados
#### Facade (Padrão de Fachada)
- **SystemFacade**: Centraliza e simplifica a interação com o sistema, fornecendo uma interface unificada para várias operações.

#### Proxy (Padrão de Proxy)
- **UserProxy, AdminProxy, TerritoryProxy**: Utilizados para armazenar em cache objetos frequentemente acessados, reduzindo a necessidade de consultas repetidas ao banco de dados.

#### Builder (Padrão de Construtor)
- **TerritoryBuilder**: Facilita a criação de objetos `Territory` complexos, permitindo a configuração passo a passo de suas propriedades.

#### Adapter (Padrão de Adaptador)
- **CoordinateAdapter**: Converte coordenadas geográficas em componentes cartesianas (x, y) para uso no sistema.

#### Singleton (Padrão de Singleton)
- **Database**: Garante que apenas uma instância da classe de banco de dados seja criada, fornecendo um ponto de acesso global a essa instância.

#### Strategy (Padrão de Estratégia)
- **UserRole**: Define uma interface comum para diferentes papéis de usuário (RegularUser e AdminUser), permitindo que cada um tenha seu próprio comportamento de menu.

#### Template Method (Padrão de Método Template)
- **PersonTemplate**: Define o esqueleto de um algoritmo na superclasse, permitindo que subclasses específicas implementem detalhes do algoritmo.

### 4. Banco de Dados
#### Classe `Database` (Arquivo: `database/database.py`)
- Gerencia a conexão e as operações com o banco de dados SQLite.
- Cria e mantém as tabelas necessárias:
  - `admins`
  - `users`
  - `territories`
  - `animals`
  - `location`
  - `tracker`

&nbsp;&nbsp;&nbsp;&nbsp;

## Funcionalidades do Sistema

### 1. Usuários Comuns
- Podem visualizar territórios.
- Iniciam uma **thread** para simular a visualização do território em tempo real.

### 2. Administradores
- Têm acesso total ao sistema.
- Podem gerenciar **territórios, usuários e animais**.
- Podem visualizar territórios em tempo real e históricos de localização dos animais.

&nbsp;&nbsp;&nbsp;&nbsp;

## Regras e Limitações

### Login e Autenticação
- Os usuários e administradores são autenticados usando **bcrypt** para verificação de senha.

### Gerenciamento de Territórios
- Os administradores podem **criar, visualizar e deletar** territórios.

### Gerenciamento de Usuários
- Os administradores podem **criar, listar e deletar** usuários.

### Gerenciamento de Animais
- Os administradores podem **adicionar, listar e deletar** animais.

&nbsp;&nbsp;&nbsp;&nbsp;

## Interações Entre Padrões

### Facade e Classes de Entidade
- **SystemFacade** interage com **Tracker, Animal e Territory** para realizar operações complexas de forma simplificada.

### Proxy para Cache
- **UserProxy, AdminProxy, TerritoryProxy** armazenam em cache objetos frequentemente acessados, melhorando a eficiência do sistema.

### Builder para Criação de Objetos
- **TerritoryBuilder** facilita a criação de objetos `Territory` complexos, permitindo a configuração passo a passo de suas propriedades.

### Adapter para Conversão de Coordenadas
- **CoordinateAdapter** converte coordenadas geográficas em componentes cartesianas (x, y) para uso no sistema.
f
### Singleton para Gerenciamento de Banco de Dados
- **Database**: Utiliza o padrão Singleton para garantir que apenas uma instância da classe de banco de dados seja criada. Isso é feito através do método `__new__`, que verifica se uma instância já existe antes de criar uma nova. Esse padrão é útil para gerenciar a conexão com o banco de dados de forma centralizada e eficiente.

### Strategy para Gerenciamento de Menus de Usuário
- **UserRole**: Define uma interface comum para diferentes papéis de usuário (RegularUser e AdminUser). Cada classe concreta implementa o método `show_menu` de forma diferente, permitindo que cada tipo de usuário tenha seu próprio comportamento de menu. Isso facilita a adição de novos tipos de usuários no futuro sem modificar o código existente.

### Template Method para Definição de Algoritmos
- **PersonTemplate**: Define o esqueleto de um algoritmo na superclasse, permitindo que subclasses específicas (User e Admin) implementem detalhes do algoritmo. Métodos abstratos como `save` e `delete` são definidos na superclasse e implementados nas subclasses, garantindo que a estrutura do algoritmo seja seguida enquanto permite variações nos detalhes.

&nbsp;&nbsp;&nbsp;&nbsp;

## Conclusão
O projeto **"PetTracker"** é um sistema robusto de rastreamento de animais, utilizando **padrões de design** para manter o código organizado e eficiente. Ele fornece funcionalidades essenciais para **gerenciamento de territórios e animais**, com uma interface intuitiva para diferentes tipos de usuários.
