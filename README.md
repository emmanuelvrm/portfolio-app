# Portfólio de Dados · Emmanuel VRM

Aplicação web (Streamlit) que reúne, em um só site, os projetos de dados do portfólio — para recrutadores testarem os modelos sem abrir notebooks.

| Página | Projeto | Código | Notebook |
| --- | --- | --- | --- |
| 🎓 ENEM 2021 | Previsão da média do ENEM (LightGBM/PyCaret) | [repo](https://github.com/emmanuelvrm/desempenho-enem-2021) | [Colab](https://colab.research.google.com/github/emmanuelvrm/desempenho-enem-2021/blob/main/notebooks/Desempenho_ENEM.ipynb) |
| 🧠 Depressão | Inferência de sintomas depressivos (Extra Trees) | [repo](https://github.com/emmanuelvrm/inferencia-depressao-habitos-saudaveis) | [Colab](https://colab.research.google.com/github/emmanuelvrm/inferencia-depressao-habitos-saudaveis/blob/main/notebooks/Inferencia_Depressao_e_Habitos_Saudaveis.ipynb) |
| 💳 Inadimplentes | Painel exploratório interativo | [repo](https://github.com/emmanuelvrm/analise-inadimplentes) | [Colab](https://colab.research.google.com/github/emmanuelvrm/analise-inadimplentes/blob/main/notebooks/Analise_Inadimplentes.ipynb) |
| 🎮 Jogos | Recomendador para streamers da Twitch | [repo](https://github.com/emmanuelvrm/recomendacao-jogos-twitch) | [Colab](https://colab.research.google.com/github/emmanuelvrm/recomendacao-jogos-twitch/blob/main/notebooks/03_modelagem.ipynb) |

## Rodar localmente
```bash
python3.10 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notas técnicas
- Os modelos `.pkl` (PyCaret, 2023) só carregam com **Python 3.10 + pandas 1.5.3 + scikit-learn 1.2.2 + scipy 1.9.3 + lightgbm 3.3.5** — as versões estão fixadas em `requirements.txt`.
- Deploy na Railway com Railpack (`railpack.json`; `libgomp1` para o LightGBM).
- `data/` contém apenas dados compactos (o recomendador usa uma agregação dos CSVs completos do repositório do projeto).
- ENEM: as opções do formulário vêm das categorias do encoder treinado; o exemplo do notebook original usava `idade = 20` (categoria inválida, a correta é `"20 anos"`).
- A página de depressão é educacional e **não é ferramenta de diagnóstico**.
