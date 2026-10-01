"""Funcoes testaveis sem ROS: quaternions e persistencia sem sobrescrita."""
import math
from pathlib import Path
import re
import yaml


def yaw_to_quaternion(yaw: float) -> tuple[float, float]:
    if not math.isfinite(yaw):
        raise ValueError('yaw deve ser finito')
    return math.sin(yaw / 2.0), math.cos(yaw / 2.0)


def quaternion_to_yaw(x: float, y: float, z: float, w: float) -> float:
    values = (x, y, z, w)
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Quaternion nao finito')
    norm = math.sqrt(sum(v * v for v in values))
    if norm < 1e-12:
        raise ValueError('Quaternion nulo')
    x, y, z, w = (v / norm for v in values)
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def valid_label(label: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}', label)) and label != 'end'


def save_spots(output: Path, records: dict, frame: str, base: str) -> tuple[Path, Path]:
    """Cria YAML e TXT novos. Remove apenas os arquivos criados nesta tentativa."""
    if not records:
        raise ValueError('Nenhuma posicao gravada')
    output = Path(output).expanduser()
    if output.suffix not in ('.yaml', '.yml'):
        raise ValueError('output_file deve terminar em .yaml ou .yml')
    text_path = output.with_suffix('.txt')
    data = {'schema_version': 1, 'frame_id': frame, 'base_frame_id': base, 'spots': records}
    text = '# label x y yaw qx qy qz qw (metros, radianos)\n'
    for label, record in records.items():
        if not valid_label(label):
            raise ValueError('Etiqueta invalida: ' + label)
        p, q = record['position'], record['orientation']
        vals = [p['x'], p['y'], record['yaw'], q['x'], q['y'], q['z'], q['w']]
        if not all(math.isfinite(v) for v in vals):
            raise ValueError('Pose nao finita')
        text += label + ' ' + ' '.join(format(v, '.9g') for v in vals) + '\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for path, content in [(output, yaml.safe_dump(data, sort_keys=False)), (text_path, text)]:
            with path.open('x', encoding='utf-8') as handle:
                created.append(path)
                handle.write(content)
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return output, text_path
