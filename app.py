# ==========================================
# SISTEMA DE GERENCIAMENTO DE FINANÇAS
# ==========================================

import json
from datetime import datetime

# Nome do arquivo onde as finanças serão salvas
ARQUIVO_DADOS = "transacoes.json"

def carregar_dados():
    """Carrega as transações salvas no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(transacoes):
    """Salva a lista de transações no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(transacoes, f, ensure_ascii=False, indent=4)

def adicionar_transacao(tipo):
    """Adiciona uma nova receita ou despesa."""
    descricao = input("Descrição (ex: Salário, Mercado, Aluguel): ").strip()
    try:
        valor = float(input("Valor (R$): ").replace(",", "."))
    except ValueError:
        print("\n❌ Valor inválido! Digite apenas números.\n")
        return

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    transacao = {
        "tipo": tipo,  # "Receita" ou "Despesa"
        "descricao": descricao,
        "valor": valor,
        "data": data
    }

    transacoes = carregar_dados()
    transacoes.append(transacao)
    salvar_dados(transacoes)
    print(f"\n✅ {tipo} de R$ {valor:.2f} registrada com sucesso!\n")

def exibir_extrato():
    """Exibe o histórico de transações e o saldo geral."""
    transacoes = carregar_dados()

    if not transacoes:
        print("\n📭 Nenhuma transação registrada ainda.\n")
        return

    print("\n" + "="*45)
    print("           EXTRATO FINANCEIRO")
    print("="*45)

    total_receitas = 0.0
    total_despesas = 0.0

    for t in transacoes:
        sinal = "+" if t["tipo"] == "Receita" else "-"
        cor_tipo = "🟢" if t["tipo"] == "Receita" else "🔴"
        
        print(f"{cor_tipo} [{t['data']}] {t['descricao']}: {sinal}R$ {t['valor']:.2f}")

        if t["tipo"] == "Receita":
            total_receitas += t["valor"]
        else:
            total_despesas += t["valor"]

    saldo = total_receitas - total_despesas

    print("-" * 45)
    print(f"Total de Entradas (Receitas): R$ {total_receitas:.2f}")
    print(f"Total de Saídas  (Despesas): R$ {total_despesas:.2f}")
    print("-" * 45)
    
    if saldo >= 0:
        print(f"Saldo Atual: 🔵 R$ {saldo:.2f} (Conta no Azul)")
    else:
        print(f"Saldo Atual: 🔴 R$ {saldo:.2f} (Conta no Vermelho)")
    print("="*45 + "\n")

def menu():
    """Menu principal do sistema."""
    while True:
        print("--- PAINEL DE FINANÇAS ---")
        print("1. Adicionar Receita (+)")
        print("2. Adicionar Despesa (-)")
        print("3. Ver Extrato e Saldo")
        print("4. Sair")

        opcao = input("Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            adicionar_transacao("Receita")
        elif opcao == "2":
            adicionar_transacao("Despesa")
        elif opcao == "3":
            exibir_extrato()
        elif opcao == "4":
            print("\nAté logo! Mantenha suas finanças organizadas. 👋\n")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    menu()