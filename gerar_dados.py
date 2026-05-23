import csv
import random
from datetime import datetime, timedelta

random.seed(42)

nomes = [
    "Ana Paula Silva","Carlos Eduardo Santos","Fernanda Lima","João Pedro Oliveira",
    "Mariana Costa","Rafael Souza","Beatriz Almeida","Diego Ferreira","Camila Rodrigues",
    "Lucas Martins","Juliana Pereira","Thiago Nascimento","Larissa Carvalho","Mateus Gomes",
    "Priscila Araújo","Felipe Barros","Gabriela Ribeiro","André Monteiro","Vanessa Teixeira",
    "Bruno Castro","Natália Mendes","Rogério Freitas","Tatiane Cardoso","Leandro Pinto",
    "Simone Correia","Fábio Moreira","Aline Nunes","Renato Vieira","Patrícia Lopes",
    "Marcos Rocha","Cristiane Azevedo","Wellington Moura","Sandra Cunha","Alexandre Melo",
    "Débora Cavalcante","Rodrigo Machado","Claudia Andrade","Sérgio Figueiredo","Elaine Ramos",
    "Paulo Henrique Lima","Adriana Campos","Gustavo Borges","Cíntia Barbosa","Marcelo Duarte",
    "Letícia Vilaça","Eronildo Bezerra","Rosangela Tavares","Cleber Santana","Joelma Reis",
    "Wanderley Queiroz","Edilene Carmo","Gilson Fontes","Neusa Farias","Osmar Pacheco",
    "Edna Guimarães","Nilton Vasconcelos","Sueli Coelho","Elias Medeiros","Célia Braga",
    "Valdeci Nogueira","Isaura Pires","Ermando Leite","Graciele Sampaio","Aurélio Bastos",
    "Dilma Fonseca","Humberto Rezende","Ivone Brito","Jailson Cavalcante","Lurdes Xavier",
    "Murilo Bezerra","Odete Cardoso","Percival Moura","Quesia Dantas","Salvador Borba"
]

operadores = ["Ana Lima","Carlos M.","Fernanda S.","Diego R.","Beatriz K.","Rafael T."]
status_opcoes = ["PAGO","PENDENTE","QUEBRADO","NEGOCIANDO","EM ATRASO"]
status_peso   = [0.35, 0.30, 0.10, 0.12, 0.13]

ddds = ["11","21","31","41","51","61","71","81","85","91","92","98","62","67","65","47","48"]

def cpf_fake(i):
    base = f"{i:09d}"
    d1 = sum(int(base[j])*(10-j) for j in range(9)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    base2 = base + str(d1)
    d2 = sum(int(base2[j])*(11-j) for j in range(10)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    c = base + str(d1) + str(d2)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

def telefone():
    ddd = random.choice(ddds)
    num = f"9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    return f"({ddd}) {num}"

base_date = datetime(2025, 1, 1)

rows = []
for i in range(1, 601):
    nome = random.choice(nomes) + (f" {random.choice(['Jr.','Filho','Neto',''])}" if random.random()<0.15 else "")
    nome = nome.strip()
    cpf  = cpf_fake(i)
    tel  = telefone()

    dias_atraso = random.choices(
        [random.randint(1,30), random.randint(31,60), random.randint(61,90), random.randint(91,180)],
        weights=[0.25, 0.30, 0.25, 0.20]
    )[0]

    valor_divida = round(random.choices(
        [random.uniform(300,2000), random.uniform(2000,8000), random.uniform(8000,25000), random.uniform(25000,60000)],
        weights=[0.45, 0.35, 0.15, 0.05]
    )[0], 2)

    status = random.choices(status_opcoes, weights=status_peso)[0]

    if status == "PAGO":
        valor_pago = valor_divida
        data_pagamento = (base_date + timedelta(days=random.randint(0,500))).strftime("%d/%m/%Y")
    elif status in ("NEGOCIANDO","QUEBRADO"):
        valor_pago = round(valor_divida * random.uniform(0.1, 0.5), 2)
        data_pagamento = ""
    else:
        valor_pago = 0.00
        data_pagamento = ""

    data_venc = (base_date + timedelta(days=random.randint(0,400))).strftime("%d/%m/%Y")
    operador = random.choice(operadores)

    faixa = ("0-30 dias" if dias_atraso<=30 else
             "31-60 dias" if dias_atraso<=60 else
             "61-90 dias" if dias_atraso<=90 else "90+ dias")

    rows.append([i, nome, cpf, tel, valor_divida, dias_atraso, faixa,
                 status, valor_pago, operador, data_venc, data_pagamento])

header = ["ID","Nome","CPF","Telefone","Valor_Divida","Dias_Atraso","Faixa_Atraso",
          "Status","Valor_Pago","Operador","Data_Vencimento","Data_Pagamento"]

with open("/home/claude/cobranca_dados.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(header)
    w.writerows(rows)

print(f"Gerado: {len(rows)} registros")
print("Primeiras 3 linhas:")
for r in rows[:3]: print(r)
