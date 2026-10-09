# Aula 02 — Nav2, mapeamento, localização e gravação de posições

**Ambiente-alvo: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic.**

Roteiro de execução baseado nos 41 slides iniciais de `ROS2 Aula2.pptx`, ampliados com exercícios práticos de AMCL, serviços e gravação de posições nos slides seguintes. Mantém a sequência da aula: demonstração Nav2, Cartographer, mapa salvo, map server/lifecycle, AMCL e gravação de posições. Os arquivos completos estão neste diretório; não é necessário copiar código do Pastebin.

> **Estado de validação:** o professor executou Cartographer, Map Server, AMCL, Gazebo, RViz e o serviço de posições em um notebook Jazzy, com os resultados descritos em [correções e fontes](CORRECOES_E_FONTES.md). Esta revisão do repositório alinha os exemplos com esse ensaio; ainda é necessário testar os arquivos revisados e suas dependências em outro computador. Não considerar a aula homologada apenas porque os testes de sintaxe passam.
>
> **Proveniência:** os links do Pastebin dos slides não puderam ser lidos nesta revisão. Os arquivos dependentes desses links são implementações novas, equivalentes ao exercício, não cópias recuperadas. O contrato de resposta do serviço e o formato dos arquivos de posições estão documentados aqui. Veja [correções e fontes](CORRECOES_E_FONTES.md).

## 1. Como usar este roteiro

Cada bloco é identificado pelo terminal em que deve ser executado. Comandos como `ros2 launch`, `rviz2` e teleop ficam executando: **não cole o próximo comando no mesmo terminal ocupado**. Use outro terminal ou encerre o processo indicado com `Ctrl+C`.

| Slides | Etapa deste roteiro |
|---|---|
| 3–5 | Instalação e demonstração pronta do Nav2 |
| 6–14 | Mapeamento, SLAM e pacote Cartographer |
| 15–19 | Salvar e carregar mapa |
| 20–23 | Lifecycle do map server |
| 24–34 | Localização AMCL e inspeção no RViz |
| 35–36 | Pose inicial pelo RViz, comando ou configuração |
| 37–40 | Serviço de gravação de posições |
| 41 | O slide só apresenta título/GPS e `colcon build`; não define um exercício GPS executável |

A demonstração pronta do Nav2 usa o simulador mínimo do Nav2. Os exercícios seguintes usam `turtlebot3_gazebo` da ROBOTIS, na versão Jazzy. **São duas sessões distintas: encerre a demonstração antes de iniciar o mapeamento.** Não combine os dois lançadores.

## 2. Obter o material sem mexer na cópia da Aula 01

### Terminal de preparação — clonar uma vez

Use uma pasta nova. Caso ela já exista, confira seu conteúdo em vez de apagá-la.

```bash
git clone --branch aula02-jazzy-2026-10-01 --single-branch \
  https://github.com/marcusvinicius178/ros2-aulas.git \
  "$HOME/ros2-aulas-aula02"
cd "$HOME/ros2-aulas-aula02"
```

Esta branch permite ensaiar sem alterar a `main`. Para atualizar uma cópia já clonada dessa branch:

```bash
git -C "$HOME/ros2-aulas-aula02" pull --ff-only
```

Se o Git reclamar de alterações locais, pare e confira `git status`; não use `reset --hard`.

### Conferir o laptop

```bash
bash "$HOME/ros2-aulas-aula02/aula02/scripts/00_diagnostico.bash"
```

Esperado: Ubuntu `24.04`, Jazzy em `/opt/ros/jazzy` e pacotes de simulação Jazzy. O diagnóstico não instala nada. Falta de pacotes antes da instalação é esperada. Não use `ros2 --version`: confira `echo "$ROS_DISTRO"` depois de carregar o ambiente.

### Instalar as dependências — antes da aula

Pré-requisito: ROS 2 Jazzy Desktop e repositório apt do ROS já configurados, conforme Aula 01. Não instalar pacotes Humble neste roteiro.

```bash
bash "$HOME/ros2-aulas-aula02/aula02/scripts/01_instalar.bash"
```

O script completo executa `apt update` e instala apenas as dependências declaradas; não executa atualização geral do Ubuntu e não altera `.bashrc`. Leia a lista do apt antes de confirmar. Execute hoje, não dependa da rede da sala amanhã.

### Preparar e compilar os quatro pacotes

```bash
bash "$HOME/ros2-aulas-aula02/aula02/scripts/02_preparar_workspace.bash"
```

O workspace é **`~/ros2_aula02_ws`**, separado de `~/ros2_ws`. O script cria links para os pacotes de `aula02/exemplos`, preserva os nomes dos slides e recusa substituir diretórios já existentes. Os arquivos não são copiados para dois lugares: editar os arquivos do repositório também altera a fonte vista pelo workspace.

Comando de compilação executado pelo script:

```bash
cd "$HOME/ros2_aula02_ws"
colcon build --symlink-install \
  --packages-up-to cartographer_slam map_server localization_server spot_recorder_interfaces \
  --event-handlers console_direct+
```

A dependência de `localization_server` em `spot_recorder_interfaces` determina a ordem de geração da interface. É necessário aparecer `Summary: 4 packages finished` sem falha. **Não avance em caso de erro de compilação.**

### Carregar o ambiente em CADA terminal novo

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
```

Esse comando define `AULA02_DIR`, `AULA02_WS`, `AULA02_DATA`, `TURTLEBOT3_MODEL=waffle` e descoberta ROS local à máquina. Usa domínio 42 quando `ROS_DOMAIN_ID` não estava definido. Todos os terminais precisam ter o mesmo domínio. Não usar este ambiente para conectar robôs físicos ou computadores de alunos entre si.

Não misture Conda/venv nem Humble/Jazzy no mesmo terminal. O script recusa Conda/venv e uma distribuição ROS diferente; ele não apaga overlays antigos. Confira a procedência dos pacotes:

```bash
echo "$ROS_DISTRO"
ros2 pkg prefix cartographer_slam
ros2 pkg prefix map_server
ros2 pkg prefix localization_server
ros2 interface show spot_recorder_interfaces/srv/MyServiceMessage
```

Os três prefixos devem apontar para `~/ros2_aula02_ws/install/...`, não para o workspace antigo. Se aparecer outro caminho, não continue até corrigir a ordem dos `source`.

## 3. Demonstração inicial: Nav2 pronto — slides 3–5

### Terminal A

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

Aguarde Gazebo e RViz. Confirme que o tempo da simulação avança. No RViz, use **2D Pose Estimate**: clique na posição real do robô e arraste para indicar sua orientação. Depois use **Nav2 Goal** em uma região livre e observe o planejamento e o movimento.

O `GAZEBO_MODEL_PATH` antigo dos slides não é necessário nesta demonstração do Gazebo moderno. Não lance outro `turtlebot3_world` junto. Esta etapa usa o mapa fornecido pelo Nav2, não o mapa que será criado abaixo.

### Terminal B — inspeção opcional da demonstração

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 node list
ros2 lifecycle get /amcl
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 action list -t
```

Observe os nós e ações. Planejador, controlador e BT compõem a navegação; map server e AMCL, isoladamente, não fazem o robô seguir um objetivo.

**Transição obrigatória:** cancele o objetivo no RViz, encerre o lançamento do Terminal A com `Ctrl+C` e confira o encerramento do Gazebo/RViz. Só então inicie a sessão seguinte. Não use `killall` indiscriminadamente.

## 4. Mapeamento com Cartographer — slides 6–14

### Terminal A — somente o simulador ROBOTIS

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
export GZ_SIM_RESOURCE_PATH="$(ros2 pkg prefix --share turtlebot3_gazebo)/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py \
  use_sim_time:=true x_pose:=-2.0 y_pose:=-0.5
```

Apesar do nome do pacote, sua branch Jazzy utiliza `ros_gz_sim`, não Gazebo Classic. `GZ_SIM_RESOURCE_PATH` é exportado antes do lançamento para disponibilizar os modelos locais. Deixe o simulador aberto durante as próximas etapas.

### Terminal B — verificar sensores antes de mapear

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 topic list -t
ros2 topic echo /clock --once
ros2 topic echo /scan --once --qos-reliability best_effort
ros2 topic echo /odom --once --qos-reliability best_effort
```

Esperado: mensagens de `/clock`, `/scan` e `/odom`. `echo --once` espera uma mensagem; se ficar parado, interrompa com `Ctrl+C` e investigue a simulação/bridge antes de seguir.

No mesmo Terminal B, após os comandos anteriores terminarem:

```bash
ros2 launch cartographer_slam cartographer.launch.py use_sim_time:=true
```

O launch contém **dois nós**: `cartographer_node` e `cartographer_occupancy_grid_node`. O segundo publica `/map`, necessário ao RViz e ao salvamento.

Nesta configuração, a simulação publica `odom -> base_footprint`; Cartographer publica `map -> odom`. Não iniciar AMCL ao mesmo tempo. IMU não é exigida por este exercício 2D; `/scan`, `/odom` e as transformações do robô são necessários.

### Terminal C — RViz

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
rviz2 -d "$(ros2 pkg prefix --share nav2_bringup)/rviz/nav2_default_view.rviz" \
  --ros-args -p use_sim_time:=true
```

Use `Fixed Frame = map`. Confira o display do mapa (`/map`) e do laser (`/scan`, confiabilidade **Best Effort**). Habilite `RobotModel`, com descrição em `/robot_description`; se o modelo não chegar, selecione durabilidade **Transient Local** nesse tópico. O painel de navegação não ficará operacional nesta sessão: ainda não lançamos os servidores de planejamento e controle.

### Terminal D — teleop

```bash
bash "$HOME/ros2-aulas-aula02/aula02/scripts/03_teleop.bash"
```

O script lê o tipo real de `/cmd_vel` e escolhe `stamped:=true` para `TwistStamped` ou `false` para `Twist`. Se houver nenhum ou mais de um tipo, ele para, em vez de tentar comandar pelo tipo errado. Não execute junto com o Nav2 enviando velocidades.

Mantenha o foco neste terminal. Use `i` para frente, `j`/`l` para girar e **`k` para parar**. Não suponha que soltar a tecla sempre pare o robô. Comece devagar; o script solicita velocidade linear 0,15 m/s e angular 0,5 rad/s. Explore os corredores livres, contorne obstáculos e retorne a regiões já observadas.

Para mostrar o comando explícito em aula, antes confira em outro terminal:

```bash
ros2 topic type /cmd_vel
ros2 topic info /cmd_vel --verbose
```

No simulador Jazzy ROBOTIS consultado, o bridge declara `geometry_msgs/msg/TwistStamped`. Nesse caso, o comando equivalente é:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
  -p stamped:=true -p use_sim_time:=true -p frame_id:=base_footprint \
  -p speed:=0.15 -p turn:=0.5
```

Use apenas **um** teleop. Em uma instalação cujo tópico realmente seja `Twist`, use o script detector: ele também omite `frame_id`, pois o teleop só aceita esse parâmetro preenchido quando `stamped:=true`. Não basta trocar somente o valor de `stamped` no comando acima.

## 5. Salvar o mapa — slides 15 e 18

No Terminal D, pare o robô com `k`. Mantenha Gazebo, Cartographer e RViz abertos.

### Terminal E

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
mkdir -p "$AULA02_DATA/mapas"
ros2 run nav2_map_server map_saver_cli \
  -f "$AULA02_DATA/mapas/turtlebot_area" \
  --ros-args -p use_sim_time:=true -p save_map_timeout:=60.0
ls -lh "$AULA02_DATA/mapas/turtlebot_area."*
cat "$AULA02_DATA/mapas/turtlebot_area.yaml"
```

Deve haver `turtlebot_area.yaml` e a imagem indicada na chave `image` do YAML, normalmente `turtlebot_area.pgm`. O nome é consistente: não procurar `area_do_turtlebot`.

O Cartographer ensaiado publicou /map com QoS RELIABLE e TRANSIENT_LOCAL. O map_saver_cli pode solicitar esse perfil; o timeout foi elevado para 60 s porque o simulador estava lento. Confira com `ros2 topic info -v /map`. Se outro publicador oferecer apenas durabilidade VOLATILE, adicione `-p map_subscribe_transient_local:=false`. Aguarde a mensagem de sucesso antes de encerrar o SLAM.

**Atenção:** repetir o salvamento com o mesmo prefixo pode sobrescrever o mapa anterior. Para preservar um ensaio, use outro prefixo e passe o respectivo YAML nas etapas seguintes. O mapa salvo contém ocupação, não é um checkpoint `.pbstream` para retomar Cartographer.

No YAML, `resolution` é metros por pixel e `origin` é `[x, y, yaw]`, não `[x, y, z]`. Coordenadas do mapa gerado não precisam coincidir com as coordenadas do mundo do Gazebo.

**Antes de sair do mapeamento:** observe onde o robô está no mapa do RViz. Essa é a região em que você inicializará AMCL. Pare teleop com `k` e depois `Ctrl+C` no Terminal D; encerre Cartographer com `Ctrl+C` no Terminal B. **Mantenha o simulador A e o RViz C abertos.**

## 6. Carregar mapa e estudar lifecycle — slides 16–23

### Terminal B — map server isolado

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 launch map_server map_server.launch.py \
  map:="$AULA02_DATA/mapas/turtlebot_area.yaml" use_sim_time:=true
```

`map_server` é o nome do pacote didático. O executável de publicação vem de `nav2_map_server`. O launch ativa apenas esse nó, por meio de `lifecycle_manager_mapper`.

### Terminal E — consultar, pausar e retomar

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 lifecycle get /map_server
ros2 service list | grep lifecycle
ros2 interface show nav2_msgs/srv/ManageLifecycleNodes
ros2 service call /lifecycle_manager_mapper/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes "{command: 1}"
ros2 lifecycle get /map_server
```

Esperado: estado `active` antes da pausa e `inactive` depois dela. Para retomar:

```bash
ros2 service call /lifecycle_manager_mapper/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes "{command: 2}"
ros2 lifecycle get /map_server
```

**O mapa pode continuar visível no RViz depois da pausa:** o display guarda a mensagem recebida. A pausa não apaga o mapa já entregue nem garante, sozinha, que outro sistema pare de navegar. O resultado deste exercício é observado no estado lifecycle e nas respostas dos serviços.

Como Cartographer foi encerrado e AMCL ainda não começou, a transformação `map -> odom` não está sendo atualizada. Falta de alinhamento do robô/laser nesta etapa isolada não significa que o map server falhou.

**Transição:** encerre o map server do Terminal B com `Ctrl+C`. O próximo launch já inclui outro map server e seu gerenciador; não deixe dois nós com o mesmo nome.

## 7. Localizar com AMCL — slides 24–34

### Terminal B

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 launch localization_server localization.launch.py \
  map:="$AULA02_DATA/mapas/turtlebot_area.yaml" use_sim_time:=true
```

Agora são iniciados map server, AMCL e `lifecycle_manager_localization`. Não existe `recoveries_server` nesse launch e não são gerenciados servidores que não foram iniciados.

### Terminal E — verificação

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 param get /amcl use_sim_time
ros2 param get /amcl robot_model_type
```

Esperado: ambos `active`, relógio de simulação `True` e `nav2_amcl::DifferentialMotionModel`.

No RViz C, use **2D Pose Estimate** na posição atual do robô no **mapa salvo** e arraste para indicar a orientação. Não use `Nav2 Goal` como substituto da pose inicial. Habilite a nuvem de partículas no display Nav2 correspondente a `/particle_cloud`; confira o tipo do tópico quando adicionar o display manualmente. Não assumir que esse tópico é `geometry_msgs/PoseArray`.

### Terminal D — melhorar a estimativa por movimento

```bash
bash "$HOME/ros2-aulas-aula02/aula02/scripts/03_teleop.bash"
```

Gire e desloque o robô lentamente em região livre. Observe o alinhamento dos pontos do laser às paredes do mapa e a concentração das partículas. A concentração sozinha não prova que a pose está correta; confira a consistência geométrica.

### Terminal E — inspecionar TF e estimativa

```bash
ros2 topic echo /amcl_pose --once
ros2 run tf2_ros tf2_echo map base_footprint
```

O segundo comando fica executando; encerre com `Ctrl+C` antes do próximo exercício. Guarde `x`, `y` e o yaw em **radianos** da pose estimada. Não confunda yaw com `position.z`.

## 8. Pose inicial por comando ou configuração — slides 35–36

### 8.1 Publicação com quaternion correto

Pare o robô. Substitua os três valores abaixo pelos valores que acabou de observar no frame `map`. O exemplo **não afirma** que `(0, 0, 0)` seja a pose atual correta.

```bash
ros2 run localization_server set_initial_pose 0.0 0.0 0.0 \
  --ros-args -p use_sim_time:=true
```

O script completo espera relógio/assinante por até 10 segundos, publica `PoseWithCovarianceStamped`, preenche covariance e calcula `orientation.z=sin(yaw/2)` e `orientation.w=cos(yaw/2)`. `position.z` permanece zero neste exemplo planar.

### 8.2 Inicialização automática pelo arquivo

Arquivo completo: [amcl_config.yaml](exemplos/localization_server/config/amcl_config.yaml).

**Local exato da edição:** dentro do bloco `amcl: -> ros__parameters:`, troque `set_initial_pose: false` por `set_initial_pose: true`. No bloco `initial_pose:` imediatamente abaixo, coloque os `x`, `y` e `yaw` medidos no seu mapa; preserve `z: 0.0`. Edite o arquivo inteiro no caminho:

```bash
nano "$AULA02_DIR/exemplos/localization_server/config/amcl_config.yaml"
```

Encerre o launch de localização B, mantenha o robô parado no simulador e recompile a configuração antes de relançar:

```bash
cd "$AULA02_WS"
colcon build --symlink-install --packages-up-to localization_server
source "$AULA02_DIR/scripts/ambiente.bash"
ros2 launch localization_server localization.launch.py \
  map:="$AULA02_DATA/mapas/turtlebot_area.yaml" use_sim_time:=true
```

AMCL passará a iniciar na pose configurada. **Isso muda a hipótese do localizador, não teletransporta o robô.** Para reproduzir o segundo exemplo dos slides, uma pose deliberadamente errada pode ilustrar a inconsistência do filtro; não use as coordenadas antigas dos slides como verdade do seu mapa. Depois restaure uma pose correta pelo RViz/comando.

Para voltar ao exercício interativo, devolva `set_initial_pose` a `false` e repita build/relaunch.

### 8.3 Localização global, partículas e covariância (experimento 08/10/2026)

Com o AMCL e o mapa ativos, **2D Pose Estimate** envia uma hipótese local no tópico `/initialpose` (tipo `geometry_msgs/msg/PoseWithCovarianceStamped`). Outra alternativa é reinicializar as partículas pelo espaço livre do mapa, usando um serviço ROS 2:

```bash
ros2 service type /reinitialize_global_localization
ros2 interface show std_srvs/srv/Empty
ros2 service call /reinitialize_global_localization std_srvs/srv/Empty "{}"
```

O serviço usa request e response vazias. Uma resposta recebida **não garante** que a localização já tenha convergido. Movimente cuidadosamente o robô e acompanhe as observações do LiDAR.

Para visualizar as hipóteses, adicione no RViz o display **nav2_rviz_plugins/ParticleCloud** para `/particle_cloud` (tipo `nav2_msgs/msg/ParticleCloud` no Jazzy). `/amcl_pose` **não é PoseArray**: use um display `PoseWithCovariance`, pois o tipo é `geometry_msgs/msg/PoseWithCovarianceStamped`. O círculo/elipse roxo expressa incerteza em posição; a região angular amarela expressa incerteza em yaw.

```bash
ros2 topic list -t | grep -E '/particle_cloud|/amcl_pose'
ros2 topic info -v /particle_cloud
ros2 topic echo /amcl_pose --once --field pose.covariance
```

Se o RViz reclamar de QoS incompatível, confira as ofertas do tópico com `ros2 topic info -v`. Para o erro de locale `locale::facet::_S_create_c_locale`, desative Conda e teste `LC_ALL=C.UTF-8 LANG=C.UTF-8 rviz2 --ros-args -p use_sim_time:=true`. Não use simultaneamente Cartographer e AMCL como produtores de `map -> odom`.

## 9. Gravar posições para a próxima aula — slides 37–40 (versão ensaiada)

Mantenha Gazebo, AMCL, RViz e teleop ativos, mas pare o robô antes de registrar cada posição. O gravador principal **assina /amcl_pose** e só pode capturar um ponto depois de receber a primeira estimativa do AMCL. Como o AMCL Jazzy oferece `/amcl_pose` com **RELIABLE + TRANSIENT_LOCAL**, o subscriber do gravador usa o mesmo QoS para receber também a última pose publicada quando o nó é iniciado mais tarde. Isso não substitui a necessidade de localização válida e atualizada.

### Terminal E — gravador didático

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 launch localization_server spot_recorder.launch.py use_sim_time:=true
```

Esse launch passa o caminho absoluto `$HOME/ros2_aula02_dados/spots.txt` ao nó. A resposta e os logs mostram o nome do arquivo. Se executado diretamente com `ros2 run localization_server spots_to_file`, o padrão `spots.txt` será gravado no **diretório de trabalho do processo servidor**, não no terminal cliente.

### Terminal F — serviço

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 interface show spot_recorder_interfaces/srv/MyServiceMessage
ros2 topic echo /amcl_pose --once
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage "{label: 'left'}"
```

Após mover o robô para um segundo ponto, execute:

```bash
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage "{label: 'center'}"
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage "{label: 'end'}"
cat "$HOME/ros2_aula02_dados/spots.txt"
```

**Contrato da prática executada no notebook do professor:**

```text
string label
---
bool navigation_successfull
string message
```

`left` e `center` registram poses em memória; `end` escreve as poses com `x,y,z,qx,qy,qz,qw` em `spots.txt`. Receber `navigation_successfull: false` e `Nenhuma pose recebida ainda de /amcl_pose` significa que o AMCL ainda não forneceu posição. O gravador didático sobrescreve o TXT na próxima chamada `end`: faça backup antes de uma nova sessão se quiser preservá-lo.

**Se o gravador ainda disser "Nenhuma pose recebida":** confira se está no mesmo `ROS_DOMAIN_ID` do AMCL; execute `ros2 topic info -v /amcl_pose` e teste `ros2 topic echo /amcl_pose --once --qos-durability transient_local --qos-reliability reliable`. Se a pose estiver disponível, reinicie o gravador atualizado. Com o robô parado, também é possível solicitar uma nova atualização: `ros2 service call /request_nomotion_update std_srvs/srv/Empty "{}"`. Se nada for publicado, verifique `/scan`, `/clock` e `odom -> base_footprint -> base_scan`.

**Atenção:** a implementação de 01/10 usava `bool success` e gravação por TF. Esse contrato era incompatível com a resposta `navigation_successfull` efetivamente testada. Recompile `spot_recorder_interfaces` e `localization_server` e carregue o overlay atualizado.

### Variante avançada opcional — TF + YAML/TXT

A versão anterior, com validação de TF, carimbos de tempo e gravação sem sobrescrever, permanece disponível como `spots_to_file_tf.py` + `spot_recorder_tf.launch.py`, agora com o mesmo campo `navigation_successfull`:

```bash
ros2 launch localization_server spot_recorder_tf.launch.py use_sim_time:=true
```

Ela gera `~/ros2_aula02_dados/spots_DATA_HORA.yaml` e um TXT correspondente. **Não execute os dois gravadores juntos**, pois ambos oferecem o serviço `/record_spot`. Essa variante não foi testada no ensaio de hoje.


## 10. Arquivos completos e onde editar

| Arquivo | Função |
|---|---|
| [cartographer.launch.py](exemplos/cartographer_slam/launch/cartographer.launch.py) | Inicia SLAM e publicação de ocupação |
| [cartographer.lua](exemplos/cartographer_slam/config/cartographer.lua) | Frames, sensores e configuração SLAM 2D |
| [map_server.launch.py](exemplos/map_server/launch/map_server.launch.py) | Mapa e lifecycle isolados |
| [localization.launch.py](exemplos/localization_server/launch/localization.launch.py) | Mapa + AMCL + lifecycle |
| [amcl_config.yaml](exemplos/localization_server/config/amcl_config.yaml) | Parâmetros e pose inicial |
| [MyServiceMessage.srv](exemplos/spot_recorder_interfaces/srv/MyServiceMessage.srv) | Contrato do serviço |
| [spots_to_file.py](exemplos/localization_server/localization_server/spots_to_file.py) | Nó ensaiado que assina /amcl_pose e salva spots.txt |
| [pose_utils.py](exemplos/localization_server/localization_server/pose_utils.py) | Quaternions e saída YAML/TXT da variante avançada |
| [spot_recorder.launch.py](exemplos/localization_server/launch/spot_recorder.launch.py) | Inicia o gravador didático |
| [spots_to_file_tf.py](exemplos/localization_server/localization_server/spots_to_file_tf.py) | Variante avançada por TF |
| [spot_recorder_tf.launch.py](exemplos/localization_server/launch/spot_recorder_tf.launch.py) | Launch da variante avançada |
| [set_initial_pose.py](exemplos/localization_server/localization_server/set_initial_pose.py) | Publicação da pose pela linha de comando |

Os `package.xml`, `setup.py`, `setup.cfg`, `__init__.py`, marcadores `resource/` e `CMakeLists.txt` também estão completos em [exemplos](exemplos). O `setup.py` inclui a entrada didática `srv/*.srv` em `data_files` para mostrar como copiar recursos (mesmo se a pasta estiver vazia), **não para gerar a interface**. A geração real ocorre no pacote `spot_recorder_interfaces` com `rosidl_generate_interfaces()` e `ament_cmake`. Em `data_files`, cada entrada deve ser uma dupla `(destino, lista_de_arquivos)`; evite aninhar tuplas e caracteres invisíveis U+200B.

## 11. Problemas comuns

| Sintoma | Verificação e correção |
|---|---|
| `Package ... not found` | Faça build, carregue `ambiente.bash` no terminal e confira `ros2 pkg prefix` |
| `ModuleNotFoundError: spot_recorder_interfaces` | Compile com `--packages-up-to localization_server` e recarregue o overlay; não basta editar `setup.py` |
| Gazebo sem mundo/modelos | Confira pacote Jazzy, `GZ_SIM_RESOURCE_PATH` da etapa 4, log de spawn e bridge |
| `/clock` parado | Confira se o Gazebo está pausado ou se o bridge falhou; não comece AMCL sem clock |
| Robô não anda | Foque o terminal do teleop, confira assinantes/tipo de `/cmd_vel`; não misture Twist/TwistStamped |
| `/map` não aparece durante SLAM | Confira os dois nós Cartographer, `/scan`, `/odom`, TF e durabilidade do display |
| Erro de TF ou saltos da pose | Não rode Cartographer e AMCL simultaneamente; deve haver uma autoridade para `map -> odom` |
| Nós `unconfigured` | Leia o erro anterior de YAML/TF/mapa no launch; consulte o lifecycle manager correspondente à etapa |
| Mapa ainda visível após pausa | É cache do RViz; consulte o estado lifecycle para verificar a transição |
| Configuração parece não atualizar | Edite a fonte do repositório, recompile e relance; confira qual pacote está sendo usado |
| Gravador responde `navigation_successfull: false` | Leia `message`: primeiro espere o AMCL publicar /amcl_pose; na variante avançada confira também TF/clock |
| Janela gráfica falha | Guarde o log. Em outro terminal, tente `export QT_QPA_PLATFORM=xcb` antes de relançar a janela; isso é diagnóstico, não cura geral |

Não apague `~/ros2_ws`, não edite os pacotes em `/opt/ros/jazzy` e não atualize kernel/driver na véspera da aula para corrigir um erro de launch.

## 12. Checklist do ensaio no laptop

Antes de dar a aula, confirme: build dos quatro pacotes; demonstração Nav2 abre; somente uma sessão Gazebo ativa; clock/scan/odom chegando; robô responde e para no teleop; mapa salvo com imagem e YAML; pause/resume observado no lifecycle; AMCL ativo e laser alinhado; duas posições e `end` com `navigation_successfull: true`; spots.txt conferido. Guarde o mapa e a saída do diagnóstico.

Testes locais que não exigem ROS (exigem `python3-yaml`):

```bash
cd "$HOME/ros2-aulas-aula02"
python3 -m unittest discover -s aula02/tests -v
```

Eles verificam sintaxe Python/Bash, XML de pacotes, configuração AMCL, contrato do serviço, conversão de quaternion, etiquetas e escrita sem sobrescrita. **Não substituem colcon build nem o ensaio gráfico.**

## 13. Atualização pós-laboratório e transporte ao notebook do IPT

No ensaio do professor em 08/10/2026, Cartographer publicou `/map` como `OccupancyGrid` RELIABLE/TRANSIENT_LOCAL, o Map Server carregou `turtlebot_area.yaml`, AMCL localizou após `2D Pose Estimate`, e o serviço de gravação respondeu `navigation_successfull=True` para `left`, `center` e `end`. A versão **revisada no GitHub** ainda requer compilação e teste na máquina de destino.

O launch de localização aceita agora `map` opcional, com default `~/ros2_ws/src/map_server/maps/turtlebot_area.yaml` para quem acompanha a estrutura dos slides. Nesta branch que usa `~/ros2_aula02_ws`, continue indicando explicitamente o caminho do mapa salvo em `$AULA02_DATA`.

O `turtlebot_area.yaml` e o `.pgm` foram gerados no notebook, portanto **não acompanham os códigos no GitHub**. Transfira os dois arquivos para o IPT, confira que o YAML referencia a imagem correta e ajuste `map:=/caminho/absoluto/mapa.yaml` quando necessário. Não transfira `build/`, `install/` ou `log/`; recompile as fontes.

Depois de atualizar essa branch no notebook:

```bash
cd "$AULA02_WS"
colcon build --base-paths src --packages-up-to localization_server --symlink-install
source "$AULA02_DIR/scripts/ambiente.bash"
ros2 interface show spot_recorder_interfaces/srv/MyServiceMessage
```

O serviço instalado deve mostrar `bool navigation_successfull`. Se mostrar `bool success`, confira `ros2 pkg prefix spot_recorder_interfaces`: pode haver um overlay antigo no terminal.
