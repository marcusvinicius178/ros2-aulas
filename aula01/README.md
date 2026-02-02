# Aula 01

## Objetivo
- Instalar e configurar ferramentas de desenvolimento do ROS2

## Pré-requisitos
- Ubuntu 22.04 ou 24.04
- Terminal
- Internet

## Comandos para UBUNTU 22.04 (jammy)

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

### Instalação do Desktop (Recomendada): ROS; Rviz; Demos, Tutoriais
```bash 
sudo apt install ros-humble-desktop
```
### Ferramentas de desenvolvimento: Compiladores e outras ferramentas para buildar os pacotes ROS
```
sudo apt install ros-dev-tools
```

### Configurando o Ambiente 
### Configure o ambiente obtendo o seguinte arquivo

```bash
source /opt/ros/humble/setup.bash
```

### Edite o arquivo .bashrc adicionando a linha acima ("source /opt/ros/humble/setup.bash") na última linha deste arquivo. 




## Notas
- (preencha aqui)
