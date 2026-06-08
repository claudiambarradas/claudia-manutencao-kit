# Carrossel — He-Man & as IAs que fariam um trabalho melhor

Carrossel de Instagram (7 slides, 1080×1350) sobre os efeitos especiais criticados do novo
*Masters of the Universe* (He-Man, 2026) e 5 IAs de vídeo que entregariam um resultado melhor.

Feito no layout/paleta do **super carrossel** (capa com foto full-bleed, slides de conteúdo
em fundo escuro com print da IA no centro, CTA em fundo creme).

## Slides
1. Capa — foto do elenco + título serifado
2. Veo 3
3. Sora 2
4. Kling 2.6
5. Runway (Gen 4.5)
6. Seedance 2.0
7. CTA — @euclaud.ia

## Arquivos
- `carrossel.html` — fonte editável. Abre no navegador (com internet) pra renderizar com as
  fontes corretas (Playfair Display + Inter, via Google Fonts).
- `out/slide_1.png … slide_7.png` — slides prontos pra postar (1080×1350).
- `out/carrossel.pdf` — versão em PDF.
- `assets/` — foto da capa e os prints recortados das IAs (`*_crop.jpeg`).
- `legenda.md` — legenda + hashtags do post.

## Como exportar com a fonte exata
Os PNGs em `out/` foram gerados num ambiente sem acesso ao Google Fonts, então usam uma
serifada substituta (Liberation Serif). Pra exportar com **Playfair Display** de verdade:
abre o `carrossel.html` no navegador e tira print de cada `.slide`, ou roda sua skill local
de super carrossel sobre este HTML.

## Re-renderizar os PNGs (ambiente com Python)
```bash
pip install weasyprint PyMuPDF
python3 - <<'PY'
from weasyprint import HTML
import fitz
HTML('carrossel.html').write_pdf('out/carrossel.pdf')
doc = fitz.open('out/carrossel.pdf'); zoom = 1080/810
for i, p in enumerate(doc, 1):
    p.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(f'out/slide_{i}.png')
PY
```
