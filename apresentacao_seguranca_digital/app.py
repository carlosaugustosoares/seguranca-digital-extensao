import tkinter as tk
from tkinter import messagebox

SLIDES = [
("🔐 SEGURANÇA DIGITAL",
 "Como reconhecer riscos e proteger suas informações no dia a dia.",
 ["Golpes virtuais • Senhas seguras • Proteção de dados • Phishing"]),
("POR QUE FALAR SOBRE SEGURANÇA DIGITAL?",
 "A internet faz parte da nossa rotina. Usamos aplicativos, redes sociais, bancos, lojas e serviços digitais.",
 ["Quanto mais usamos esses serviços, maior a importância de reconhecer situações de risco.",
  "Um cuidado simples antes de clicar, informar um dado ou instalar algo pode evitar prejuízos.",
  "💡 Segurança digital começa com informação e atenção."]),
("RISCOS DO USO INADEQUADO DA INTERNET",
 "Alguns problemas podem acontecer quando não temos cuidado.",
 ["🎣 Golpes e phishing — mensagens e páginas falsas tentam enganar.",
  "🔑 Roubo de contas — senhas fracas ou reutilizadas aumentam os riscos.",
  "💳 Prejuízo financeiro — criminosos podem tentar obter dinheiro ou dados.",
  "👤 Exposição de dados — informações pessoais podem ser usadas indevidamente."]),
("GOLPES VIRTUAIS: SINAIS DE ALERTA",
 "Fique atento principalmente quando uma mensagem:",
 ["• cria urgência: “faça agora” ou “sua conta será bloqueada”;",
  "• promete prêmio, dinheiro ou vantagem fácil;",
  "• pede senha, código de segurança ou dados pessoais;",
  "• apresenta link estranho ou endereço diferente do serviço oficial;",
  "• possui erros, pressão ou pedidos incomuns.",
  "💡 Pare, desconfie e confirme antes de agir."]),
("PHISHING: O QUE É?",
 "Phishing é uma tentativa de enganar a pessoa para obter informações ou fazê-la realizar uma ação prejudicial.",
 ["Pode aparecer por e-mail, SMS, WhatsApp, redes sociais ou páginas falsas.",
  "O criminoso pode se passar por banco, loja, empresa, amigo ou serviço conhecido.",
  "Exemplo: uma mensagem falsa pede seus dados por meio de um link."]),
("ANTES DE CLICAR EM UM LINK...",
 "Siga uma sequência simples:",
 ["1. PARE — não clique por impulso.",
  "2. OBSERVE — veja quem enviou e o que está sendo pedido.",
  "3. CONFIRA — verifique o endereço e procure o serviço pelo canal oficial.",
  "4. CONFIRME — se for alguém conhecido, confirme por outro meio.",
  "5. SE HOUVER DÚVIDA, NÃO CLIQUE."]),
("SENHAS SEGURAS",
 "Evite senhas fáceis de adivinhar ou reutilizadas.",
 ["❌ Evite: 123456, senha123, nome + data de nascimento e a mesma senha em tudo.",
  "✅ Prefira senhas longas e difíceis de adivinhar.",
  "✅ Use senhas diferentes para serviços importantes.",
  "✅ Quando possível, use um gerenciador de senhas."]),
("AUTENTICAÇÃO EM DOIS FATORES (2FA)",
 "O 2FA adiciona uma segunda etapa de verificação ao login.",
 ["Descobrir apenas a senha deixa de ser suficiente para acessar a conta.",
  "O segundo fator pode ser um aplicativo autenticador, código ou outro método oferecido pelo serviço.",
  "💡 Ative o 2FA principalmente em contas importantes, como e-mail e serviços financeiros."]),
("PROTEÇÃO DE DADOS PESSOAIS",
 "Antes de compartilhar uma informação, pense se ela é realmente necessária.",
 ["• Evite compartilhar dados pessoais sem necessidade.",
  "• Não envie senhas ou códigos de autenticação para outras pessoas.",
  "• Tenha cuidado com fotos de documentos e dados expostos nas redes sociais.",
  "• Verifique a quem você está fornecendo uma informação e por qual motivo.",
  "• Revise permissões e configurações de privacidade dos aplicativos."]),
("SE EU CAIR EM UM GOLPE, O QUE FAZER?",
 "Não entre em pânico. Priorize a proteção das suas contas e procure ajuda.",
 ["1. Interrompa o contato com o possível golpista.",
  "2. Proteja as contas: troque senhas e encerre sessões suspeitas.",
  "3. Avise o banco, aplicativo ou empresa pelos canais oficiais, quando aplicável.",
  "4. Guarde evidências, como mensagens e comprovantes.",
  "5. Procure os canais oficiais e autoridades competentes quando necessário."]),
("DESAFIO: VOCÊ SABERIA IDENTIFICAR?",
 "“PARABÉNS! Você ganhou um prêmio. Clique aqui AGORA e informe seus dados para receber.”",
 ["A) Clicar rapidamente.", "B) Enviar os dados.", "C) Não clicar e verificar por canal oficial.", "D) Encaminhar aos contatos."]),
("QUIZ DE FIXAÇÃO",
 "Vamos verificar o que aprendemos sobre segurança digital.",
 ["1. Um link inesperado de desconhecido: A) clicar  B) não clicar e verificar  C) encaminhar.",
  "2. Boa prática de senha: A) mesma em tudo  B) dados pessoais  C) senhas fortes e diferentes.",
  "3. Para que serve o 2FA? A) adicionar uma camada de segurança  B) aumentar internet  C) substituir antivírus.",
  "Respostas: 1-B • 2-C • 3-A"]),
("MENSAGEM FINAL",
 "Segurança digital não é saber tudo. É desenvolver bons hábitos.",
 ["✓ Desconfie de mensagens inesperadas.",
  "✓ Pense antes de clicar.",
  "✓ Use senhas fortes e, quando disponível, autenticação em dois fatores.",
  "✓ Proteja seus dados pessoais.",
  "✓ Na dúvida, confirme a informação pelos canais oficiais.",
  "🔐 Informação + atenção + bons hábitos = mais segurança."])
]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Segurança Digital - Apresentação")
        self.root.geometry("1200x760")
        self.root.minsize(850, 600)
        self.root.configure(bg="#111827")
        self.i = 0
        self.full = False

        top = tk.Frame(root, bg="#111827")
        top.pack(fill="x")
        self.progress = tk.Label(top, bg="#111827", fg="#d1d5db", font=("Arial", 11))
        self.progress.pack(side="left", padx=22, pady=12)
        tk.Button(top, text="⛶ Tela cheia", command=self.fullscreen,
                  bg="#374151", fg="white", relief="flat").pack(side="right", padx=22, pady=8)

        self.area = tk.Frame(root, bg="#f8fafc")
        self.area.pack(fill="both", expand=True, padx=18)

        bottom = tk.Frame(root, bg="#111827")
        bottom.pack(fill="x")
        self.prev = tk.Button(bottom, text="← Anterior", command=self.previous,
                              bg="#374151", fg="white", relief="flat", padx=15, pady=8)
        self.prev.pack(side="left", padx=20, pady=10)
        tk.Label(bottom, text="← → ou Espaço para navegar • F11 tela cheia • Esc sair",
                 bg="#111827", fg="#9ca3af", font=("Arial", 10)).pack(side="left", expand=True)
        self.next = tk.Button(bottom, text="Próximo →", command=self.next_slide,
                              bg="#2563eb", fg="white", relief="flat", padx=15, pady=8)
        self.next.pack(side="right", padx=20, pady=10)

        root.bind("<Right>", lambda e: self.next_slide())
        root.bind("<space>", lambda e: self.next_slide())
        root.bind("<Left>", lambda e: self.previous())
        root.bind("<F11>", lambda e: self.fullscreen())
        root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.show()

    def clear(self):
        for w in self.area.winfo_children():
            w.destroy()

    def show(self):
        self.clear()
        title, subtitle, items = SLIDES[self.i]
        self.progress.config(text=f"Slide {self.i+1} de {len(SLIDES)}")
        self.prev.config(state="normal" if self.i else "disabled")
        self.next.config(text="Finalizar ✓" if self.i == len(SLIDES)-1 else "Próximo →")

        tk.Label(self.area, text=title, bg="#f8fafc", fg="#111827",
                 font=("Arial", 30, "bold"), wraplength=1050, justify="center").pack(pady=(40,12))
        tk.Label(self.area, text=subtitle, bg="#f8fafc", fg="#4b5563",
                 font=("Arial", 17), wraplength=980, justify="center").pack(pady=(0,25))

        for item in items:
            frame = tk.Frame(self.area, bg="#ffffff", highlightbackground="#e5e7eb", highlightthickness=1)
            frame.pack(fill="x", padx=70, pady=6)
            tk.Label(frame, text=item, bg="#ffffff", fg="#1f2937",
                     font=("Arial", 16), wraplength=980, justify="left", anchor="w").pack(
                         fill="x", padx=20, pady=14)

        if self.i == 10:
            tk.Button(self.area, text="Mostrar resposta: C",
                      command=lambda: messagebox.showinfo(
                          "Resposta", "C — Não clicar e verificar a informação por um canal oficial.\n\n"
                          "A mensagem tem sinais de alerta: prêmio, urgência e pedido de dados."),
                      bg="#2563eb", fg="white", relief="flat", padx=20, pady=10,
                      font=("Arial", 12, "bold")).pack(pady=18)

    def next_slide(self):
        if self.i < len(SLIDES)-1:
            self.i += 1
            self.show()
        else:
            if messagebox.askyesno("Fim", "A apresentação terminou.\n\nVoltar ao primeiro slide?"):
                self.i = 0
                self.show()

    def previous(self):
        if self.i > 0:
            self.i -= 1
            self.show()

    def fullscreen(self):
        self.full = not self.full
        self.root.attributes("-fullscreen", self.full)

    def exit_fullscreen(self):
        self.full = False
        self.root.attributes("-fullscreen", False)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
