"""Análise de campanhas de marketing: qual canal traz mais retorno?
Uso: python analise.py"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("dados/campanhas_marketing.csv", parse_dates=["data"])

# 1. Soma por canal
canal = df.groupby("canal")[["investimento", "impressoes", "cliques", "conversoes", "receita"]].sum()

# 2. Métricas (sempre calculadas sobre os totais, nunca pela média das taxas diárias)
canal["CTR_%"] = canal.cliques / canal.impressoes * 100      # de quem viu, quantos clicaram
canal["CPC"] = canal.investimento / canal.cliques            # custo por clique
canal["CPA"] = canal.investimento / canal.conversoes         # custo por conversão
canal["ROAS"] = canal.receita / canal.investimento           # receita para cada R$ 1 investido
canal = canal.sort_values("ROAS", ascending=False)

resumo = canal[["investimento", "receita", "CTR_%", "CPC", "CPA", "ROAS"]].round(2)
print(resumo.to_string())
resumo.to_csv("resultados/resumo_por_canal.csv")

# 3. Gráfico: ROAS por canal
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(resumo.index[::-1], resumo.ROAS[::-1], color="#2563eb")
ax.axvline(1, color="#dc2626", linestyle="--", linewidth=1)
ax.text(1.03, -0.45, "abaixo de 1 = prejuízo", color="#dc2626", fontsize=8)
for i, v in enumerate(resumo.ROAS[::-1]):
    ax.text(v + 0.05, i, f"{v:.2f}", va="center", fontsize=9)
ax.set_xlabel("ROAS (receita ÷ investimento)")
ax.set_title("Retorno por canal em 2025")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("resultados/roas_por_canal.png", dpi=150)

# 4. Evolução mensal da receita
mensal = df.groupby(df.data.dt.to_period("M"))[["investimento", "receita"]].sum()
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(mensal.index.astype(str), mensal.receita / 1000, marker="o", label="Receita", color="#2563eb")
ax.plot(mensal.index.astype(str), mensal.investimento / 1000, marker="o", label="Investimento", color="#94a3b8")
ax.set_ylabel("R$ mil"); ax.set_title("Receita e investimento por mês"); ax.legend(frameon=False)
ax.tick_params(axis="x", rotation=45); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("resultados/evolucao_mensal.png", dpi=150)
