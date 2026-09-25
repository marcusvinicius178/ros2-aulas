# Aula 01 — URDF Step 7: modelo completo para demonstração

Este passo não substitui os Steps 1 a 6. Ele adiciona um modelo final em URDF puro para fechar a aula mostrando vários elementos importantes em um único robô.

## Arquivos deste passo

- [URDF completo](urdf/simple_robot_step7.urdf)
- [Launch independente](launch/display_step7.launch.py)
- [Configuração RViz](rviz/step7.rviz)
- [Script para iniciar](iniciar_step7.bash)
- [Validador estrutural em Python](validar_step7.py)

## Executar direto do repositório da aula

Entre na pasta do pacote didático:

```bash
cd ~/ros2-aulas/aula01/exemplos/meu_robo_urdf_aula
```

Execute:

```bash
bash iniciar_step7.bash
```

O script carrega automaticamente Jazzy ou Humble, verifica pacotes essenciais, roda a validação estrutural e abre o RViz com `joint_state_publisher_gui`.

## Se quiser executar manualmente

Ubuntu 24.04 / Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ~/ros2-aulas/aula01/exemplos/meu_robo_urdf_aula/launch/display_step7.launch.py
```

Ubuntu 22.04 / Humble:

```bash
source /opt/ros/humble/setup.bash
ros2 launch ~/ros2-aulas/aula01/exemplos/meu_robo_urdf_aula/launch/display_step7.launch.py
```

## O que demonstrar

Na janela de sliders:

- mova `left_shoulder_joint` e `right_shoulder_joint`: juntas `revolute` com limites;
- mova `left_finger_joint`: garra `prismatic`; o outro dedo acompanha por `mimic`;
- mova `right_wrist_joint`: junta `continuous`;
- no RViz, habilite `TF` para mostrar os frames, incluindo `camera_optical_frame`.

## O que o URDF cobre

| Tema | Elementos no código |
|---|---|
| Aparência | `link`, `visual`, `geometry`, `material`, `origin` |
| Física | `collision`, `inertial`, `mass`, tensor `inertia` |
| Movimento | `joint`, `axis`, `fixed`, `revolute`, `continuous`, `prismatic` |
| Limites | `limit`, `lower`, `upper`, `effort`, `velocity`, `dynamics`, `safety_controller` |
| Acoplamento | `mimic`, `multiplier`, `offset` |
| Controle | bloco `ros2_control`, interfaces de comando e estado |
| Transmissão | `transmission`, `mechanical_reduction` 50:1 |
| Sensor | frame óptico e bloco `gazebo` de câmera |

## Explicação importante

O RViz visualiza a descrição do robô e mostra as transformadas geradas pelas juntas. Ele não simula torque, contato, engrenagem, câmera real ou física.

O bloco `ros2_control`, a `transmission` e a câmera Gazebo estão declarados para estudo e explicação em aula. O launch deste Step 7 não inicia `controller_manager`, Gazebo nem bridge de câmera.

Frase de fechamento sugerida:

> O URDF descreve como o robô é construído. O RViz visualiza essa descrição. Controladores e simuladores são camadas separadas que executam o comportamento.
