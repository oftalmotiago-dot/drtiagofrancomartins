# Capas de vídeo

Capas verticais (1080×1920) para Reels / Shorts / TikTok.

## Como gerar

```bash
pip install Pillow

cd capas
python3 gerar_capa.py --fundo estudio --saida minha-capa.jpg
```

### Trocar os textos

```bash
python3 gerar_capa.py \
  --fundo estudio \
  --chapeu "CIRURGIA DE PÁLPEBRAS" \
  --titulo "SEGURANÇA\nE CONFORTO" \
  --saida minha-capa.jpg
```

| Parâmetro  | O que é                                        |
|------------|------------------------------------------------|
| `--fundo`  | `estudio` (degradê azul) ou `consultorio`      |
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
assets/dr-tiago-recorte.png    recorte do Dr. Tiago, fundo transparente
assets/fundo-consultorio.jpg   faixa da parede/TV do consultório (frame do vídeo)
fontes/                        Outfit (SIL Open Font License, ver Outfit-OFL.txt)
```

Para uma foto nova, basta substituir `assets/dr-tiago-recorte.png` por outro
PNG com fundo transparente e ajustar `TOPO_CABECA` / `PESSOA_LARGURA` no
topo do `gerar_capa.py`.
