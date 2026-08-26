import json
import customtkinter as ctk
from datetime import datetime

# Configurações de tema visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ARQUIVO_DADOS = "transacoes.json"

class AppFinancas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Finanças Pessoais")
        self.geometry("450x550")
        self.resizable(False, False)

        # Título Principal
        self.label_titulo = ctk.CTkLabel(self, text="💰 Minhas Finanças", font=("Arial", 22, "bold"))
        self.label_titulo.pack(pady=15)

        # Campos de Entrada
        self.entry_descricao = ctk.CTkEntry(self, placeholder_text="Descrição (ex: Salário, Mercado)", width=320)
        self.entry_descricao.pack(pady=8)

        self.entry_valor = ctk.CTkEntry(self, placeholder_text="Valor (R$)", width=320)
        self.entry_valor.pack(pady=8)

        # Botões
        self.btn_receita = ctk.CTkButton(self, text="+ Adicionar Receita", fg_color="green", hover_color="#006400", width=320, command=lambda: self.salvar_transacao("Receita"))
        self.btn_receita.pack(pady=5)

        self.btn_despesa = ctk.CTkButton(self, text="- Adicionar Despesa", fg_color="red", hover_color="#8B0000", width=320, command=lambda: self.salvar_transacao("Despesa"))
        self.btn_despesa.pack(pady=5)

        # Exibição do Saldo
        self.label_saldo = ctk.CTkLabel(self, text="Saldo Atual: R$ 0.00", font=("Arial", 16, "bold"))
        self.label_saldo.pack(pady=15)

        # Caixa do Extrato
        self.textbox_extrato = ctk.CTkTextbox(self, width=380, height=200)
        self.textbox_extrato.pack(pady=10)

        self.atualizar_tela()

    def carregar_dados(self):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_transacao(self, tipo):
        descricao = self.entry_descricao.get().strip()
        valor_texto = self.entry_valor.get().strip().replace(",", ".")

        if not descricao or not valor_texto:
            return

        try:
            valor = float(valor_texto)
        except ValueError:
            return

        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        transacao = {"tipo": tipo, "descricao": descricao, "valor": valor, "data": data}

        transacoes = self.carregar_dados()
        transacoes.append(transacao)

        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(transacoes, f, ensure_ascii=False, indent=4)

        self.entry_descricao.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        self.atualizar_tela()

    def atualizar_tela(self):
        transacoes = self.carregar_dados()
        self.textbox_extrato.delete("1.0", "end")

        total_receitas = 0.0
        total_despesas = 0.0

        for t in transacoes:
            sinal = "+" if t["tipo"] == "Receita" else "-"
            linha = f"[{t['data']}] {t['descricao']}: {sinal}R$ {t['valor']:.2f}\n"
            self.textbox_extrato.insert("end", linha)

            if t["tipo"] == "Receita":
                total_receitas += t["valor"]
            else:
                total_despesas += t["valor"]

        saldo = total_receitas - total_despesas
        cor = "#00FF00" if saldo >= 0 else "#FF4D4D"
        self.label_saldo.configure(text=f"Saldo Atual: R$ {saldo:.2f}", text_color=cor)

if __name__ == "__main__":
    app = AppFinancas()
    app.mainloop()
