#!/usr/bin/env python3
"""Extrae miembros sueltos de un .zip remoto (aunque esté partido en trozos)
con peticiones HTTP Range, sin descargar el archivo completo.

Un .zip es de acceso aleatorio: se lee su directorio central, se localiza el
miembro y se transfieren solo sus bytes. Para BDD100K, el paquete de videos
pesa ~1,97 TB y el directorio central ~12,9 MB, de modo que extraer un clip
de 20 MB cuesta ~33 MB de tráfico en vez de ~1,97 TB.

Ejemplos
--------
Un miembro concreto:

  ./zipfetch.py --parts 19 --part-size 107374182400 --last-part-size 36420631858 \\
      --url "https://.../bdd100k_videos.zip.part-{i:05d}" \\
      --member "bdd100k/videos/100k/train/0000f77c-6257be58.mov" -o clip.mov

Los 10 primeros clips de la partición de entrenamiento (orden lexicográfico):

  ./zipfetch.py --parts 19 --part-size 107374182400 --last-part-size 36420631858 \\
      --url "https://.../bdd100k_videos.zip.part-{i:05d}" \\
      --match "^bdd100k/videos/100k/train/.*\\.mov$" --limit 10 -d ~/Downloads/BDD100K

También acepta `--member` varias veces para bajar una lista explícita.

Salida: `-o ARCHIVO` para un solo miembro, `-d DIRECTORIO` para varios (se usa
el nombre base de cada miembro). No sobrescribe archivos existentes del mismo
tamaño salvo con `--force`.
"""
import argparse
import os
import posixpath
import re
import struct
import subprocess
import sys
import zlib


class Remote:
    """Lectura por rangos sobre un archivo partido en trozos consecutivos."""

    def __init__(self, template, parts, part_size, last_part_size, verbose=True):
        self.template = template
        self.sizes = [part_size] * (parts - 1) + [last_part_size]
        self.off = [0]
        for s in self.sizes:
            self.off.append(self.off[-1] + s)
        self.total = self.off[-1]
        self.transferred = 0
        self.verbose = verbose

    def read(self, off, n):
        out = b""
        while n > 0:
            p = next(i for i in range(len(self.sizes))
                     if self.off[i] <= off < self.off[i + 1])
            inner = off - self.off[p]
            k = min(n, self.sizes[p] - inner)
            url = self.template.format(i=p)
            r = subprocess.run(
                ["curl", "-sL", "--max-time", "900", "-r",
                 f"{inner}-{inner + k - 1}", url], capture_output=True)
            if r.returncode != 0 or len(r.stdout) != k:
                sys.exit(f"fallo en {url} rango {inner}-{inner + k - 1}: "
                         f"{len(r.stdout)} de {k} bytes")
            out += r.stdout
            self.transferred += k
            off += k
            n -= k
        return out


def central_directory(rem):
    """Devuelve (buffer del directorio central, offset del directorio central)."""
    tail = rem.read(rem.total - (1 << 20), 1 << 20)
    loc = tail.rfind(b"PK\x06\x07")
    if loc > 0:
        z64_off = struct.unpack("<Q", tail[loc + 8:loc + 16])[0]
        z64 = rem.read(z64_off, 56)
        cd_size = struct.unpack("<Q", z64[40:48])[0]
        cd_off = struct.unpack("<Q", z64[48:56])[0]
    else:
        eocd = tail.rfind(b"PK\x05\x06")
        cd_size, cd_off = struct.unpack("<II", tail[eocd + 12:eocd + 20])
    return rem.read(cd_off, cd_size), cd_off


def entries(cd):
    """Recorre el directorio central: (nombre, método, tamaño, offset local)."""
    i = 0
    while i + 46 <= len(cd) and cd[i:i + 4] == b"PK\x01\x02":
        f = struct.unpack("<IHHHHHHIIIHHHHHII", cd[i:i + 46])
        method, csize, nlen, elen, clen, lho = (f[4], f[8], f[10], f[11],
                                                f[12], f[16])
        name = cd[i + 46:i + 46 + nlen].decode("utf-8", "replace")
        extra = cd[i + 46 + nlen:i + 46 + nlen + elen]
        j = 0
        while j < len(extra):                       # campos extra zip64
            eid, esz = struct.unpack("<HH", extra[j:j + 4])
            if eid == 1:
                vals, k = [], 0
                while k < esz:
                    vals.append(struct.unpack("<Q", extra[j + 4 + k:
                                                        j + 12 + k])[0])
                    k += 8
                if lho == 0xFFFFFFFF:
                    lho = vals.pop(0)
            j += 4 + esz
        yield name, method, csize, lho
        i += 46 + nlen + elen + clen


def extract(rem, name, method, csize, lho):
    head = rem.read(lho, 30)
    nlen, elen = struct.unpack("<HH", head[26:30])
    data = rem.read(lho + 30 + nlen + elen, csize)
    return zlib.decompress(data, -15) if method == 8 else data


def main():
    ap = argparse.ArgumentParser(
        description="Extrae miembros de un .zip remoto por HTTP Range.")
    ap.add_argument("--url", required=True,
                    help="plantilla del trozo, con {i:05d}. p. ej. "
                         "'https://host/paquete.zip.part-{i:05d}'")
    ap.add_argument("--parts", type=int, required=True)
    ap.add_argument("--part-size", type=int, required=True,
                    help="tamaño de cada trozo, salvo el último")
    ap.add_argument("--last-part-size", type=int, required=True)
    ap.add_argument("--member", action="append", default=[],
                    help="nombre exacto dentro del zip (repetible)")
    ap.add_argument("--match", help="expresión regular sobre el nombre completo")
    ap.add_argument("--limit", type=int, help="máximo de miembros con --match")
    ap.add_argument("-o", "--output", help="archivo de salida (un solo miembro)")
    ap.add_argument("-d", "--outdir", help="directorio de salida (varios)")
    ap.add_argument("--force", action="store_true",
                    help="sobrescribir aunque exista un archivo del mismo tamaño")
    a = ap.parse_args()

    if not a.member and not a.match:
        sys.exit("indica --member o --match")
    if (bool(a.output) == bool(a.outdir)):
        sys.exit("indica exactamente uno de -o / -d")

    rem = Remote(a.url, a.parts, a.part_size, a.last_part_size)
    cd, _ = central_directory(rem)
    index = list(entries(cd))

    if a.match:
        rx = re.compile(a.match)
        chosen = sorted((e for e in index if rx.search(e[0])),
                        key=lambda e: e[0])
        if a.limit:
            chosen = chosen[:a.limit]
    else:
        by_name = {e[0]: e for e in index}
        missing = [m for m in a.member if m not in by_name]
        if missing:
            sys.exit("no están en el zip: " + ", ".join(missing))
        chosen = [by_name[m] for m in a.member]

    if not chosen:
        sys.exit("la selección quedó vacía")

    if a.output and len(chosen) > 1:
        sys.exit(f"la selección tiene {len(chosen)} miembros: usa -d DIRECTORIO")

    if a.outdir:
        os.makedirs(a.outdir, exist_ok=True)

    for name, method, csize, lho in chosen:
        dest = a.output if a.output else os.path.join(
            a.outdir, posixpath.basename(name))
        if not a.force and os.path.exists(dest) and \
                os.path.getsize(dest) == csize:
            print(f"ya existe, se omite: {dest}")
            continue
        data = extract(rem, name, method, csize, lho)
        with open(dest, "wb") as fh:
            fh.write(data)
        print(f"{name}  {len(data)} bytes  -> {dest}")

    print(f"transferido: {rem.transferred / 1e6:.1f} MB de "
          f"{rem.total / 1e12:.2f} TB del paquete")


if __name__ == "__main__":
    main()
