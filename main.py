from PyQt5 import uic ,QtWidgets 
import mysql.connector 
from mysql.connector import cursor
from reportlab.pdfgen import canvas

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


numero_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Lun@rS3nt1r",
    database="box_games",
)

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold",18)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold",12)
    pdf.drawString(10,750,"ID")
    pdf.drawString(70,750,"CODIGO")
    pdf.drawString(150,750,"PRODUTO")
    pdf.drawString(370,750,"PREÇO")
    pdf.drawString(430,750,"CATEGORIA")

    for linha in range(0, len(dados_lidos)):
        y = y + 50 
        pdf.drawString(10,750 - y, str(dados_lidos[linha][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[linha][1]))
        pdf.drawString(150,750 - y, str(dados_lidos[linha][2]))
        pdf.drawString(370,750 - y, str(dados_lidos[linha][3]))
        pdf.drawString(430,750 - y, str(dados_lidos[linha][4]))
    pdf.save()
    print("PDF FOI GERADO !")

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))

def salvar_dados_editados():
    # busca o número do ID
    global numero_id
    # Valor digitado no lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    # Atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}',preco = '{}', categoria = '{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    # Atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    abre_segunda_tela()


def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
  
def abre_segunda_tela():
    segunda_tela.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for linha in range(0, len(dados_lidos)):
        for coluna in range(0,5):
            segunda_tela.tableWidget.setItem(linha,coluna,QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def main():
    line1 = formulario.lineEdit.text()
    line2 = formulario.lineEdit_2.text()
    line3 = formulario.lineEdit_3.text()
    categoria = ""

    if formulario.radioButton.isChecked():
        print("Categoria Jogo foi selecionada.")
        categoria = "Jogo"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Acessório foi selecionada.")
        categoria = "Acessório"
    else:
        print("Categoria Console foi selecionada.")
        categoria = "Console"

    print("Código :",line1)
    print("Descrição :",line2)
    print("Preço :","R$",line3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(line1),str(line2),str(line3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

app = QtWidgets.QApplication ([])
formulario = uic.loadUi("form.ui")
segunda_tela = uic.loadUi("listar_dados.ui")
tela_editar = uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(main)
formulario.pushButton_2.clicked.connect(abre_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()
