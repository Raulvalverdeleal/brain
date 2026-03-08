#!/usr/bin/env python3
"""
Busca archivos SKILL.md en un directorio que NO tengan
las propiedades requeridas en el frontmatter YAML.

Uso:
    python3 check_skills.py [directorio] [--props prop1 prop2 ...]

Ejemplos:
    python3 check_skills.py /mnt/skills
    python3 check_skills.py /mnt/skills --props name description dependencies
    python3 check_skills.py . --props name description
"""

import os
import sys
import argparse

# Propiedades requeridas por defecto
DEFAULT_REQUIRED = ["name", "description"]


def parse_frontmatter(filepath):
    """Extrae las propiedades del frontmatter YAML de un archivo Markdown."""
    props = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        return None, f"No se pudo leer: {e}"

    if not lines or lines[0].strip() != "---":
        return props, "Sin frontmatter (no empieza con ---)"

    in_frontmatter = False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
                break  # Fin del bloque frontmatter
        # Parseo simple clave: valor (no soporta YAML anidado)
        if ":" in stripped:
            key = stripped.split(":", 1)[0].strip()
            if key:
                props[key] = True

    return props, None


def find_skill_files(root_dir):
    """Encuentra todos los archivos SKILL.md recursivamente."""
    skill_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.upper() == "SKILL.MD":
                skill_files.append(os.path.join(dirpath, filename))
    return sorted(skill_files)


def check_skills(root_dir, required_props):
    """Busca skills con propiedades faltantes y devuelve los resultados."""
    skill_files = find_skill_files(root_dir)

    if not skill_files:
        print(f"⚠️  No se encontraron archivos SKILL.md en: {root_dir}")
        return

    print(f"📂 Directorio: {os.path.abspath(root_dir)}")
    print(f"🔍 Propiedades requeridas: {', '.join(required_props)}")
    print(f"📄 Archivos SKILL.md encontrados: {len(skill_files)}")
    print("-" * 60)

    issues_found = 0

    for filepath in skill_files:
        props, error = parse_frontmatter(filepath)
        relative = os.path.relpath(filepath, root_dir)

        if error:
            print(f"❌ {relative}")
            print(f"   └─ Error: {error}")
            issues_found += 1
            continue

        missing = [p for p in required_props if p not in props]

        if missing:
            print(f"⚠️  {relative}")
            print(f"   └─ Faltan: {', '.join(missing)}")
            issues_found += 1

    print("-" * 60)
    if issues_found == 0:
        print(f"✅ Todos los {len(skill_files)} archivos tienen las propiedades requeridas.")
    else:
        ok = len(skill_files) - issues_found
        print(f"📊 Resultado: {issues_found} con problemas / {ok} correctos / {len(skill_files)} total")


def main():
    parser = argparse.ArgumentParser(
        description="Verifica propiedades de frontmatter en archivos SKILL.md"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directorio raíz donde buscar (por defecto: directorio actual)"
    )
    parser.add_argument(
        "--props",
        nargs="+",
        default=DEFAULT_REQUIRED,
        metavar="PROP",
        help=f"Propiedades requeridas (por defecto: {' '.join(DEFAULT_REQUIRED)})"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"❌ Error: '{args.directory}' no es un directorio válido.")
        sys.exit(1)

    check_skills(args.directory, args.props)


if __name__ == "__main__":
    main()