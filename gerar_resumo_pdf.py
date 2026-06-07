from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/user/claudia-manutencao-kit/resumo_imersao_isa_06_06_2026.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2.5*cm,
    leftMargin=2.5*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "titulo",
    parent=styles["Normal"],
    fontSize=18,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a1a2e"),
    spaceAfter=4,
    alignment=TA_CENTER,
)

subtitle_style = ParagraphStyle(
    "subtitulo",
    parent=styles["Normal"],
    fontSize=10,
    fontName="Helvetica",
    textColor=colors.HexColor("#555555"),
    spaceAfter=2,
    alignment=TA_CENTER,
)

section_style = ParagraphStyle(
    "secao",
    parent=styles["Normal"],
    fontSize=11,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#c0392b"),
    spaceBefore=14,
    spaceAfter=4,
)

body_style = ParagraphStyle(
    "corpo",
    parent=styles["Normal"],
    fontSize=10,
    fontName="Helvetica",
    textColor=colors.HexColor("#222222"),
    leading=15,
    spaceAfter=4,
)

bullet_style = ParagraphStyle(
    "bullet",
    parent=body_style,
    leftIndent=14,
    bulletIndent=0,
    spaceBefore=1,
    spaceAfter=1,
)

label_style = ParagraphStyle(
    "label",
    parent=styles["Normal"],
    fontSize=9,
    fontName="Helvetica",
    textColor=colors.HexColor("#777777"),
    spaceAfter=2,
    alignment=TA_CENTER,
)

content = []

# Cabeçalho
content.append(Spacer(1, 0.3*cm))
content.append(Paragraph("Resumo — Imersão Isabela @atrevidaisa", title_style))
content.append(Paragraph("06 de junho de 2026", subtitle_style))
content.append(Spacer(1, 0.2*cm))
content.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#c0392b")))
content.append(Spacer(1, 0.2*cm))
content.append(Paragraph("Reunião via Zoom &nbsp;|&nbsp; Duração: ~10h &nbsp;|&nbsp; 291 participantes", label_style))
content.append(Spacer(1, 0.5*cm))

sections = [
    (
        "1. IA e o futuro do mercado de trabalho",
        "Isabela abriu com dados do <b>Fórum Econômico Mundial (2024)</b> sobre o futuro dos empregos. "
        "A mensagem central: as habilidades <b>menos substituíveis pela IA são as humanas</b> — empatia, liderança, "
        "ensinar e gerir pessoas. As primeiras a serem substituídas são justamente as técnicas de tecnologia e "
        "especialistas em IA. Conclusão: você não precisa dominar ferramenta nenhuma — precisa dominar <b>gente</b>.",
        []
    ),
    (
        "2. Desmistificando a IA no conteúdo",
        "Ela reforçou que a imersão é uma <b>aula de conteúdo</b>, não de IA. O jeito mais burro que ela usa a IA "
        "funciona porque o que vende é o <b>roteiro e a estratégia</b>, não a sofisticação da ferramenta. "
        "Liberou a turma do medo de ficar para trás por não saber usar todas as IAs.",
        []
    ),
    (
        "3. Olhar estratégico para referências",
        "Ensinamento sobre como analisar perfis de concorrentes com \"olhos maldosos\" — entender <b>por que</b> "
        "algo funciona (às vezes é a personalidade de quem posta, não a estratégia em si). Alerta sobre o erro de "
        "copiar estratégias de quem tem recursos que você não tem.",
        []
    ),
    (
        "4. Logística de produção de conteúdo",
        "Um dos pontos mais práticos: separar as etapas do conteúdo em <b>dias diferentes</b> "
        "(pesquisa, roteiro, gravação, edição, postagem). Isabela nunca grava e escreve no mesmo dia. "
        "Dica de contratar um \"sombra\" (adolescente, parceiro) para criar pressão externa e compromisso.",
        []
    ),
    (
        "5. Produto e ticket — não comece barato",
        "Crítica direta ao modelo de <b>low ticket</b> (e-books, mini-cursos baratos) para quem está começando. "
        "Recomendação: venda mentorias, consultorias, acelerações — produtos com ticket que façam diferença real. "
        "Ela entrou no mercado vendendo R$ 5.000 quando a média era R$ 2.000.",
        []
    ),
    (
        "6. ICP — Perfil do Cliente Ideal",
        "Explicou a diferença entre persona e ICP: o ICP considera o <b>momento</b> da pessoa, não só o perfil. "
        "Quem ela é, o que está vivendo agora. Alerta: muita gente está vendendo para quem não tem dinheiro "
        "por causa do tipo de comunicação que usa.",
        []
    ),
    (
        "7. Pesquisa de público com IA (ChatGPT)",
        "Mostrou na prática como usar o ChatGPT para gerar relatórios de pesquisa de público, usados como "
        "documentação para alimentar <b>agentes de IA</b> que ajudam na criação de conteúdo. "
        "Prometeu enviar os prompts por e-mail após a aula.",
        []
    ),
    (
        "8. Os 4 pilares do conteúdo",
        "",
        [
            "<b>Você</b> — identidade e posicionamento",
            "<b>Seu cliente</b> — dores, desejos, momento de vida",
            "<b>Seu mercado</b> — concorrentes, referências, o que performa",
            "<b>O algoritmo</b> — formatos e frequência",
        ]
    ),
    (
        "9. Linha editorial na prática",
        "Apresentou um exemplo real de linha editorial de cliente com equipe: mistura de vídeos com roteiro, "
        "caixinha de perguntas, carrosséis, conteúdo pessoal. A proporção do mercado: "
        "<b>70% conteúdo para público frio / 30% para público mais quente</b>. "
        "Reforçou que a linha editorial deve caber na sua realidade — não copie de quem tem time se você está sozinha.",
        []
    ),
    (
        "10. Agentes de IA para conteúdo",
        "Mostrou como montar agentes no ChatGPT usando a pesquisa de público como base de documentação, "
        "para gerar roteiros e carrosséis no estilo de referências escolhidas. A ideia é \"debulhar\" a "
        "estratégia de um perfil de referência e aplicar ao cliente.",
        []
    ),
]

for title, body, bullets in sections:
    content.append(Paragraph(title, section_style))
    if body:
        content.append(Paragraph(body, body_style))
    for b in bullets:
        content.append(Paragraph(f"• &nbsp; {b}", bullet_style))

# Rodapé de próximos passos
content.append(Spacer(1, 0.6*cm))
content.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#dddddd")))
content.append(Spacer(1, 0.3*cm))
content.append(Paragraph("<b>Próximos passos mencionados na aula:</b>", body_style))
content.append(Paragraph(
    "Envio de materiais, prompts e links por e-mail; abertura de vagas de consultoria individual (10 vagas).",
    body_style
))

doc.build(content)
print(f"PDF gerado: {OUTPUT}")
