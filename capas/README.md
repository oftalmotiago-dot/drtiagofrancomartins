# Capas de vídeo

Capas verticais (1080×1920) para Reels / Shorts / TikTok.

## Como gerar

```bash
pip install Pillow

cd capas
python3 gerar_capa.py --foto sueter --fundo estudio --saida minha-capa.jpg
```

### Trocar os textos

```bash
python3 gerar_capa.py \
  --foto camisa-azul --fundo grafite \
  --chapeu "CICATRIZ NA BLEFAROPLASTIA" \
  --titulo "O MITO QUE\nMAIS ATRAPALHA" \
  --saida minha-capa.jpg
```

| Parâmetro  | O que é                                        |
|------------|------------------------------------------------|
| `--foto`   | `sueter`, `camisa-azul` ou `sueter-marrom`      |
| `--fundo`  | `estudio` (azul da marca), `consultorio`, `grafite` ou `petroleo` |
| `--chapeu` | linha pequena acima do título                   |
| `--titulo` | título principal (`\n` quebra a linha)          |
| `--nome`   | nome na assinatura                              |
| `--cargo`  | especialidade na assinatura                     |
| `--saida`  | caminho do arquivo gerado                       |

O título se redimensiona sozinho para caber na largura e no espaço livre
acima da cabeça — dá para escrever frases mais curtas ou mais longas sem
quebrar o layout.

## Decisões de layout

- **1080×1920 (9:16)** — formato nativo de Reels, Shorts e TikTok.
- **Área segura 4:5** — a grade do perfil do Instagram corta a capa para
  1080×1350 centralizado (y de 285 a 1635). Título e assinatura ficam
  dentro dessa faixa para não serem cortados.
- **Rosto sorrindo** — recortado da selfie e recomposto sobre o fundo, com
  luz de contorno para separar a figura do azul.

## Arquivos

```
assets/dr-tiago-recorte.png      recorte com suéter vinho, fundo transparente
assets/dr-tiago-camisa-azul.png  recorte com camisa azul, fundo transparente
assets/dr-tiago-sueter-marrom.png  recorte com suéter marrom, fundo transparente
assets/fundo-consultorio.jpg     faixa da parede/TV do consultório (frame do vídeo)
fontes/                          Outfit (SIL Open Font License, ver Outfit-OFL.txt)
```

Cada fundo tem sua paleta de texto. O `grafite` existe para roupas claras — a
camisa azul se aproxima demais do azul da marca e perde separação no `estudio`.
O `petroleo` acompanha roupas marrons: azul-esverdeado é o complementar do
marrom, e o acento vira areia quente em vez de azul.

## Adicionar uma foto nova

Salve o recorte (PNG com fundo transparente) em `assets/` e acrescente uma
entrada em `PERFIS`, no topo do `gerar_capa.py`:

```python
"camisa-azul": dict(arquivo="dr-tiago-camisa-azul.png",
                    largura=1160, centro_x=567, topo_cabeca=600, brilho=1.14),
```

- `largura` — largura final da figura na capa
- `centro_x` — onde o **rosto** deve cair (nem sempre é o meio do recorte)
- `topo_cabeca` — altura do topo da cabeça; o título se ajusta a partir dela
- `brilho` — correção de exposição, para fotos em contraluz
- `base_titulo` *(opcional)* — até onde o título pode descer. Por padrão ele
  para `FOLGA_CABELO` px antes do cabelo. Quando o rosto ocupa muito quadro e
  não sobra espaço, baixe esse limite: o título cruza o topo do cabelo, que é
  escuro e não atrapalha a leitura.

Para gerar o recorte, o modelo `birefnet-general` do `rembg` foi o único que
separou o Dr. Tiago da cadeira de escritório atrás dele — `u2net` e
`u2net_human_seg` trouxeram junto as abas de tela da cadeira.

**Atenção à `largura`:** na selfie atual os ombros já tocam as bordas
da própria foto, ou seja, o corpo vem cortado da origem. Por isso a figura é
montada com largura maior que os 1080 px da capa — ela sangra para fora do
quadro e o corte fica de fora. Se a largura cair abaixo de ~1100 px, reaparece
uma linha reta cortando o corpo nas laterais. Uma foto tirada de mais longe,
com espaço sobrando dos dois lados do corpo, permite enquadrar mais aberto.
