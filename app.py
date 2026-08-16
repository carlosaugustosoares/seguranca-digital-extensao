from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3, uuid, csv, io, socket
import qrcode
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
BANCO = os.getenv("BANCO", "banco.db")
SENHA_ADMIN = os.getenv("SENHA_ADMIN")

PERGUNTAS = [
    {"id":1,"texto":"Você recebe uma mensagem dizendo que ganhou um prêmio e precisa clicar em um link. O que deve fazer?","opcoes":["Clicar imediatamente no link","Informar seus dados pessoais","Verificar a mensagem e evitar links suspeitos","Encaminhar a mensagem para outras pessoas"],"correta":2,"explicacao":"Mensagens que prometem prêmios e pedem para clicar em links podem ser tentativas de golpe. Antes de clicar, verifique a origem e procure informações pelos canais oficiais."},
    {"id":2,"texto":"Qual dessas é uma boa prática para criar uma senha?","opcoes":["Usar apenas números","Usar seu nome e data de nascimento","Usar uma senha forte e difícil de adivinhar","Usar a mesma senha em todos os sites"],"correta":2,"explicacao":"Uma senha forte deve ser difícil de adivinhar. Também é recomendável evitar reutilizar a mesma senha em vários serviços."},
    {"id":3,"texto":"O que é phishing?","opcoes":["Um tipo de antivírus","Uma tentativa de enganar alguém para obter informações","Um sistema operacional","Um aplicativo de mensagens"],"correta":1,"explicacao":"Phishing é uma tentativa de enganar a pessoa para obter informações, como senhas ou dados pessoais, normalmente por meio de mensagens, e-mails ou páginas falsas."},
    {"id":4,"texto":"Para que serve a autenticação em dois fatores (2FA)?","opcoes":["Para deixar a internet mais rápida","Para aumentar a segurança da conta","Para criar uma senha automaticamente","Para apagar vírus do computador"],"correta":1,"explicacao":"A autenticação em dois fatores adiciona uma segunda etapa de verificação, dificultando o acesso à conta mesmo quando alguém descobre a senha."},
    {"id":5,"texto":"Você recebe um e-mail de um banco solicitando sua senha. O que deve fazer?","opcoes":["Enviar a senha imediatamente","Responder perguntando o motivo","Ignorar a solicitação e verificar pelos canais oficiais do banco","Encaminhar para um amigo"],"correta":2,"explicacao":"Bancos e serviços legítimos não devem pedir sua senha por mensagens. Quando houver dúvida, acesse o aplicativo ou site oficial diretamente, sem usar links da mensagem."}
]

def conectar():
    c=sqlite3.connect(BANCO); c.row_factory=sqlite3.Row; return c

def criar_banco():
    c=conectar()
    c.execute("""CREATE TABLE IF NOT EXISTS participantes (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo TEXT UNIQUE NOT NULL, data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS respostas (id INTEGER PRIMARY KEY AUTOINCREMENT, participante_id INTEGER NOT NULL, pergunta INTEGER NOT NULL, resposta INTEGER NOT NULL, correta INTEGER NOT NULL, FOREIGN KEY(participante_id) REFERENCES participantes(id))""")
    c.commit(); c.close()

def obter_ip_local():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close(); return ip
    except OSError: return "127.0.0.1"

def admin_logado(): return session.get("admin") is True

@app.route("/")
def inicio(): return render_template("index.html")

@app.route("/quiz")
def quiz(): return render_template("quiz.html", perguntas=PERGUNTAS)

@app.route("/enviar", methods=["POST"])
def enviar():
    c=conectar(); codigo=str(uuid.uuid4())[:8].upper(); cur=c.execute("INSERT INTO participantes(codigo) VALUES(?)",(codigo,)); pid=cur.lastrowid; pontos=0; resultado=[]
    for p in PERGUNTAS:
        v=request.form.get(f"pergunta_{p['id']}"); resposta=int(v) if v is not None else -1; correta=int(resposta==p["correta"]); pontos+=correta
        c.execute("INSERT INTO respostas(participante_id,pergunta,resposta,correta) VALUES(?,?,?,?)",(pid,p["id"],resposta,correta))
        resultado.append({"pergunta":p["texto"],"resposta_marcada":p["opcoes"][resposta] if 0<=resposta<len(p["opcoes"]) else "Não respondida","resposta_correta":p["opcoes"][p["correta"]],"correta":correta,"explicacao":p["explicacao"]})
    c.commit(); c.close(); return render_template("resultado.html",pontuacao=pontos,total=len(PERGUNTAS),codigo=codigo,respostas=resultado)

@app.route("/admin",methods=["GET","POST"])
def admin_login():
    if admin_logado(): return redirect(url_for("dashboard"))
    if request.method=="POST":
        if request.form.get("senha","")==SENHA_ADMIN: session["admin"]=True; return redirect(url_for("dashboard"))
        flash("Senha incorreta.")
    return render_template("admin_login.html")

@app.route("/admin/sair")
def admin_sair(): session.pop("admin",None); return redirect(url_for("admin_login"))

@app.route("/dashboard")
def dashboard():
    if not admin_logado(): return redirect(url_for("admin_login"))
    c=conectar(); participantes=c.execute("SELECT COUNT(*) total FROM participantes").fetchone()["total"]; total=c.execute("SELECT COUNT(*) total FROM respostas").fetchone()["total"]; acertos=c.execute("SELECT COALESCE(SUM(correta),0) total FROM respostas").fetchone()["total"]; erros=total-acertos; geral=round(acertos/total*100,1) if total else 0
    estatisticas=[]
    for p in PERGUNTAS:
        d=c.execute("SELECT COUNT(*) total, COALESCE(SUM(correta),0) acertos FROM respostas WHERE pergunta=?",(p["id"],)).fetchone(); t=d["total"]; a=d["acertos"]; estatisticas.append({"pergunta":p["id"],"texto":p["texto"],"total":t,"acertos":a,"erros":t-a,"percentual":round(a/t*100,1) if t else 0})
    ultimos=c.execute("SELECT p.codigo,p.data_hora,COALESCE(SUM(r.correta),0) acertos FROM participantes p LEFT JOIN respostas r ON r.participante_id=p.id GROUP BY p.id ORDER BY p.id DESC LIMIT 10").fetchall(); c.close()
    return render_template("dashboard.html",participantes=participantes,total_respostas=total,total_acertos=acertos,total_erros=erros,percentual_geral=geral,estatisticas=estatisticas,ultimos=ultimos)

@app.route("/admin/qr")
def qr_code():
    if not admin_logado(): return redirect(url_for("admin_login"))
    endereco=f"http://{obter_ip_local()}:5000"; imagem=qrcode.make(endereco); arquivo=io.BytesIO(); imagem.save(arquivo,format="PNG"); arquivo.seek(0); return send_file(arquivo,mimetype="image/png")

@app.route("/admin/qr-info")
def qr_info():
    if not admin_logado(): return redirect(url_for("admin_login"))
    return render_template("qr.html",endereco=f"http://{obter_ip_local()}:5000")

@app.route("/admin/exportar")
def exportar():
    if not admin_logado(): return redirect(url_for("admin_login"))
    c=conectar(); linhas=c.execute("SELECT p.codigo,p.data_hora,r.pergunta,r.resposta,r.correta FROM participantes p JOIN respostas r ON r.participante_id=p.id ORDER BY p.id,r.pergunta").fetchall(); c.close(); out=io.StringIO(); w=csv.writer(out); w.writerow(["codigo_participante","data_hora","pergunta","resposta","correta"])
    for x in linhas: w.writerow([x["codigo"],x["data_hora"],x["pergunta"],x["resposta"],x["correta"]])
    data=io.BytesIO(out.getvalue().encode("utf-8-sig")); return send_file(data,mimetype="text/csv",as_attachment=True,download_name="respostas_seguranca_digital.csv")

if __name__=="__main__":
    criar_banco(); print("\nQUIZ DE SEGURANÇA DIGITAL\nComputador: http://127.0.0.1:5000\nRede Wi-Fi: http://%s:5000\nDashboard: http://127.0.0.1:5000/admin\nSenha configurada no arquivo .env\n"%obter_ip_local()); app.run(debug=True,host="0.0.0.0",port=5000)
