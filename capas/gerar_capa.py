#!/usr/bin/env python3
"""Gera a capa vertical (1080x1920) dos videos do Dr. Tiago Franco Martins.

Uso:
    python3 gerar_capa.py --fundo estudio --saida capa.jpg
    python3 gerar_capa.py --fundo consultorio \
        --chapeu "CIRURGIA DE PÁLPEBRAS" --titulo "SEGURANÇA\nE CONFORTO"

Requer Pillow:  pip install Pillow
"""
import argparse
from pathlib import Path

from PIL import (Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)

BASE = Path(__file__).resolve().parent
FUNDO_CONSULTORIO = BASE / "assets" / "fundo-consultorio.jpg"
BOLD = BASE / "fontes" / "Outfit-Bold.ttf"
REGULAR = BASE / "fontes" / "Outfit-Regular.ttf"

W, H = 1080, 1920

# A grade do Instagram corta a capa para 4:5 (1080x1350 centralizado):
# todo texto precisa caber nesta faixa para nao ser cortado no perfil.
SAFE_TOP, SAFE_BOT = (H - 1350) // 2, (H + 1350) // 2

MARGEM = 68
CONDENSAR_MIN = 0.82   # condensacao horizontal maxima do titulo
FOLGA_CABELO = 50      # respiro entre a base do titulo e o topo da cabeca
AZUL_TOPO, AZUL_BASE = (5, 24, 46), (12, 62, 102)
DESTAQUE = (94, 199, 245)

# Cada fundo carrega sua paleta de texto: destaque (barrinhas), apoio (linha da
# especialidade) e os tons usados para escurecer topo e base.
PALETA_AZUL = dict(destaque=DESTAQUE, chapeu=(198, 226, 245), apoio=(176, 208, 232),
                   sombra_base=(4, 18, 34), sombra_topo=(3, 16, 32))
PALETAS = {
    "estudio": PALETA_AZUL,
    "consultorio": PALETA_AZUL,
    "grafite": PALETA_AZUL,
    # petroleo acompanha roupas marrons: o azul-esverdeado e o complementar do
    # marrom, e o acento vira areia quente em vez de azul.
    "petroleo": dict(destaque=(240, 192, 132), chapeu=(240, 224, 202),
                     apoio=(214, 200, 180),
                     sombra_base=(5, 24, 26), sombra_topo=(4, 20, 22)),
}

# Enquadramento de cada foto. A largura passa de 1080 de proposito: nas duas
# fotos o corpo ja toca as bordas da imagem original dos ombros para baixo, entao
# a figura precisa sangrar para fora do quadro — assim o corte fica fora da capa
# em vez de virar uma linha reta nas laterais. `centro_x` alinha o ROSTO no meio
# da capa (nem sempre e o meio do recorte).
PERFIS = {
    "sueter": dict(arquivo="dr-tiago-recorte.png",
                   largura=1120, centro_x=540, topo_cabeca=610, brilho=1.06),
    # foto tirada em contraluz (janela atras): o rosto pede um brilho maior
    "camisa-azul": dict(arquivo="dr-tiago-camisa-azul.png",
                        largura=1160, centro_x=567, topo_cabeca=600, brilho=1.14),
    # nesta foto o rosto e bem maior dentro do quadro: a cabeca sobe para o
    # queixo nao encostar na assinatura, e o titulo cruza de leve o cabelo.
    "sueter-marrom": dict(arquivo="dr-tiago-sueter-marrom.png",
                          largura=1160, centro_x=510, topo_cabeca=480,
                          base_titulo=558, brilho=1.08),
}


def fonte(caminho, tamanho):
    return ImageFont.truetype(str(caminho), tamanho)


def degrade(topo, base):
    faixa = Image.new("RGB", (1, H))
    px = faixa.load()
    for y in range(H):
        t = y / (H - 1)
        px[0, y] = tuple(round(topo[i] + (base[i] - topo[i]) * t) for i in range(3))
    return faixa.resize((W, H), Image.BICUBIC)


def brilho(img, centro, raio, cor, forca):
    """Soma um brilho radial suave ao fundo."""
    camada = Image.new("L", (W, H), 0)
    ImageDraw.Draw(camada).ellipse(
        [centro[0] - raio, centro[1] - raio, centro[0] + raio, centro[1] + raio], fill=forca
    )
    camada = camada.filter(ImageFilter.GaussianBlur(raio * 0.55))
    return Image.composite(Image.new("RGB", (W, H), cor), img, camada)


def vinheta(img, cor=(3, 16, 32)):
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-280, 100, W + 280, H - 40], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(210)).point(lambda p: 255 - p)
    return Image.composite(Image.new("RGB", (W, H), cor), img, v)


def fundo_estudio():
    """Degrade azul da marca, com halo atras da cabeca."""
    bg = degrade(AZUL_TOPO, AZUL_BASE)
    bg = brilho(bg, (540, 980), 620, (24, 108, 168), 150)
    bg = brilho(bg, (150, 250), 460, (10, 40, 74), 120)
    bg = brilho(bg, (540, 900), 400, (34, 132, 198), 110)
    return bg


def fundo_petroleo():
    """Azul-esverdeado profundo, complementar do marrom."""
    bg = degrade((6, 30, 34), (13, 72, 78))
    bg = brilho(bg, (540, 960), 620, (24, 116, 122), 140)
    bg = brilho(bg, (150, 250), 460, (6, 40, 46), 110)
    bg = brilho(bg, (540, 900), 400, (34, 140, 146), 105)
    return vinheta(bg, (3, 18, 20))


def fundo_grafite():
    """Grafite frio com brilho azul discreto. Da mais contraste para roupas
    claras, que se aproximam demais do azul da marca."""
    bg = degrade((22, 26, 32), (38, 46, 58))
    bg = brilho(bg, (540, 940), 620, (52, 74, 100), 130)
    bg = brilho(bg, (540, 880), 380, (64, 104, 140), 95)
    return vinheta(bg, (12, 15, 20))


def fundo_consultorio():
    """Faixa da parede/TV do consultorio (frame do proprio video), desfocada e
    dissolvida no azul da marca. Usa so a area acima da cabeca, sem UI do celular."""
    ALTURA_FAIXA = 1000
    faixa = Image.open(FUNDO_CONSULTORIO).convert("RGB")
    faixa = faixa.resize((W, ALTURA_FAIXA), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22))
    faixa = ImageEnhance.Color(faixa).enhance(1.15)

    mascara = Image.new("L", (1, H), 0)
    mp = mascara.load()
    for y in range(H):
        if y < 620:
            mp[0, y] = 235
        elif y < ALTURA_FAIXA:
            mp[0, y] = round(235 * (1 - (y - 620) / (ALTURA_FAIXA - 620)) ** 1.4)

    tela = Image.new("RGB", (W, H), (8, 34, 60))
    tela.paste(faixa, (0, 0))
    bg = Image.composite(tela, degrade((6, 26, 48), (10, 54, 90)),
                         mascara.resize((W, H), Image.BICUBIC))
    bg = brilho(bg, (540, 900), 400, (30, 118, 180), 90)
    return vinheta(bg)


def camadas_pessoa(perfil):
    """Devolve (sombra, figura, luz de contorno) ja posicionadas na tela."""
    cut = Image.open(BASE / "assets" / perfil["arquivo"]).convert("RGBA")
    alfa = cut.getchannel("A")

    rgb = ImageEnhance.Brightness(cut.convert("RGB")).enhance(perfil["brilho"])
    rgb = ImageEnhance.Contrast(rgb).enhance(1.07)
    rgb = ImageEnhance.Color(rgb).enhance(1.05)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=3, percent=55, threshold=3))
    rgb.putalpha(alfa)

    escala = perfil["largura"] / cut.width
    bx0, by0, bx1, _ = alfa.getbbox()
    cut = rgb.resize((round(cut.width * escala), round(cut.height * escala)), Image.LANCZOS)

    figura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    figura.paste(cut, (round(perfil["centro_x"] - (bx0 + bx1) / 2 * escala),
                       perfil["topo_cabeca"] - round(by0 * escala)), cut)

    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra.paste(Image.new("RGBA", (W, H), (0, 10, 22, 190)), (0, 0), figura)
    sombra = sombra.filter(ImageFilter.GaussianBlur(34))

    # luz de contorno: separa a figura do fundo escuro
    a = figura.getchannel("A")
    borda = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(3)), a.filter(ImageFilter.MinFilter(9)))
    borda = borda.filter(ImageFilter.GaussianBlur(3)).point(lambda v: min(255, int(v * 0.5)))
    contorno = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    contorno.paste(Image.new("RGBA", (W, H), (190, 226, 250, 255)), (0, 0), borda)
    return sombra, figura, contorno


def escurecer_extremos(img, paleta):
    """Degrades no topo e na base para o texto sempre ter contraste."""
    base = Image.new("L", (1, H), 0)
    bp = base.load()
    for y in range(H):
        t = max(0.0, (y - 1240) / (H - 1240))
        bp[0, y] = round(238 * t ** 1.25)
    img = Image.composite(Image.new("RGBA", (W, H), paleta["sombra_base"] + (255,)), img,
                          base.resize((W, H), Image.BICUBIC))

    topo = Image.new("L", (1, H), 0)
    tp = topo.load()
    for y in range(H):
        tp[0, y] = round(165 * max(0.0, (760 - y) / 760) ** 1.3)
    return Image.composite(Image.new("RGBA", (W, H), paleta["sombra_topo"] + (255,)), img,
                           topo.resize((W, H), Image.BICUBIC))


def escrever(img, titulo, chapeu, nome, cargo, base_titulo, paleta):
    d = ImageDraw.Draw(img, "RGBA")
    largura_max = W - 2 * MARGEM

    # chapeu, com barra de destaque
    y = SAFE_TOP + 8
    d.rounded_rectangle([MARGEM, y + 6, MARGEM + 8, y + 44], 4, fill=paleta["destaque"])
    d.text((MARGEM + 26, y), chapeu, font=fonte(BOLD, 34), fill=paleta["chapeu"])

    # Titulo. Palavras longas ("BLEFAROPLASTIA") condensam de leve em vez de
    # encolher: mantem o impacto sem estourar a margem.
    y += 70
    linhas = titulo.split("\n")
    # Corpo da fonte tirado do espaco livre ate a cabeca, ja descontando a folga.
    # 1.03 = entrelinha; 0.72 = altura aproximada das maiusculas da Outfit.
    espaco = base_titulo - y
    tamanho = min(190, int(espaco / ((len(linhas) - 1) * 1.03 + 0.72)))
    while tamanho > 44:
        f = fonte(BOLD, tamanho)
        larguras = [f.getbbox(ln)[2] for ln in linhas]
        fator = min(1.0, largura_max / max(larguras))
        if fator >= CONDENSAR_MIN:
            break
        tamanho -= 2


    entrelinha = round(tamanho * 1.03)
    for i, linha in enumerate(linhas):
        tela = Image.new("RGBA", (max(larguras) + 12, round(tamanho * 1.5)), (0, 0, 0, 0))
        dl = ImageDraw.Draw(tela)
        dl.text((3, 4), linha, font=f, fill=(0, 12, 26, 120))
        dl.text((0, 0), linha, font=f, fill=(255, 255, 255))
        if fator < 1.0:
            tela = tela.resize((round(tela.width * fator), tela.height), Image.LANCZOS)
        img.alpha_composite(tela, (MARGEM, y + i * entrelinha))

    # assinatura, ancorada no limite inferior da area segura
    base = SAFE_BOT - 6
    d.rounded_rectangle([MARGEM, base - 128, MARGEM + 96, base - 122], 3, fill=paleta["destaque"])
    d.text((MARGEM, base - 108), nome, font=fonte(BOLD, 52), fill=(255, 255, 255))
    d.text((MARGEM, base - 44), cargo.upper(), font=fonte(REGULAR, 34), fill=paleta["apoio"])


def gerar(fundo, perfil, titulo, chapeu, nome, cargo, saida):
    paleta = PALETAS[fundo]
    bg = {"estudio": fundo_estudio, "consultorio": fundo_consultorio,
          "grafite": fundo_grafite, "petroleo": fundo_petroleo}[fundo]()
    sombra, figura, contorno = camadas_pessoa(perfil)

    img = Image.alpha_composite(bg.convert("RGBA"), sombra)
    img = Image.alpha_composite(img, figura)
    img = Image.alpha_composite(img, contorno)
    img = escurecer_extremos(img, paleta)

    # Ate onde o titulo pode descer. Por padrao para antes do cabelo; um perfil
    # pode baixar esse limite quando o rosto ocupa muito quadro e nao sobra
    # espaco — ai o titulo cruza o topo do cabelo, que e escuro e nao atrapalha.
    base_titulo = perfil.get("base_titulo", perfil["topo_cabeca"] - FOLGA_CABELO)
    escrever(img, titulo, chapeu, nome, cargo, base_titulo, paleta)
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(saida, quality=95, subsampling=0)
    print("capa gerada:", saida)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fundo", default="estudio",
                   choices=sorted(PALETAS))
    p.add_argument("--foto", default="sueter", choices=sorted(PERFIS))
    p.add_argument("--titulo", default="BLEFAROPLASTIA\nEM HOMENS",
                   help="use \\n para quebrar linha")
    p.add_argument("--chapeu", default="CIRURGIA DE PÁLPEBRAS")
    p.add_argument("--nome", default="Dr. Tiago Franco Martins")
    p.add_argument("--cargo", default="Oftalmologista · Cirurgião oculoplástico")
    p.add_argument("--saida", default="capa.jpg")
    a = p.parse_args()
    gerar(a.fundo, PERFIS[a.foto], a.titulo.replace("\\n", "\n"), a.chapeu,
          a.nome, a.cargo, a.saida)
