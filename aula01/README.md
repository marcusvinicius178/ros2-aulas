# Aula 01 — Introdução ao ROS 2

## Objetivo

- Instalar e configurar as ferramentas de desenvolvimento do ROS 2.
- Preparar o ambiente utilizado durante as aulas.
- Criar um workspace ROS 2.
- Criar o primeiro pacote ROS 2 em Python.
- Implementar um Publisher e um Subscriber.
- Executar nós individualmente e através de um Launch File.

---

# 1. Pré-requisitos

- Ubuntu 22.04 ou Ubuntu 24.04
- Terminal
- Internet

> **Ubuntu 22.04:** ROS 2 Humble  
> **Ubuntu 24.04:** ROS 2 Jazzy

---

# 2. Instalação e configuração do ROS 2

## 2.1 Configurar UTF-8

Verifique se o sistema está configurado para utilizar UTF-8:

```bash
locale
```

Instale e configure os locales:

```bash
sudo apt update
sudo apt install locales

sudo locale-gen en_US en_US.UTF-8

sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

export LANG=en_US.UTF-8
```

Verifique novamente:

```bash
locale
```

---

## 2.2 Adicionar o repositório `universe`

Instale as ferramentas necessárias:

```bash
sudo apt install software-properties-common
```

Adicione o repositório:

```bash
sudo add-apt-repository universe
```

---

## 2.3 Configurar o repositório de pacotes do ROS 2

Instale o `curl`:

```bash
sudo apt update
sudo apt install curl -y
```

Obtenha automaticamente a versão atual do pacote `ros2-apt-source`:

```bash
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
```

Baixe o pacote:

```bash
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
```

Instale:

```bash
sudo dpkg -i /tmp/ros2-apt-source.deb
```

---

## 2.4 Atualizar o sistema

Atualize o cache dos repositórios:

```bash
sudo apt update
```

Atualize os pacotes do sistema:

```bash
sudo apt upgrade
```

---

# 3. Instalação do ROS 2

Escolha **somente a opção correspondente à versão do seu Ubuntu**.

## Ubuntu 22.04 — ROS 2 Humble

Instalação Desktop recomendada, contendo ROS 2, RViz, demos e ferramentas:

```bash
sudo apt install ros-humble-desktop
```

---

## Ubuntu 24.04 — ROS 2 Jazzy

Instalação Desktop recomendada:

```bash
sudo apt install ros-jazzy-desktop
```

---

## Ferramentas de desenvolvimento

Instale as ferramentas utilizadas para desenvolvimento e compilação:

```bash
sudo apt install ros-dev-tools
```

---

# 4. Configurando o ambiente ROS 2

Escolha o comando correspondente à sua distribuição.

## Ubuntu 22.04 — Humble

```bash
source /opt/ros/humble/setup.bash
```

Para carregar automaticamente o ROS 2 em novos terminais:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

---

## Ubuntu 24.04 — Jazzy

```bash
source /opt/ros/jazzy/setup.bash
```

Para carregar automaticamente o ROS 2 em novos terminais:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

Depois, em ambos os casos:

```bash
source ~/.bashrc
```

---

# 5. Pacotes e ferramentas úteis

## 5.1 Ubuntu 22.04 + ROS 2 Humble

### Ferramentas gerais de compilação

- `build-essential`: GCC, G++, Make e ferramentas básicas.
- `python3-colcon-common-extensions`: extensões do Colcon.
- `python3-rosdep`: resolução automática de dependências.
- Fast DDS e Cyclone DDS: implementações de middleware DDS.

```bash
sudo apt install -y \
  build-essential \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-humble-rmw-fastrtps-cpp \
  ros-humble-rmw-cyclonedds-cpp
```

---

### RViz2 e TF2

```bash
sudo apt install -y \
  ros-humble-rviz2 \
  ros-humble-tf2-tools
```

---

### Turtlesim

```bash
sudo apt install -y \
  ros-humble-turtlesim
```

---

### Teleoperação pelo teclado

```bash
sudo apt install -y \
  ros-humble-teleop-twist-keyboard
```

---

### TurtleBot3 + Gazebo Classic

```bash
sudo apt install -y \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-msgs \
  ros-humble-turtlebot3-simulations \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros
```

---

# 6. Ubuntu 24.04 + ROS 2 Jazzy + TurtleBot3

No Ubuntu 24.04, utilizaremos ROS 2 Jazzy e Gazebo Sim.

## 6.1 Carregar ROS 2 Jazzy

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 6.2 Instalar Gazebo Harmonic

Atualize o sistema e instale as dependências:

```bash
sudo apt-get update

sudo apt-get install -y \
  curl \
  lsb-release \
  gnupg
```

Adicione a chave do repositório OSRF:

```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
```

Adicione o repositório:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
```

Atualize novamente:

```bash
sudo apt-get update
```

Instale o Gazebo Harmonic:

```bash
sudo apt-get install -y gz-harmonic
```

---

## 6.3 Criar o workspace do TurtleBot3

```bash
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src
```

Clone os pacotes principais:

```bash
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git

git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git

git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
```

---

## 6.4 Clonar os pacotes de simulação

Ainda dentro de:

```text
~/turtlebot3_ws/src
```

execute:

```bash
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
```

Depois:

```bash
cd ~/turtlebot3_ws
```

---

## 6.5 Instalar dependências com `rosdep`

Caso o `rosdep` ainda não tenha sido inicializado:

```bash
sudo rosdep init 2>/dev/null || true
```

Atualize:

```bash
rosdep update
```

Instale as dependências do workspace:

```bash
rosdep install --from-paths src -i -y
```

---

## 6.6 Compilar o workspace

Instale o Colcon, caso ainda não esteja instalado:

```bash
sudo apt install -y python3-colcon-common-extensions
```

Compile:

```bash
cd ~/turtlebot3_ws

colcon build --symlink-install
```

---

## 6.7 Carregar o workspace

```bash
source ~/turtlebot3_ws/install/setup.bash
```

---

## 6.8 Rodar a simulação do TurtleBot3

Existem diferentes modelos e mundos disponíveis.

### Opção 1 — Burger + Empty World

Defina o modelo:

```bash
export TURTLEBOT3_MODEL=burger
```

Execute:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

---

### Opção 2 — Waffle + TurtleBot3 World

Defina o modelo:

```bash
export TURTLEBOT3_MODEL=waffle
```

Execute:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

---

### Opção 3 — Waffle Pi + TurtleBot3 House

Defina o modelo:

```bash
export TURTLEBOT3_MODEL=waffle_pi
```

Execute:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```

---

# Parte prática da Aula 1

Nesta seção estão os comandos e arquivos utilizados durante a parte prática da aula, seguindo a ordem apresentada nos slides.

---

# Prática 1 — Criando o primeiro pacote ROS 2

## 1. Criar o workspace

Crie a estrutura padrão do workspace:

```bash
mkdir -p ~/ros2_ws/src
```

Entre no workspace:

```bash
cd ~/ros2_ws
```

---

## 2. Criar o pacote `my_lab01`

Entre na pasta de código-fonte:

```bash
cd ~/ros2_ws/src
```

Crie o pacote:

```bash
ros2 pkg create \
  --build-type ament_python \
  my_lab01 \
  --dependencies rclpy std_msgs sensor_msgs geometry_msgs \
  --maintainer-name "Marcus Vinicius" \
  --maintainer-email "marcus@example.com" \
  --license Apache-2.0
```

Após esse comando, será criada uma estrutura semelhante a:

```text
ros2_ws/
└── src/
    └── my_lab01/
        ├── my_lab01/
        ├── package.xml
        ├── resource/
        ├── setup.cfg
        └── setup.py
```

---

## 3. Criar o Publisher

Entre no diretório Python do pacote:

```bash
cd ~/ros2_ws/src/my_lab01/my_lab01
```

Crie o arquivo:

```bash
gedit simple_pub.py
```

O código utilizado na aula está disponível em:

[`scripts/simple_pub.py`](scripts/simple_pub.py)

Copie o conteúdo desse arquivo para:

```text
~/ros2_ws/src/my_lab01/my_lab01/simple_pub.py
```

---

## 4. Criar o Subscriber

Ainda no mesmo diretório:

```bash
cd ~/ros2_ws/src/my_lab01/my_lab01
```

Crie o arquivo:

```bash
gedit simple_sub.py
```

O código utilizado na aula está disponível em:

[`scripts/simple_sub.py`](scripts/simple_sub.py)

Copie o conteúdo para:

```text
~/ros2_ws/src/my_lab01/my_lab01/simple_sub.py
```

---

## 5. Dar permissão de execução aos scripts

```bash
chmod +x ~/ros2_ws/src/my_lab01/my_lab01/simple_pub.py
```

```bash
chmod +x ~/ros2_ws/src/my_lab01/my_lab01/simple_sub.py
```

---

## 6. Atualizar o `setup.py`

Abra:

```bash
gedit ~/ros2_ws/src/my_lab01/setup.py
```

Utilize como referência o arquivo:

[`scripts/setup.py`](scripts/setup.py)

O `setup.py` é responsável, entre outras funções, por registrar os executáveis Python do pacote.

---

## 7. Criar o Launch File

Entre no diretório principal do pacote:

```bash
cd ~/ros2_ws/src/my_lab01
```

Crie a pasta `launch`:

```bash
mkdir -p launch
```

Crie o arquivo:

```bash
gedit ~/ros2_ws/src/my_lab01/launch/demo.launch.py
```

Utilize como referência:

[`scripts/launch/demo.launch.py`](scripts/launch/demo.launch.py)

---

## 8. Compilar o workspace

Entre no workspace:

```bash
cd ~/ros2_ws
```

Compile:

```bash
colcon build --symlink-install
```

Carregue o ambiente compilado:

```bash
source ~/ros2_ws/install/setup.bash
```

---

## 9. Testar Publisher e Subscriber

Abra dois terminais.

### Terminal 1 — Publisher

```bash
source ~/ros2_ws/install/setup.bash
```

Execute:

```bash
ros2 run my_lab01 simple_pub
```

---

### Terminal 2 — Subscriber

```bash
source ~/ros2_ws/install/setup.bash
```

Execute:

```bash
ros2 run my_lab01 simple_sub
```

O Subscriber deverá começar a receber as mensagens enviadas pelo Publisher.

---

## 10. Executar Publisher e Subscriber através do Launch File

Primeiro carregue o workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Execute:

```bash
ros2 launch my_lab01 demo.launch.py
```

Os dois nós deverão ser inicializados pelo mesmo Launch File.

---

# Prática 2 — Inspeção de Topics

Nesta prática vamos utilizar a CLI do ROS 2 para inspecionar tópicos, mensagens, frequência e conexões entre Publishers e Subscribers.

## 1. Executar a aplicação

Primeiro, carregue o workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Execute o Launch File:

```bash
ros2 launch my_lab01 demo.launch.py
```

---

## 2. Listar os tópicos disponíveis

Em outro terminal:

```bash
source ~/ros2_ws/install/setup.bash
```

Liste os tópicos:

```bash
ros2 topic list
```

---

## 3. Verificar o tipo de mensagem de um tópico

```bash
ros2 topic type /topic
```

---

## 4. Visualizar as mensagens publicadas

```bash
ros2 topic echo /topic
```

---

## 5. Publicar manualmente em um tópico

```bash
ros2 topic pub /topic std_msgs/msg/String "data: 'teste'"
```

---

## 6. Verificar a frequência de publicação

```bash
ros2 topic hz /topic
```

---

## 7. Ver informações sobre Publishers e Subscribers

```bash
ros2 topic info /topic
```

---

## 8. Ver informações detalhadas do tópico

```bash
ros2 topic info /topic --verbose
```

---

# Prática 3 — TurtleBot3, Gazebo e LiDAR

Nesta prática vamos executar o TurtleBot3 no simulador, controlar o robô pelo teclado e observar os dados publicados pelo sensor LiDAR.

## 1. Terminal A — Executar o simulador

Carregue o ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Defina o modelo do TurtleBot3:

```bash
export TURTLEBOT3_MODEL=burger
```

Execute o mundo do TurtleBot3:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Mantenha este terminal aberto.

---

## 2. Terminal B — Teleoperação

Abra um novo terminal.

Carregue o ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Execute o controle pelo teclado:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
```

Utilize o teclado para movimentar o TurtleBot3 no simulador.

---

## 3. Terminal C — Visualizar os dados do LiDAR

Abra um terceiro terminal.

Carregue o ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Observe as mensagens publicadas pelo LiDAR:

```bash
ros2 topic echo /scan
```

Para confirmar o tipo da mensagem:

```bash
ros2 topic type /scan
```

Para verificar a frequência:

```bash
ros2 topic hz /scan
```

Para visualizar informações detalhadas do tópico:

```bash
ros2 topic info /scan --verbose
```

---

## 4. Resultado esperado

Ao final desta prática deverão existir três processos simultâneos:

```text
Terminal A
└── Gazebo + TurtleBot3

Terminal B
└── teleop_twist_keyboard

Terminal C
└── ros2 topic echo /scan
```

Ao movimentar o robô pelo teclado, o TurtleBot3 deverá se mover no simulador enquanto o tópico `/scan` continua publicando os dados do LiDAR.

---

# Prática 4 — Leitura do LiDAR e navegação

Nesta prática vamos criar um nó ROS 2 que recebe os dados do LiDAR através do tópico `/scan` e publica comandos de velocidade para o robô.

## 1. Criar o arquivo `read_navigate.py`

Entre no diretório Python do pacote:

```bash
cd ~/ros2_ws/src/my_lab01/my_lab01
```

Crie o arquivo:

```bash
gedit read_navigate.py
```

O código utilizado na aula está disponível em:

[`scripts/read_navigate.py`](scripts/read_navigate.py)

Copie o conteúdo desse arquivo para:

```text
~/ros2_ws/src/my_lab01/my_lab01/read_navigate.py
```

---

## 2. Dar permissão de execução

```bash
chmod +x ~/ros2_ws/src/my_lab01/my_lab01/read_navigate.py
```

---

## 3. Atualizar o `setup.py`

Abra:

```bash
gedit ~/ros2_ws/src/my_lab01/setup.py
```

Utilize como referência:

[`scripts/setup.py`](scripts/setup.py)

O arquivo deve conter o executável:

```text
read_navigate = my_lab01.read_navigate:main
```

---

## 4. Recompilar o workspace

Entre no workspace:

```bash
cd ~/ros2_ws
```

Compile novamente:

```bash
colcon build --symlink-install
```

Carregue o workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

---

## 5. Terminal A — Executar o TurtleBot3 no Gazebo

Carregue o ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Defina o modelo:

```bash
export TURTLEBOT3_MODEL=burger
```

Execute o simulador:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

---

## 6. Terminal B — Executar o nó de navegação

Abra um novo terminal.

Carregue o workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Execute:

```bash
ros2 run my_lab01 read_navigate
```

---

## 7. Terminal C — Inspecionar o LiDAR

Abra outro terminal.

Visualize as mensagens do LiDAR:

```bash
ros2 topic echo /scan
```

Verifique a frequência:

```bash
ros2 topic hz /scan
```

---

## 8. Resultado esperado

O nó `read_navigate` deverá:

- receber os dados do sensor LiDAR através do tópico `/scan`;
- processar as distâncias medidas;
- publicar comandos de velocidade para o robô;
- permitir que o TurtleBot3 reaja aos obstáculos do ambiente.

---

# Prática 5 — Visualizando a comunicação com RQT Graph

Nesta prática vamos utilizar o `rqt_graph` para visualizar graficamente os nós e tópicos ativos no sistema ROS 2.

## 1. Executar a aplicação

Primeiro, execute novamente a aplicação criada anteriormente:

```bash
source ~/ros2_ws/install/setup.bash
```

```bash
ros2 launch my_lab01 demo.launch.py
```

Mantenha esse terminal aberto.

---

## 2. Abrir o RQT Graph

Abra um novo terminal e carregue o ambiente ROS 2:

```bash
source ~/ros2_ws/install/setup.bash
```

Execute:

```bash
ros2 run rqt_graph rqt_graph
```

---

## 3. O que observar

No `rqt_graph`, identifique:

- o nó Publisher;
- o nó Subscriber;
- o tópico que conecta os dois nós;
- o sentido do fluxo de mensagens.

A representação esperada é semelhante a:

```text
Publisher Node
      |
      v
    /topic
      |
      v
Subscriber Node
```

---

## 4. Testar com o TurtleBot3

Também é possível utilizar o `rqt_graph` enquanto o TurtleBot3 estiver executando.

Em um terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

```bash
export TURTLEBOT3_MODEL=burger
```

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Em outro terminal:

```bash
ros2 run rqt_graph rqt_graph
```

Observe os nós e tópicos criados pelo simulador e pelo robô.

---

# Prática 6 — Bridge ROS–Gazebo e RViz

Nesta prática vamos observar como os dados do robô simulado são disponibilizados no ROS 2 e visualizados no RViz.

## 1. Executar o TurtleBot3 no Gazebo

Abra um terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Defina o modelo:

```bash
export TURTLEBOT3_MODEL=burger
```

Execute o simulador:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Mantenha este terminal aberto.

---

## 2. Verificar os tópicos disponíveis

Abra um novo terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Liste os tópicos:

```bash
ros2 topic list
```

Procure tópicos relacionados a sensores, estados do robô e controle.

---

## 3. Inspecionar os estados das juntas

Verifique se o tópico de estados das juntas está disponível:

```bash
ros2 topic echo /joint_states
```

Esse tópico contém informações sobre as juntas do robô, como posição e velocidade.

---

## 4. Executar a teleoperação

Em outro terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Execute:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
```

Movimente o robô e observe como os estados e tópicos são atualizados.

---

## 5. Abrir o RViz

Abra um novo terminal:

```bash
source /opt/ros/jazzy/setup.bash
```

Execute:

```bash
rviz2
```

---

## 6. O que observar no RViz

No RViz, observe que os dados publicados pelos nós ROS 2 podem ser visualizados graficamente.

Alguns exemplos de informações que podem ser exibidas:

- modelo do robô;
- transformadas TF;
- dados do LiDAR;
- posição e orientação;
- estados das juntas;
- informações de sensores.

---

## 7. Relação entre Gazebo, ROS 2 e RViz

O fluxo conceitual é:

```text
Gazebo
  |
  | dados da simulação
  v
Bridge / ROS 2
  |
  | tópicos e transformadas
  v
RViz
```

O Gazebo simula o robô e o ambiente.

O ROS 2 transporta as informações através de tópicos, serviços e transformadas.

O RViz visualiza essas informações.

---

# Prática 7 — Exercício com o Prius

Nesta prática vamos executar uma demonstração com o Prius em ambiente simulado e utilizar ferramentas do ROS 2 para inspecionar os dados publicados.

## 1. Clonar o repositório

Entre no diretório desejado:

```bash
cd ~
```

Clone o repositório:

```bash
git clone https://github.com/mattborghi/osrf_car_demo.git
```

Entre na pasta:

```bash
cd ~/osrf_car_demo
```

---

## 2. Atualizar o arquivo `run_demo.bash`

Antes de compilar o demo, substitua o conteúdo do arquivo:

```text
~/osrf_car_demo/run_demo.bash
```

pelo arquivo utilizado nesta aula:

[`prius/run_demo.bash`](prius/run_demo.bash)

Abra o arquivo original:

```bash
gedit ~/osrf_car_demo/run_demo.bash
```

Apague todo o conteúdo atual e copie o conteúdo de:

[`prius/run_demo.bash`](prius/run_demo.bash)

Garanta também que o arquivo possui permissão de execução:

```bash
chmod +x ~/osrf_car_demo/run_demo.bash
```

---

## 3. Compilar o demo

Execute:

```bash
./build_demo.bash
```

---

## 4. Executar com suporte NVIDIA

Execute:

```bash
./run_demo.bash --nvidia
```

Mantenha esse terminal aberto.

---

## 5. Entrar no container

Abra um novo terminal.

Liste os containers em execução:

```bash
docker ps
```

Identifique o nome do container.

Entre nele com:

```bash
docker exec -it NOME_DO_CONTAINER bash
```

---

## 6. Listar os tópicos ROS 2

Dentro do container:

```bash
ros2 topic list
```

---

## 7. Abrir o RQT Graph

Ainda dentro do ambiente ROS 2:

```bash
ros2 run rqt_graph rqt_graph
```

Observe os nós e tópicos criados pela simulação.

---

## 8. Inspecionar posição e velocidade das juntas

Execute:

```bash
ros2 topic echo /prius/joint_states
```

Observe os valores publicados pelo veículo durante a simulação.

---

# Prática 8 — DDS e QoS na prática

Nesta prática vamos observar o efeito de políticas de QoS incompatíveis entre Publisher e Subscriber.

## 1. Clonar o repositório da demonstração de QoS

Entre na pasta do demo do Prius:

```bash
cd ~/osrf_car_demo
```

Clone o repositório:

```bash
git clone https://github.com/marcusvinicius178/qos_demo_visual.git
```

---

## 2. Atualizar o Dockerfile

Substitua o conteúdo do `Dockerfile` utilizado pelo demo pelo arquivo:

[`qos/Dockerfile`](qos/Dockerfile)

---

## 3. Recompilar a imagem

Entre novamente em:

```bash
cd ~/osrf_car_demo
```

Execute:

```bash
./build_demo.bash
```

Depois:

```bash
./run_demo.bash --nvidia
```

---

## 4. Entrar no container

Em outro terminal:

```bash
docker ps
```

Identifique o nome do container e entre nele:

```bash
docker exec -it NOME_DO_CONTAINER bash
```

---

## 5. Teste com QoS incompatível

Execute:

```bash
ros2 launch qos_demo_visual qos_prius_qos_demo.launch.py consumer_sub_rel:=reliable
```

Em outro terminal dentro do container:

```bash
ros2 topic echo /qos_demo/points_fixed
```

Com o Subscriber configurado como `reliable` e o Publisher utilizando `best_effort`, os dados não deverão fluir devido à incompatibilidade de QoS.

---

## 6. Teste com QoS compatível

Finalize o launch anterior e execute:

```bash
ros2 launch qos_demo_visual qos_prius_qos_demo.launch.py consumer_sub_rel:=best_effort
```

Verifique novamente:

```bash
ros2 topic echo /qos_demo/points_fixed
```

Agora os dados deverão começar a ser publicados.

---

## 7. Visualização no RViz

No RViz, adicione um display:

```text
PointCloud2
```

Configure o tópico:

```text
/qos_demo/points_fixed
```

Ajuste a política de Reliability para:

```text
Best Effort
```

---

## 8. Teste de Durability

Adicione um display:

```text
Marker
```

Configure o tópico:

```text
/qos_demo/latched_marker
```

Altere a política de Durability de:

```text
Volatile
```

para:

```text
Transient Local
```

O marker deverá aparecer no RViz.


# URDF — Step 1: criando o primeiro link

Nesta etapa vamos criar a estrutura inicial do pacote `meu_robo_urdf_aula` e o primeiro modelo URDF.

## 1. Criar a estrutura do pacote

Entre na pasta `src` do workspace:

```bash
cd ~/ros2_ws/src
```

Crie a estrutura de diretórios:

```bash
mkdir -p meu_robo_urdf_aula/launch
mkdir -p meu_robo_urdf_aula/urdf
mkdir -p meu_robo_urdf_aula/rviz
```

Entre no pacote:

```bash
cd ~/ros2_ws/src/meu_robo_urdf_aula
```

Crie os arquivos:

```bash
touch package.xml
touch CMakeLists.txt
touch launch/display_step1.launch.py
touch urdf/simple_robot_step1.urdf
touch rviz/step1.rviz
```

---

## 2. Preencher os arquivos do Step 1

Os arquivos completos utilizados na aula estão disponíveis neste repositório.

### `package.xml`

[`package.xml`](exemplos/meu_robo_urdf_aula/package.xml)

Abra o arquivo local:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/package.xml
```

Copie para ele o conteúdo disponível no link acima.

---

### `CMakeLists.txt`

[`CMakeLists.txt`](exemplos/meu_robo_urdf_aula/CMakeLists.txt)

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/CMakeLists.txt
```

Copie para ele o conteúdo disponível no link acima.

---

### `simple_robot_step1.urdf`

[`urdf/simple_robot_step1.urdf`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step1.urdf)

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/urdf/simple_robot_step1.urdf
```

Copie para ele o conteúdo disponível no link acima.

---

### `display_step1.launch.py`

[`launch/display_step1.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step1.launch.py)

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/launch/display_step1.launch.py
```

Copie para ele o conteúdo disponível no link acima.

---

### `step1.rviz`

[`rviz/step1.rviz`](exemplos/meu_robo_urdf_aula/rviz/step1.rviz)

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/rviz/step1.rviz
```

Copie para ele o conteúdo disponível no link acima.

---

## 3. Compilar o Step 1

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue o workspace:

```bash
source install/setup.bash
```

---

## 4. Executar o Step 1

```bash
ros2 launch meu_robo_urdf_aula display_step1.launch.py
```

O RViz deverá abrir mostrando o primeiro modelo do robô.

---

# URDF — Step 2: adicionando o primeiro braço e a primeira junta

Nesta etapa vamos preservar o Step 1 e criar uma nova versão do modelo.

Será adicionado o link `left_arm_link`, conectado ao torso através de uma junta do tipo `revolute`.

## 1. Criar os arquivos do Step 2

Entre no pacote:

```bash
cd ~/ros2_ws/src/meu_robo_urdf_aula
```

Crie o novo URDF a partir do Step 1:

```bash
cp urdf/simple_robot_step1.urdf urdf/simple_robot_step2.urdf
```

Crie o novo Launch File:

```bash
cp launch/display_step1.launch.py launch/display_step2.launch.py
```

Crie a configuração do RViz para este passo:

```bash
cp rviz/step1.rviz rviz/step2.rviz
```

---

## 2. Atualizar o URDF do Step 2

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/urdf/simple_robot_step2.urdf
```

Substitua o conteúdo pelo arquivo:

[`urdf/simple_robot_step2.urdf`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step2.urdf)

---

## 3. Atualizar o Launch File do Step 2

Abra:

```bash
gedit ~/ros2_ws/src/meu_robo_urdf_aula/launch/display_step2.launch.py
```

Use como referência:

[`launch/display_step2.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step2.launch.py)

Esse Launch File deve carregar:

```text
simple_robot_step2.urdf
```

e a configuração:

```text
step2.rviz
```

---

## 4. Configuração RViz do Step 2

O arquivo utilizado nesta etapa está disponível em:

[`rviz/step2.rviz`](exemplos/meu_robo_urdf_aula/rviz/step2.rviz)

---

## 5. Recompilar o pacote

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue novamente o workspace:

```bash
source install/setup.bash
```

---

## 6. Executar o Step 2

```bash
ros2 launch meu_robo_urdf_aula display_step2.launch.py
```

O modelo deverá apresentar o torso e o primeiro braço conectado através de uma junta do tipo `revolute`.

---

---

# URDF — Step 3: adicionando o braço direito

Nesta etapa adicionamos o braço direito ao modelo.

Arquivos utilizados:

- [`urdf/simple_robot_step3.urdf`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step3.urdf)
- [`launch/display_step3.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step3.launch.py)

Compile o pacote:

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue o workspace:

```bash
source install/setup.bash
```

Execute:

```bash
ros2 launch meu_robo_urdf_aula display_step3.launch.py
```

---

# URDF — Step 4: adicionando uma câmera

Nesta etapa adicionamos um novo link representando uma câmera sobre o robô.

A câmera é conectada ao corpo através de uma junta fixa.

Arquivos utilizados:

- [`urdf/simple_robot_step4.urdf`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step4.urdf)
- [`launch/display_step4.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step4.launch.py)

Compile o pacote:

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue o workspace:

```bash
source install/setup.bash
```

Execute:

```bash
ros2 launch meu_robo_urdf_aula display_step4.launch.py
```

Nesta etapa o modelo deve apresentar:

- torso;
- braço esquerdo;
- braço direito;
- câmera;
- junta fixa conectando a câmera ao robô

---

# URDF — Step 5: conversão para Xacro

Nesta etapa o modelo URDF é convertido para Xacro.

O Xacro permite utilizar propriedades e macros, reduzindo repetição e facilitando a manutenção do modelo do robô.

Arquivos utilizados:

- [`urdf/simple_robot_step5.urdf.xacro`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step5.urdf.xacro)
- [`launch/display_step5.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step5.launch.py)
- [`rviz/step5.rviz`](exemplos/meu_robo_urdf_aula/rviz/step5.rviz)

Compile o pacote:

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue o workspace:

```bash
source install/setup.bash
```

Execute:

```bash
ros2 launch meu_robo_urdf_aula display_step5.launch.py
```

Nesta etapa o modelo passa a ser descrito utilizando Xacro, permitindo uma estrutura mais modular e reutilizável.

---

# URDF — Step 6: levando a câmera para o Gazebo

Nesta etapa o modelo Xacro passa a incluir a integração da câmera com o Gazebo.

O `camera_link` continua representando o frame físico da câmera no modelo do robô.

O Gazebo adiciona o sensor responsável pela geração da imagem, e a bridge converte os dados do simulador para mensagens ROS 2.

O fluxo é:

```text
camera_link
    ↓
Gazebo Sensor
    ↓
ros_gz_bridge
    ↓
ROS 2
    ↓
RViz2
```

## Arquivos utilizados

- [`urdf/simple_robot_step6.urdf.xacro`](exemplos/meu_robo_urdf_aula/urdf/simple_robot_step6.urdf.xacro)
- [`launch/display_step6.launch.py`](exemplos/meu_robo_urdf_aula/launch/display_step6.launch.py)
- [`rviz/step6.rviz`](exemplos/meu_robo_urdf_aula/rviz/step6.rviz)
- [`world/empty_camera.world.sdf`](exemplos/meu_robo_urdf_aula/world/empty_camera.world.sdf)

## Compilar o pacote

```bash
cd ~/ros2_ws
colcon build --packages-select meu_robo_urdf_aula
```

Carregue o workspace:

```bash
source install/setup.bash
```

## Executar

```bash
ros2 launch meu_robo_urdf_aula display_step6.launch.py
```

## Resultado esperado

Nesta etapa:

- o robô deverá ser carregado no simulador;
- a câmera deverá existir como sensor no Gazebo;
- a imagem deverá ser disponibilizada através da bridge;
- o RViz poderá visualizar o tópico correspondente à câmera.
