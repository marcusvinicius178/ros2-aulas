# Aula 02 — Nav2, mapeamento, localização e gravação de posições

**Ambiente-alvo: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic.**

Roteiro de execução baseado nos 41 slides de `ROS2 Aula2.pptx`. Mantém a sequência da aula: demonstração Nav2, Cartographer, mapa salvo, map server/lifecycle, AMCL e gravação de posições. Os arquivos completos estão neste diretório; não é necessário copiar código do Pastebin.

> **Estado de validação:** testes locais de sintaxe, estrutura e funções auxiliares executados. A compilação ROS, o Gazebo, o RViz e a demonstração completa ainda precisam ser ensaiados no laptop. Não considerar a aula homologada apenas porque os testes sem ROS passaram.
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
  --ros-args -p use_sim_time:=true -p save_map_timeout:=15.0 \
  -p map_subscribe_transient_local:=false
ls -lh "$AULA02_DATA/mapas/turtlebot_area."*
cat "$AULA02_DATA/mapas/turtlebot_area.yaml"
```

Deve haver `turtlebot_area.yaml` e a imagem indicada na chave `image` do YAML, normalmente `turtlebot_area.pgm`. O nome é consistente: não procurar `area_do_turtlebot`.

Para Cartographer, o assinante do salvamento usa durabilidade volátil explicitamente: ele pode receber o próximo mapa periódico tanto de um publicador volátil quanto de um transient-local. Aguarde a mensagem de sucesso antes de encerrar o SLAM.

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

## 9. Gravar posições para a próxima aula — slides 37–40

Mantenha A (simulação), B (localização), C (RViz) e D (teleop) ativos. Pare o robô antes de cada captura.

### Terminal E — gravador

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 launch localization_server spot_recorder.launch.py use_sim_time:=true
```

O log mostra o caminho de saída, por exemplo `~/ros2_aula02_dados/spots_DATA_HORA.yaml`. Cada sessão usa um nome novo. Espere alguns segundos para o listener receber TF.

### Terminal F — serviço

```bash
source "$HOME/ros2-aulas-aula02/aula02/scripts/ambiente.bash"
ros2 interface show spot_recorder_interfaces/srv/MyServiceMessage
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage \
  "{label: 'center'}"
```

No Terminal D, mova até outro local e pare com `k`. No F:

```bash
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage \
  "{label: 'left'}"
ros2 service call /record_spot spot_recorder_interfaces/srv/MyServiceMessage \
  "{label: 'end'}"
ls -lt "$AULA02_DATA"/spots_*
```

Cada chamada deve responder `success: true`. A etiqueta é só um nome: `center`/`left` não mandam o robô se mover. `end` salva um **YAML estruturado** e um **TXT legível**, cujos caminhos aparecem na resposta. Antes de `end`, as posições estão apenas em memória. Não feche o gravador sem salvar.

O novo serviço mantém a requisição `string label` mostrada nos slides. Sua resposta nesta implementação é `bool success` + `string message`; não foi possível confirmar a resposta do Pastebin original. Os arquivos de saída também são um contrato novo e explícito, não uma garantia de compatibilidade com um leitor antigo da próxima aula.

O YAML contém `schema_version`, `frame_id`, `base_frame_id` e um dicionário `spots`, com posição, quaternion, yaw e timestamp por etiqueta. O TXT contém colunas `label x y yaw qx qy qz qw`. O gravador lê a TF `map -> base_footprint`, rejeita TF velha, etiquetas duplicadas e sobrescrita de arquivo existente. Ele não faz navegação nem verifica sozinho a convergência do AMCL.

## 10. Arquivos completos e onde editar

| Arquivo | Função |
|---|---|
| [cartographer.launch.py](exemplos/cartographer_slam/launch/cartographer.launch.py) | Inicia SLAM e publicação de ocupação |
| [cartographer.lua](exemplos/cartographer_slam/config/cartographer.lua) | Frames, sensores e configuração SLAM 2D |
| [map_server.launch.py](exemplos/map_server/launch/map_server.launch.py) | Mapa e lifecycle isolados |
| [localization.launch.py](exemplos/localization_server/launch/localization.launch.py) | Mapa + AMCL + lifecycle |
| [amcl_config.yaml](exemplos/localization_server/config/amcl_config.yaml) | Parâmetros e pose inicial |
| [MyServiceMessage.srv](exemplos/spot_recorder_interfaces/srv/MyServiceMessage.srv) | Contrato do serviço |
| [spots_to_file.py](exemplos/localization_server/localization_server/spots_to_file.py) | Nó gravador |
| [pose_utils.py](exemplos/localization_server/localization_server/pose_utils.py) | Quaternions e salvamento YAML/TXT |
| [spot_recorder.launch.py](exemplos/localization_server/launch/spot_recorder.launch.py) | Inicia o gravador |
| [set_initial_pose.py](exemplos/localization_server/localization_server/set_initial_pose.py) | Publicação da pose pela linha de comando |

Os `package.xml`, `setup.py`, `setup.cfg`, `__init__.py`, marcadores `resource/` e `CMakeLists.txt` também estão completos em [exemplos](exemplos). Não acrescente `srv/` aos `data_files` do pacote Python: a interface é gerada pelo pacote `ament_cmake` próprio.

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
| Gravador responde `success: false` | Leia `message`; espere TF, confira AMCL/clock e use etiqueta nova |
| Janela gráfica falha | Guarde o log. Em outro terminal, tente `export QT_QPA_PLATFORM=xcb` antes de relançar a janela; isso é diagnóstico, não cura geral |

Não apague `~/ros2_ws`, não edite os pacotes em `/opt/ros/jazzy` e não atualize kernel/driver na véspera da aula para corrigir um erro de launch.

## 12. Checklist do ensaio no laptop

Antes de dar a aula, confirme: build dos quatro pacotes; demonstração Nav2 abre; somente uma sessão Gazebo ativa; clock/scan/odom chegando; robô responde e para no teleop; mapa salvo com imagem e YAML; pause/resume observado no lifecycle; AMCL ativo e laser alinhado; duas posições e `end` com `success: true`; YAML/TXT conferidos. Guarde o mapa e a saída do diagnóstico.

Testes locais que não exigem ROS (exigem `python3-yaml`):

```bash
cd "$HOME/ros2-aulas-aula02"
python3 -m unittest discover -s aula02/tests -v
```

Eles verificam sintaxe Python/Bash, XML de pacotes, configuração AMCL, contrato do serviço, conversão de quaternion, etiquetas e escrita sem sobrescrita. **Não substituem colcon build nem o ensaio gráfico.**
