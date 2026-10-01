# Aula 02 — correções, proveniência e limites

## Base e escopo

Material fornecido: `ROS2 Aula2.pptx`, 41 slides, capa com novembro de 2025. Revisão preparada em 1 de outubro de 2026 para Ubuntu 24.04 / ROS 2 Jazzy / Gazebo Harmonic.

Os slides continuam sendo a base pedagógica. Esta revisão adiciona arquivos completos e instruções de execução. Não altera o PowerPoint nem a Aula 01. Não implementa GPS: o slide 41 não fornece os passos e configurações necessários.

## Alterações explícitas

| Slides | Situação no material | Tratamento nesta revisão |
|---|---|---|
| 3–4 | Pacotes Jazzy junto de `GAZEBO_MODEL_PATH` | Demo Nav2 moderno; exercícios ROBOTIS Jazzy com `GZ_SIM_RESOURCE_PATH` |
| 4 e 14 | Dois lançadores diferentes ao longo da aula | Sessões separadas; instrução de encerrar a demo antes do SLAM |
| 11–14 | Arquivos em Pastebin; `init.py` | Implementação nova completa em `cartographer_slam`; `__init__.py`, resource e instalação dos launch/config |
| 14, 18, 19, 28 | Travessões Unicode em opções de CLI | `--packages-select`/`--packages-up-to` e `-f` com hífens ASCII |
| 14 | SLAM sem detalhe de publicação de ocupação no slide | Launch contém nó SLAM e nó `cartographer_occupancy_grid_node` |
| 15 | `origin` descrito como `(x,y,z)` | Esclarecido `[x,y,yaw]` para mapa 2D; não implica que pose do mapa seja pose no Gazebo |
| 16–19 | `map_server` criado no workspace; nomes de saída inconsistentes | Fontes em `src` via links; prefixo `turtlebot_area` consistente; caminho absoluto do YAML |
| 18, 30, 39 | `stamped:=true` sem conferir tipo | Mantido quando bridge usa TwistStamped; script detecta tipo real e recusa ambiguidade |
| 22–23 | Exemplo de manager com nós de navegação e `recoveries_server` | Managers específicos de cada exercício; apenas nós efetivamente iniciados |
| 23 | Pausa descrita como bloqueio da navegação | Distinção entre lifecycle do publicador e mapa/cache já recebido |
| 28 | Build seleciona `map_server` no exercício de localização | Build inclui `localization_server` e a dependência de interface |
| 34 | Tipo de movimento descrito como `differential` | YAML Jazzy usa `nav2_amcl::DifferentialMotionModel` |
| 35–36 | Coordenadas fixas dos exemplos e yaw confundível com z no comando | Pose manual no mapa atual; utilitário de quaternion; aviso de que AMCL não teletransporta robô |
| 37–40 | Serviço e gravador em Pastebin | Nova implementação com requisição label, resposta success/message e saída YAML + TXT documentada |
| 38 | Inclusão de `srv/` em `data_files` Python | Interface gerada por `spot_recorder_interfaces` com rosidl/ament_cmake; entrada Python em setup.py |

Workspace novo `~/ros2_aula02_ws` é uma decisão desta revisão para evitar sobrescrever exercícios já existentes em `~/ros2_ws`. Os quatro nomes de pacote foram preservados. Arquivos de dados ficam em `~/ros2_aula02_dados`, fora do código-fonte.

## Pastebins não recuperados

As URLs raw de todos os 15 IDs abaixo foram tentadas e não ficaram acessíveis pela ferramenta. Também foram tentadas as páginas normais de `zXSFCu8h`, `3FcvWtga` e `tc45GU0G`, sem sucesso. Isso não prova que os links estejam apagados: podem abrir no navegador do professor.

| ID/URL original | Arquivo indicado pelos slides |
|---|---|
| https://pastebin.com/BQHeEKHS | cartographer_slam/package.xml |
| https://pastebin.com/cFnuUB6D | cartographer_slam/setup.py |
| https://pastebin.com/zXSFCu8h | cartographer_slam/launch/cartographer.launch.py |
| https://pastebin.com/ajAUmhaH | cartographer_slam/config/cartographer.lua |
| https://pastebin.com/davr0dan | map_server/package.xml |
| https://pastebin.com/3VPrF9i3 | map_server/setup.py |
| https://pastebin.com/wqRpPvin | map_server/launch/map_server.launch.py |
| https://pastebin.com/wCbPtwAx | localization_server/setup.py |
| https://pastebin.com/HDmX2fLV | localization_server/launch/localization.launch.py |
| https://pastebin.com/SLDGyjQR | localization_server/config/amcl_config.yaml |
| https://pastebin.com/4Bh0e4KP | spot_recorder_interfaces/CMakeLists.txt |
| https://pastebin.com/DDmnHEB6 | spot_recorder_interfaces/package.xml |
| https://pastebin.com/tc45GU0G | spot_recorder_interfaces/srv/MyServiceMessage.srv |
| https://pastebin.com/3FcvWtga | localization_server/localization_server/spots_to_file.py |
| https://pastebin.com/g80pqzcm | localization_server/launch/spot_recorder.launch.py |

Não houve comparação linha a linha com esses originais. Em especial, só o campo de requisição `label` e a chamada com `end` estão visíveis nos slides; a resposta success/message e o formato detalhado de YAML/TXT foram definidos nesta revisão. Um leitor usado na Aula 03 deverá consumir esse contrato ou ser adaptado explicitamente.

## Referências oficiais consultadas

Compatibilidade de instalação:
- https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- https://docs.nav2.org/jazzy/getting_started/quickstart/quickstart/
- https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/gazebo/

Lançador Gazebo e tipo de mensagem, lidos no código-fonte da branch Jazzy:
- https://github.com/ROBOTIS-GIT/turtlebot3_simulations/blob/jazzy/turtlebot3_gazebo/launch/turtlebot3_world.launch.py — blob `1d2f1882ef81a88e0a9d0e7c1e55da3a3b05bdf3`: usa `ros_gz_sim`, posição inicial e recursos modernos.
- https://github.com/ROBOTIS-GIT/turtlebot3_simulations/blob/jazzy/turtlebot3_gazebo/launch/spawn_turtlebot3.launch.py — blob `2fca6d546863380e95c6dabf8858bd45eb5fbc4a`: carrega SDF e bridge específico do modelo.
- https://github.com/ROBOTIS-GIT/turtlebot3_simulations/blob/jazzy/turtlebot3_gazebo/params/turtlebot3_waffle_bridge.yaml — blob `7806de7a80ef177c786305010914ff96579500fa`: cmd_vel é `geometry_msgs/msg/TwistStamped`.

Teleop:
- https://github.com/ros2/teleop_twist_keyboard/blob/rolling/teleop_twist_keyboard.py — blob `a3b337dd247076b2813700db0514ac5af8a8a2ba`: parâmetro `frame_id` preenchido só é aceito com `stamped=true`. O script detector omite `frame_id` quando escolhe Twist. Essa leitura foi da branch rolling; a execução ainda deve ser confirmada na versão Jazzy instalada.

Cartographer, AMCL e RViz:
- https://github.com/ROBOTIS-GIT/turtlebot3/blob/jazzy/turtlebot3_cartographer/config/turtlebot3_lds_2d.lua — blob `ffedf92914f589f43d6467bd38bd4eeb6e430d77`: referência de configuração 2D. A configuração didática nova usa `base_footprint` para tracking sem IMU e não reproduz todas as opções de tuning desse arquivo.
- https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/others/configuring_amcl/ — frames, modelo diferencial, pose inicial e pesos do modelo laser.
- https://github.com/ros-navigation/navigation2/blob/jazzy/nav2_bringup/rviz/nav2_default_view.rviz — blob `c8dd37685833c1db4b83c62e4c2d124678f15ff1`; configuração RViz reutilizada diretamente do pacote instalado, não vendorizada.

Branches e páginas oficiais podem mudar. O script de diagnóstico registra versões realmente instaladas e o bridge local; a checagem de cmd_vel não depende de supor que a máquina já recebeu a mesma versão consultada.

## Testes e pendências

Executados no ambiente de preparação, sem ROS: 13 testes unittest de sintaxe/estrutura, seleção de argumentos do teleop com CLI simulado, contrato, parâmetros, quaternions e persistência. Python/Bash/XML/YAML verificados. Não foi executado parser Lua com Cartographer, geração rosidl, build colcon ou runtime ROS/Gazebo/RViz. As dependências binárias precisam ser instaladas e verificadas no Ubuntu 24.04 do laptop.

Não foram adicionados workflows que instalem ROS ou executem simulação no GitHub Actions. A branch/PR de revisão não equivale a uma aprovação para demonstração ao vivo. O checklist de aceitação está no fim do README.
