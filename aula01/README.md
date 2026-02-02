# Aula 01

## Objetivo
- Instalar e configurar ferramentas de desenvolimento do ROS2

## Pré-requisitos
- Ubuntu 22.04 ou 24.04
- Terminal
- Internet


### Configurar o sistema para texto e caracteres especiais (UTF-8)
```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### Configurar fontes: Adicionar o repositório apt do ROS2 no sistema
```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

### Instalando o pacote ros2-apt irá configurar os repositórios do ROS2 para o sistema. Atualizações das configurações do repositório irão ocorrer automaticamente quando novas versões deste pacote são liberadas para os repositórios do ROS2.
```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

### Instalação dos pacotes ROS2
### Atualize os caches do repositório apt configurando os repositórios
```bash
sudo apt update
```

### Os pacotes ROS2 são construídos frequentemente em sistemas Ubuntu atualizados. É semre recomendadado que você garanta que seu sistema esteja atualizado antes de instalar novos pacotes.
```bash
sudo apt upgrade
```

## Instalação do Desktop para Ubuntu 22.04 (Recomendada): ROS; Rviz; Demos, Tutoriais
```bash 
sudo apt install ros-humble-desktop
```

## Instalação do Desktop para Ubuntu 24.04 (Recomendada): ROS; Rviz; Demos, Tutoriais
```bash 
sudo apt install ros-jazzy-desktop
```

### Ferramentas de desenvolvimento: Compiladores e outras ferramentas para buildar os pacotes ROS
```
sudo apt install ros-dev-tools
```

### Configurando o Ambiente (Ubuntu 22.04)
### Configure o ambiente obtendo o seguinte arquivo

```bash
source /opt/ros/humble/setup.bash
```

### Configurando o Ambiente (Ubuntu 24.04)
### Configure o ambiente obtendo o seguinte arquivo

```bash
source /opt/ros/jazzy/setup.bash
```

### Edite o arquivo .bashrc adicionando a linha acima ("source /opt/ros/humble/setup.bash") na última linha deste arquivo. 

# ------------------------------------------------------------
# Pacotes e ferramentas úteis para os próximos tutoriais
# Ubuntu 22.04 (Jammy) + ROS 2 Humble
# ------------------------------------------------------------

# 1) Ferramentas gerais de compilação e desenvolvimento
# - build-essential: gcc/g++/make básicos
# - python3-colcon-common-extensions: colcon com plugins comuns para build do ROS
# - python3-rosdep: resolve dependências de pacotes ROS (muito usado em workspaces)
#
# 2) RMW (DDS) implementações
# - FastDDS e CycloneDDS para você poder alternar middleware se necessário
```bash
sudo apt install -y \
  build-essential \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-humble-rmw-fastrtps-cpp \
  ros-humble-rmw-cyclonedds-cpp
```
# Visualização e depuração
# - RViz2: visualização
# - tf2-tools: ferramentas de inspeção de TF (view_frames, tf2_echo, etc)
bash```
sudo apt install -y \
  ros-humble-rviz2 \
  ros-humble-tf2-tools

# Turtlesim (aquecimento)
# - Pacote clássico para testar tópicos, serviços e nós rapidamente
```bash
sudo apt install -y \
  ros-humble-turtlesim
```

# Teleop (controle por teclado)
# - Envia geometry_msgs/Twist para controlar robôs/simulação
```bash
sudo apt install -y \
  ros-humble-teleop-twist-keyboard
```
# TurtleBot3 + Gazebo Classic (mais simples para Humble)
# - Instala pacotes do TurtleBot3 e simulação pronta
# - Gazebo Classic via gazebo_ros_pkgs (ainda disponível no Humble)
```bash
sudo apt install -y \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-msgs \
  ros-humble-turtlebot3-simulations \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros
```

# ============================================================
# Ubuntu 24.04 (Noble) + ROS 2 Jazzy
# TurtleBot3 Simulation (Gazebo Sim / gz-harmonic) - por SOURCE
# ============================================================

# 0) (Pré) Garanta que seu ROS 2 Jazzy já está instalado e carregado
```bash
source /opt/ros/jazzy/setup.bash
```
# 1) Instalar Gazebo Sim (Harmonic) via repositório OSRF (Gazebo Sim)
# (comandos do Quick Start do TurtleBot3 para Ubuntu 24.04 + Jazzy)
```bash
sudo apt-get update
sudo apt-get install -y curl lsb-release gnupg
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install -y gz-harmonic
# Fonte: Quick Start (Jazzy) :contentReference[oaicite:2]{index=2}
```
# 2) Criar workspace do TurtleBot3 e clonar os pacotes principais (branch jazzy)
```bash
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src

git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
```
# Fonte: Quick Start (Jazzy) :contentReference[oaicite:3]{index=3}

# 3) Clonar as simulações (branch jazzy) e buildar tudo
```bash
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
```
# Fonte: Simulation (Jazzy) :contentReference[oaicite:4]{index=4}
```bash
cd ~/turtlebot3_ws
```
# 4) (Recomendado) instalar dependências do workspace via rosdep
# (se você já usa rosdep no PC, pode pular o "init")
```bash
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths src -i -y
```
# 5) Build
```bash
sudo apt install -y python3-colcon-common-extensions
colcon build --symlink-install
```
# 6) Source do workspace
```bash
source ~/turtlebot3_ws/install/setup.bash
```
# 7) Rodar a simulação (3 mundos disponíveis)
# Empty World:
```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
```
# (alternativas)
# export TURTLEBOT3_MODEL=waffle
# ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
#
# export TURTLEBOT3_MODEL=waffle_pi
# ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
# Fonte: Simulation (Jazzy) :contentReference[oaicite:5]{index=5}
