# -*- coding: utf-8 -*-
import json, io, os

INK   = "#12171B"; INK2 = "#4E5B63"; INK3 = "#7C888E"
BLUE  = "#2F6690"; AMBER = "#A9631F"; RULE = "#C7CFD2"
PAPER = "#F2F5F5"; FILM  = "#14181A"
CREAM = "#F7F2E9"; SAND  = "#D9D2C6"; GOLD  = "#E3A867"

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:ital,wght@0,400;0,600;1,400'
         '&family=Zilla+Slab:ital,wght@0,600;0,700;1,600&display=swap">')

SLAB = "'Zilla Slab', Georgia, 'Times New Roman', serif"
SANS = "'Public Sans', 'Helvetica Neue', Helvetica, sans-serif"
MONO = "'IBM Plex Mono', 'Courier New', monospace"

def page(body, dark=False):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  {FONTS}
  <style>
    body {{ margin: 0; background: {FILM if dark else PAPER}; }}
    a {{ color: {BLUE}; text-decoration: none; }}
    a:hover {{ color: {AMBER}; }}
  </style>
</helmet>
{body}
</x-dc>
</body>
</html>
"""

def frame(inner, dark=False, extra=""):
    bg = FILM if dark else PAPER
    return (f'<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; '
            f'background: {bg}; font-family: {SANS};">\n{extra}{inner}\n</div>')

def kicker(t, dark=False):
    c = GOLD if dark else BLUE
    return (f'<div style="font-family: {MONO}; font-size: 26px; font-weight: 500; '
            f'letter-spacing: 0.2em; text-transform: uppercase; color: {c};">{t}</div>')

def head(t, size=88, dark=False):
    c = CREAM if dark else INK
    return (f'<div style="font-family: {SLAB}; font-weight: 700; font-size: {size}px; '
            f'line-height: 1.04; letter-spacing: -0.015em; color: {c}; text-wrap: balance;">{t}</div>')

def body_txt(t, size=40, dark=False):
    c = SAND if dark else INK2
    return (f'<div style="font-size: {size}px; line-height: 1.42; color: {c};">{t}</div>')

def em(t, dark=False):
    c = CREAM if dark else INK
    return f'<span style="color: {c}; font-weight: 600;">{t}</span>'

def rule(dark=False):
    c = "rgba(247,242,233,0.22)" if dark else RULE
    return f'<div style="height: 1px; background: {c};"></div>'

def foot(left, right, dark=False):
    c = "rgba(247,242,233,0.62)" if dark else INK3
    return (f'<div style="margin-top: auto; display: flex; justify-content: space-between; '
            f'gap: 24px; font-family: {MONO}; font-size: 24px; letter-spacing: 0.12em; '
            f'text-transform: uppercase; color: {c};">'
            f'<span>{left}</span><span>{right}</span></div>')

def stack(children, gap=32, pad=84, top_bar=True, dark=False):
    bar = ''
    if top_bar and not dark:
        bar = f'<div style="height: 10px; background: {AMBER};"></div>'
    kids = "\n  ".join(children)
    return (f'{bar}<div style="display: flex; flex-direction: column; gap: {gap}px; '
            f'padding: {pad}px; height: 100%; box-sizing: border-box;">\n  {kids}\n</div>')

def photo_layer(src, alt):
    return (f'<img src="{src}" alt="{alt}" style="position: absolute; inset: 0; width: 100%; '
            f'height: 100%; object-fit: cover; filter: saturate(0.9) contrast(1.03);">\n'
            f'<div style="position: absolute; inset: 0; background: linear-gradient(180deg, '
            f'rgba(12,15,16,0.66) 0%, rgba(12,15,16,0.06) 32%, rgba(12,15,16,0.28) 52%, '
            f'rgba(12,15,16,0.90) 100%);"></div>\n')

def li(t, dark=False, size=40):
    c = CREAM if dark else INK
    b = GOLD if dark else BLUE
    return (f'<div style="display: flex; gap: 22px; align-items: baseline; font-size: {size}px; '
            f'line-height: 1.3; color: {c};">'
            f'<span style="color: {b}; flex: 0 0 auto;">&#9656;</span><span>{t}</span></div>')

def ul(items, dark=False, gap=22, size=40):
    return (f'<div style="display: flex; flex-direction: column; gap: {gap}px;">'
            + "".join(li(i, dark, size) for i in items) + '</div>')

HANDLE = "@drtiagofrancomartins"
files = {}

# ---------- 01 capa ----------
stamp = (f'<div style="position: absolute; top: 72px; left: 84px; z-index: 3; font-family: {MONO}; '
         f'font-size: 26px; letter-spacing: 0.28em; color: {GOLD}; border: 1px solid {GOLD}; '
         f'padding: 10px 18px;">1987</div>')
inner = stack([
    '<div style="margin-top: auto;"></div>',
    head("Eu j&aacute; passava o dia<br>olhando dentro dos olhos<br>das pessoas.", 86, dark=True),
    body_txt("Mudou a tecnologia. N&atilde;o mudou o que a gente<br>enxerga numa p&aacute;lpebra cansada.", 40, dark=True),
    rule(dark=True),
    foot("Blefaroplastia", "arraste &rarr;", dark=True),
], gap=30, dark=True)
files["Main.dc.html"] = page(frame(
    f'<div style="position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column;">{inner}</div>',
    dark=True, extra=photo_layer("slitlamp.jpg", "Oftalmologista na l&acirc;mpada de fenda, anos 80") + stamp), dark=True)

# ---------- 02 ----------
files["Definicao.dc.html"] = page(frame(stack([
    kicker("O que &eacute;"),
    head("Blefaroplastia n&atilde;o &eacute;<br>&ldquo;tirar ruga do olho&rdquo;."),
    body_txt("&Eacute; a cirurgia que remove o excesso de pele e reposiciona a gordura das p&aacute;lpebras para devolver a " + em("moldura natural do olho") + "."),
    rule(),
    body_txt("Ruga &eacute; textura. P&aacute;lpebra pesada &eacute; estrutura.<br>Problemas diferentes, solu&ccedil;&otilde;es diferentes."),
    foot("02 / 10", HANDLE),
], gap=36)))

# ---------- 03 ----------
files["Sinais.dc.html"] = page(frame(stack([
    kicker("Sinais"),
    head("Sua p&aacute;lpebra pode estar pedindo avalia&ccedil;&atilde;o se:", 72),
    ul(["a pele encosta nos c&iacute;lios",
        "voc&ecirc; levanta a sobrancelha sem perceber pra enxergar",
        "a testa d&oacute;i no fim do dia",
        "o delineador some na dobra da p&aacute;lpebra",
        "as fotos mostram um cansa&ccedil;o que voc&ecirc; n&atilde;o est&aacute; sentindo"], gap=26),
    rule(),
    body_txt("Marcou tr&ecirc;s? Vale uma consulta.", 36),
    foot("03 / 10", HANDLE),
], gap=34)))

# ---------- 04 ----------
files["Funcional.dc.html"] = page(frame(stack([
    kicker("N&atilde;o &eacute; s&oacute; est&eacute;tica"),
    head("Tem hora que a p&aacute;lpebra vira um problema de vis&atilde;o.", 76),
    body_txt("Quando a dermatoc&aacute;lase avan&ccedil;a, o excesso de pele cobre a pupila e " + em("reduz o campo visual superior") + "."),
    rule(),
    body_txt("A&iacute; a cirurgia &eacute; " + em("funcional") + " &mdash; documentada por campimetria e fotografia, inclusive para autoriza&ccedil;&atilde;o em conv&ecirc;nio."),
    foot("04 / 10", HANDLE),
], gap=36)))

# ---------- 05 ----------
col = lambda t, b: (f'<div style="display: flex; flex-direction: column; gap: 18px;">'
    f'<div style="font-family: {MONO}; font-size: 26px; font-weight: 600; letter-spacing: 0.16em; '
    f'text-transform: uppercase; color: {BLUE};">{t}</div>'
    f'<div style="font-size: 38px; line-height: 1.32; color: {INK};">{b}</div></div>')
files["SuperiorInferior.dc.html"] = page(frame(stack([
    kicker("Superior &ne; inferior"),
    head("S&atilde;o duas cirurgias diferentes.", 76),
    (f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 48px;">'
     + col("Superior", "Excesso de pele.<br>Olhar pesado.<br>Campo visual comprometido.")
     + col("Inferior", "Bolsas de gordura.<br>Sulco marcado.<br>Sombra que imita olheira.")
     + '</div>'),
    rule(),
    body_txt("Nem todo mundo precisa das duas. &Agrave;s vezes uma s&oacute; resolve o inc&ocirc;modo inteiro."),
    foot("05 / 10", HANDLE),
], gap=38)))

# ---------- 06 ----------
files["PeleMusculo.dc.html"] = page(frame(stack([
    kicker("O erro que mais vejo"),
    head("P&aacute;lpebra ca&iacute;da nem sempre &eacute; pele.", 78),
    body_txt("Pode ser o " + em("m&uacute;sculo levantador") + " &mdash; e a&iacute; o nome &eacute; ptose, n&atilde;o dermatoc&aacute;lase."),
    body_txt("Operar s&oacute; a pele quando o problema &eacute; o m&uacute;sculo gera aquele resultado frustrado: cicatrizou bem, mas o olhar continua ca&iacute;do."),
    rule(),
    body_txt("Por isso o exame mede a " + em("fun&ccedil;&atilde;o do levantador") + " e a " + em("MRD1") + " antes de qualquer decis&atilde;o.", 36),
    foot("06 / 10", HANDLE),
], gap=32)))

# ---------- 07 ----------
inner7 = stack([
    kicker("Como &eacute; feita", dark=True),
    '<div style="margin-top: auto;"></div>',
    ul(["Anestesia local com seda&ccedil;&atilde;o",
        "40 a 90 minutos",
        "Ambulatorial &mdash; alta no mesmo dia",
        "Superior: cicatriz dentro do sulco natural",
        "Inferior: via transconjuntival, sem cicatriz externa"], dark=True, gap=24, size=38),
    rule(dark=True),
    body_txt("A marca&ccedil;&atilde;o &eacute; feita com voc&ecirc; " + em("sentado e acordado", dark=True) + ". P&aacute;lpebra deitada mente.", 38, dark=True),
    foot("07 / 10", HANDLE, dark=True),
], gap=30, dark=True)
files["Cirurgia.dc.html"] = page(frame(
    f'<div style="position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column;">{inner7}</div>',
    dark=True, extra=photo_layer("surgery.jpg", "Cirurgi&atilde;o operando p&aacute;lpebra, anos 80")), dark=True)

# ---------- 08 ----------
def tl(when, what):
    return (f'<div style="display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 32px; align-items: baseline;">'
            f'<div style="font-family: {MONO}; font-size: 32px; font-weight: 600; color: {BLUE};">{when}</div>'
            f'<div style="font-size: 36px; line-height: 1.3; color: {INK};">{what}</div></div>')
files["Recuperacao.dc.html"] = page(frame(stack([
    kicker("Recupera&ccedil;&atilde;o"),
    head("O que esperar de verdade.", 76),
    ('<div style="display: flex; flex-direction: column; gap: 24px;">'
     + tl("48&ndash;72h", "gelo e cabeceira elevada")
     + tl("5&ndash;7 dias", "retirada dos pontos")
     + tl("7&ndash;14 dias", "incha&ccedil;o e roxo v&atilde;o embora")
     + tl("10&ndash;14 dias", "retorno social tranquilo")
     + tl("2&ndash;3 semanas", "libera&ccedil;&atilde;o para academia")
     + tl("meses", "cicatriz amadurece e clareia")
     + '</div>'),
    rule(),
    body_txt("Quem promete &ldquo;sem edema&rdquo; est&aacute; vendendo, n&atilde;o operando.", 36),
    foot("08 / 10", HANDLE),
], gap=34)))

# ---------- 09 ----------
def myth(q, a):
    return (f'<div style="display: flex; flex-direction: column; gap: 10px;">'
            f'<div style="font-family: {SLAB}; font-weight: 600; font-style: italic; font-size: 42px; '
            f'line-height: 1.16; color: {INK};">&ldquo;{q}&rdquo;</div>'
            f'<div style="font-size: 33px; line-height: 1.32; color: {INK2};">{a}</div></div>')
files["Mitos.dc.html"] = page(frame(stack([
    kicker("Mitos"),
    ('<div style="display: flex; flex-direction: column; gap: 34px;">'
     + myth("Vai ficar com olhar puxado.", "Isso &eacute; ressec&ccedil;&atilde;o excessiva &mdash; erro de indica&ccedil;&atilde;o e de t&eacute;cnica, n&atilde;o a cirurgia.")
     + myth("&Eacute; coisa de idoso.", "A indica&ccedil;&atilde;o &eacute; anat&ocirc;mica, n&atilde;o et&aacute;ria. Tem gente de 35 com bolsa hereditária.")
     + myth("Acaba com a olheira.", "Olheira de sombra, causada por bolsa, sim. Olheira pigmentada, n&atilde;o.")
     + myth("&Eacute; pra sempre.", "A superior costuma durar mais de 10 anos. Mas o rosto continua envelhecendo.")
     + '</div>'),
    foot("09 / 10", HANDLE),
], gap=36)))

# ---------- 10 ----------
diptych = (f'<div style="position: absolute; inset: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));">'
   f'<div style="position: relative; overflow: hidden;">'
   f'<img src="slitlamp.jpg" alt="Retrato nos anos 80" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">'
   f'</div>'
   f'<div style="display: flex; align-items: center; justify-content: center; text-align: center; padding: 56px; '
   f'background: #232A2D; border-left: 2px dashed rgba(227,168,103,0.55); font-family: {MONO}; font-size: 24px; '
   f'line-height: 1.7; letter-spacing: 0.1em; color: {GOLD};">SUBSTITUIR<br>POR FOTO ATUAL<br><br>mesma pose<br>mesmo enquadramento</div>'
   f'</div>'
   f'<div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(12,15,16,0.30) 0%, '
   f'rgba(12,15,16,0.05) 30%, rgba(12,15,16,0.55) 62%, rgba(12,15,16,0.95) 100%);"></div>\n')
inner10 = stack([
    '<div style="margin-top: auto;"></div>',
    head("Anos 80 ou hoje, o exame come&ccedil;a igual: sentando na frente do paciente e olhando com calma.", 62, dark=True),
    body_txt("Se a sua p&aacute;lpebra anda pesando &mdash; na est&eacute;tica ou na vis&atilde;o &mdash; a conversa come&ccedil;a por uma avalia&ccedil;&atilde;o.", 36, dark=True),
    rule(dark=True),
    (f'<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 24px;">'
     f'<div style="font-family: {SLAB}; font-weight: 600; font-size: 42px; color: {CREAM};">Agende sua consulta</div>'
     f'<div style="font-family: {MONO}; font-size: 22px; line-height: 1.6; letter-spacing: 0.08em; '
     f'text-align: right; color: {GOLD};">DR. TIAGO FRANCO MARTINS<br>CRM 00000 &middot; RQE 0000</div></div>'),
], gap=28, dark=True)
files["Fechamento.dc.html"] = page(frame(
    f'<div style="position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column;">{inner10}</div>',
    dark=True, extra=diptych), dark=True)

for name, src in files.items():
    open(name, "w", encoding="utf-8").write(src)

order = ["Main.dc.html","Definicao.dc.html","Sinais.dc.html","Funcional.dc.html","SuperiorInferior.dc.html",
         "PeleMusculo.dc.html","Cirurgia.dc.html","Recuperacao.dc.html","Mitos.dc.html","Fechamento.dc.html"]
titles = ["01 · Capa","02 · O que é","03 · Sinais","04 · Funcional","05 · Superior x Inferior",
          "06 · Pele ou músculo","07 · Como é feita","08 · Recuperação","09 · Mitos","10 · Fechamento"]
abs_ = []
for i, f in enumerate(order):
    r, c = divmod(i, 5)
    abs_.append({"file": f, "x": c*(1080+140), "y": r*(1350+220), "w": 1080, "h": 1350, "title": titles[i]})
canvas = {
  "artboards": abs_,
  "annotations": [
    {"id":"crm","x":0,"y":-170,"w":520,"text":"Preencher CRM e RQE no slide 10 antes de exportar."},
    {"id":"diptico","x":4880,"y":3060,"w":560,"text":"Slide 10: a metade direita espera a foto atual — mesma pose e mesmo enquadramento da foto de 1987."},
    {"id":"fontes","x":600,"y":-170,"w":620,"text":"Na exportação em PNG/PDF as fontes do Google podem cair para Georgia e Helvetica. Confira o resultado antes de publicar."}
  ],
  "launch": {"view": "canvas"}
}
open("canvas.json","w",encoding="utf-8").write(json.dumps(canvas, ensure_ascii=False, indent=2))
print("gerados:", len(files), "artboards + canvas.json")
