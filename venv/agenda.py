from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda"
)

def main():
    campoNome = agenda.nome.text()
    campoEmail = agenda.email.text()
    campoTelefone = agenda.telefone.text()

    if agenda.rendencial.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.celular.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não Informado"

    cursor = banco.cursor()
    insert = "INSERT INTO tbl_dadosagendas(nome,email,telefone,tipoContato) values (%s,%s,%s,%s)"
    data = (str(campoNome),str(campoEmail),str(campoTelefone),tipoTelefone)
    cursor.execute(insert,data)
    banco.commit()
    print("salvo com sucersso")
    agenda.nome.setText("")
    agenda.email.setText("")
    agenda.telefone.setText("")

def consultarContato():
    listaContatos.show()
    cursor = banco.cursor()
    select = "SELECT * FROM tbl_dadosagendas"
    cursor.execute(select)
    contatosLidos = cursor.fetchall()
    listaContatos.tableWidget.setRowCount(len(contatosLidos))
    listaContatos.tableWidget.setColumnCount(5)
    for i in range (0, len(contatosLidos)):
        for f in range(0, 5):
            listaContatos.tableWidget.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))


def excluirContato():
    linhaContato = listaContatos.tableWidget.currentRow()
    listaContatos.tableWidget.removeRow(linhaContato)
    cursor = banco.cursor()
    select = "select id from tbl_dadosagendas"
    cursor.execute(select)
    contatos_lidos = cursor.fetchall()
    valorID = contatos_lidos[linhaContato][0]
    cursor.execute("delete from tbl_dadosagendas where id = " + str(valorID))
    banco.commit()

def updateConfirm():
    campoNome = telaEdicao.nomeAlterar.text()
    campoEmail = telaEdicao.emailAlterar.text()
    campoTelefone = telaEdicao.telefoneAlterar.text()

    if telaEdicao.rendencialAlterar.isChecked():
        tipoTelefone = "Residencial"
    elif telaEdicao.celularAlterar.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não Informado"
    id = getid()
    cursor = banco.cursor()
    upadate = "UPDATE  tbl_dadosagendas SET nome = %s ,email = %s ,telefone = %s ,tipoContato = %s where id = " + str(id)
    data = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
    cursor.execute(upadate, data)
    banco.commit()
    print("alterado com sucersso")
    telaEdicao.close()

def getid():
    linhaContato = listaContatos.tableWidget.currentRow()
    cursor = banco.cursor()
    select = "select id from tbl_dadosagendas"
    cursor.execute(select)
    contatos_lidos = cursor.fetchall()
    id = contatos_lidos[linhaContato][0]

    return id

def alterarContato():
    valorID = getid()
    seletWhithID = "select * from tbl_dadosagendas where id = " + str(valorID)
    cursor = banco.cursor()
    cursor.execute(seletWhithID)
    dadoLido = cursor.fetchall()
    telaEdicao.show()
    telaEdicao.nomeAlterar.setText(str(dadoLido[0][1]))
    telaEdicao.emailAlterar.setText(str(dadoLido[0][2]))
    telaEdicao.telefoneAlterar.setText(str(dadoLido[0][3]))
    if(str(dadoLido[0][4]) == "Residencial"):
        telaEdicao.rendencialAlterar.setChecked(True)
    else:
        telaEdicao.celularAlterar.setChecked(True)

def gerarPdf():
    cursor = banco.cursor()
    select = "select * from tbl_dadosagendas"
    cursor.execute(select)
    contatos_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("lista_contos.pdf")
    pdf.setFont("Times-Bold",14)
    pdf.drawString(200,800,"Lista Contatos")

    pdf.setFont("Times-Bold",12)
    pdf.drawString(10,750,"ID")
    pdf.drawString(100,750,"NOME")
    pdf.drawString(200,750,"EMAIL")
    pdf.drawString(400,750,"TELEFONE")
    pdf.drawString(500,750,"CONTATO")

    for i in range(0, len(contatos_lidos)):
        y = y + 50
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(10, 750 - y, str(contatos_lidos[i][0]))
        pdf.drawString(100, 750 - y, str(contatos_lidos[i][1]))
        pdf.drawString(200, 750 - y, str(contatos_lidos[i][2]))
        pdf.drawString(400, 750 - y, str(contatos_lidos[i][3]))
        pdf.drawString(500, 750 - y, str(contatos_lidos[i][4]))

    pdf.save()
    print("PDF gerado com sucesso!")

def voltar():
    listaContatos.close()
    agenda.show()

app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
listaContatos = uic.loadUi("tableContato.ui")
telaEdicao = uic.loadUi("update.ui")
telaEdicao.confirmar.clicked.connect(updateConfirm)
listaContatos.excluirContato.clicked.connect(excluirContato)
listaContatos.gerarPdf.clicked.connect(gerarPdf)
listaContatos.voltar.clicked.connect(voltar)
listaContatos.alterarContato.clicked.connect(alterarContato)

agenda.btnCadastrar.clicked.connect(main)
agenda.btnConsultar.clicked.connect(consultarContato)

agenda.show()
app.exec()
