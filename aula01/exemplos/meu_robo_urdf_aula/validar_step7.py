#!/usr/bin/env python3
"""Verificação estrutural offline. Não substitui urdfdom/RViz ou teste físico."""
from __future__ import annotations
import ast
import math
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def number(raw: str | None) -> float:
    require(raw is not None, "Valor numérico ausente")
    value = float(raw)
    require(math.isfinite(value), f"Valor não finito: {raw}")
    return value


def validate(base: Path) -> None:
    model = base / "urdf" / "simple_robot_step7.urdf"
    tree = ET.parse(model).getroot()
    require(tree.tag == "robot", "Elemento raiz não é robot")
    links = {element.attrib["name"]: element for element in tree.findall("link")}
    joints = {element.attrib["name"]: element for element in tree.findall("joint")}
    require(len(links) == len(tree.findall("link")), "Nomes de links duplicados")
    require(len(joints) == len(tree.findall("joint")), "Nomes de juntas duplicados")
    parents: dict[str, str] = {}
    for name, joint in joints.items():
        parent = joint.find("parent").attrib["link"]
        child = joint.find("child").attrib["link"]
        require(parent in links and child in links, f"Referência inválida: {name}")
        require(child not in parents, f"Link tem mais de um pai: {child}")
        parents[child] = parent
        kind = joint.attrib["type"]
        require(kind in {"fixed", "revolute", "continuous", "prismatic"}, f"Tipo inesperado: {kind}")
        if kind != "fixed":
            axis = [number(v) for v in joint.find("axis").attrib["xyz"].split()]
            require(len(axis) == 3 and math.isclose(sum(v*v for v in axis), 1.0), f"Eixo inválido: {name}")
            limit = joint.find("limit")
            require(limit is not None, f"Limite ausente: {name}")
            require(number(limit.get("effort")) > 0 and number(limit.get("velocity")) > 0, f"Limites inválidos: {name}")
            if kind in {"revolute", "prismatic"}:
                lower, upper = number(limit.get("lower")), number(limit.get("upper"))
                require(lower < upper, f"Intervalo inválido: {name}")
                safety = joint.find("safety_controller")
                if safety is not None:
                    require(lower <= number(safety.get("soft_lower_limit")) < number(safety.get("soft_upper_limit")) <= upper, f"Limites suaves inválidos: {name}")
        mimic = joint.find("mimic")
        if mimic is not None:
            source = mimic.get("joint")
            require(source in joints and source != name, f"Mimic inválido: {name}")
            require(joints[source].find("mimic") is None, "Esta demo espera uma dependência mimic sem encadeamento")
            require(joints[source].attrib["type"] == kind, "Tipos mimic incompatíveis")
    roots = set(links) - set(parents)
    require(roots == {"base_link"}, f"Raiz inesperada: {roots}")
    for start in links:
        seen = set()
        current = start
        while current in parents:
            require(current not in seen, f"Ciclo na árvore: {start}")
            seen.add(current)
            current = parents[current]
        require(current == "base_link", f"Link desconectado: {start}")

    physical = 0
    for name, link in links.items():
        for geom in link.findall(".//geometry"):
            shape = list(geom)[0]
            if shape.tag == "box":
                values = [number(v) for v in shape.get("size").split()]
                require(len(values) == 3 and all(v > 0 for v in values), f"Caixa inválida: {name}")
            elif shape.tag == "cylinder":
                require(number(shape.get("radius")) > 0 and number(shape.get("length")) > 0, f"Cilindro inválido: {name}")
            else:
                raise ValueError(f"Geometria externa/inesperada: {shape.tag}")
        if link.find("visual") is None:
            continue
        physical += 1
        require(link.find("collision") is not None, f"Colisão ausente: {name}")
        inertial = link.find("inertial")
        require(inertial is not None, f"Inércia ausente: {name}")
        require(number(inertial.find("mass").get("value")) > 0, f"Massa inválida: {name}")
        tensor = inertial.find("inertia")
        a, b, c = [number(tensor.get(k)) for k in ("ixx", "iyy", "izz")]
        d, e, f = [number(tensor.get(k)) for k in ("ixy", "ixz", "iyz")]
        require(a > 0 and a*b-d*d > 0 and a*b*c+2*d*e*f-a*f*f-b*e*e-c*d*d > 0, f"Tensor não positivo definido: {name}")
        require(a+b >= c-1e-12 and a+c >= b-1e-12 and b+c >= a-1e-12, f"Desigualdade de inércia inválida: {name}")

    control = tree.find("ros2_control")
    require(control is not None, "Extensão didática ros2_control ausente")
    for joint in control.findall("joint"):
        name = joint.get("name")
        require(name in joints, f"ros2_control referencia junta inexistente: {name}")
        if joints[name].find("mimic") is not None:
            require(joint.find("command_interface") is None, "Mimic não deve ter comando independente")
    for trans in control.findall("transmission"):
        require(trans.find("joint").get("name") in joints, "Junta de transmissão inexistente")
        require(number(trans.find("joint/mechanical_reduction").text) != 0, "Redução nula")
    movable = [j for j in joints.values() if j.get("type") != "fixed"]
    independent = [j for j in movable if j.find("mimic") is None]
    require(len(links) == 13 and len(joints) == 12 and len(independent) == 4, "Contagem diferente da demo")

    ast.parse((base / "launch/display_step7.launch.py").read_text(encoding="utf-8"))
    require((base / "rviz/step7.rviz").is_file(), "Configuração RViz ausente")
    print("OK: XML; nomes; árvore conectada; eixos; limites; mimic; geometrias; massas; inércias; referências de controle; sintaxe Python.")
    print(f"Modelo: {len(links)} links, {len(joints)} juntas, {physical} corpos com inércia, {len(independent)} juntas independentes + 1 mimic.")
    print("Não verificado por este teste: execução ROS/RViz, colisões entre corpos, física, hardware ou aplicação dos limites pelo controlador.")


if __name__ == "__main__":
    try:
        validate(Path(__file__).resolve().parent)
    except (ValueError, OSError, ET.ParseError, KeyError, AttributeError, SyntaxError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)
