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
