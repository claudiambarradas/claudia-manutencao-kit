#!/usr/bin/env bash
# Kit de Manutenção IA — installer
# Copia skills, templates de memória e CLAUDE.md template pras pastas do Claude Code.

set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
MEMORY_TEMPLATES_DIR="${CLAUDE_DIR}/memory-templates"

echo ""
echo "Kit de Manutencao IA — instalacao"
echo "=================================="
echo ""
echo "Fonte:  ${KIT_DIR}"
echo "Destino: ${CLAUDE_DIR}"
echo ""

if [ ! -d "${CLAUDE_DIR}" ]; then
  echo "ERRO: ~/.claude nao existe. Voce instalou o Claude Code?"
  echo "      https://docs.claude.com/claude-code"
  exit 1
fi

# --- skills ---
mkdir -p "${SKILLS_DIR}"
echo "Instalando skills em ${SKILLS_DIR}..."
for skill_path in "${KIT_DIR}/skills/"*/; do
  skill_name="$(basename "${skill_path}")"
  dest="${SKILLS_DIR}/${skill_name}"
  if [ -d "${dest}" ]; then
    echo "  - ${skill_name} ja existe, pulando (remova manualmente se quiser sobrescrever)"
  else
    cp -R "${skill_path}" "${dest}"
    echo "  + ${skill_name}"
  fi
done

# --- memory templates ---
mkdir -p "${MEMORY_TEMPLATES_DIR}"
echo ""
echo "Copiando templates de memoria em ${MEMORY_TEMPLATES_DIR}..."
cp -R "${KIT_DIR}/memory-templates/." "${MEMORY_TEMPLATES_DIR}/"
echo "  + templates copiados (nao ativos — sao referencia pra voce adaptar)"

# --- CLAUDE.md ---
echo ""
if [ -f "${HOME}/CLAUDE.md" ]; then
  echo "~/CLAUDE.md ja existe. Template disponivel em:"
  echo "  ${KIT_DIR}/claude-md-template/CLAUDE.md"
  echo "  (copie secoes manualmente se quiser)"
else
  cp "${KIT_DIR}/claude-md-template/CLAUDE.md" "${HOME}/CLAUDE.md"
  echo "CLAUDE.md criado em ~/CLAUDE.md — abre e preenche os campos [entre colchetes]"
fi

echo ""
echo "=================================="
echo "Pronto."
echo ""
echo "Proximo passo:"
echo "  1. Abre o Claude Code"
echo "  2. Diz: \"Roda a skill ops-infra-scan pra mapear minha infra\""
echo ""
