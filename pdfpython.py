import argparse
import os
import subprocess
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as pld
from datetime import datetime


class AutoReport():
    """
    Classe para a criação de relatorios automatizado.
    """
    _width = 10
    _scaleFactor = 2.6685633001422477
    _heigth = _width / _scaleFactor
    def __init__(self, dbpath):
        """
        Construtor da classe para criação de relatorios automatizado.
        """
        self._dbpath = dbpath

    def makePDF(self):
        try:
            content = r'''\documentclass{article}
            \usepackage[brazilian]{babel}
            \usepackage[utf8]{inputenc}
            \usepackage[T1]{fontenc}
            \usepackage{amsmath}
            \usepackage{indentfirst}
            \usepackage{graphicx}
            \usepackage{multicol,lipsum}
            \usepackage{float}
            \usepackage[hidelinks]{hyperref}
            \usepackage[right = 2cm, left=2cm, top=2cm, bottom=2.5cm]{geometry}
            
            \begin{document}
            \begin{center}
            \textbf{\huge %(school)s \\}
            \vspace{1cm}
            \textbf{\Large %(title)s \\}
            \end{center}
            \newpage
            Aqui sera escrito todo o relatorio etcetcetc    
            %(testeVariable)s \\
            aaaaaaaaaaaaaaaaaaaaaaaaaa
            \begin{figure}[H]
            \centering
            \includegraphics[width = \linewidth]{figuras/%(graficoResposta)s}
            \caption{Respostas transitorias de sistemas din\^amicos.}
            \label{fig:Respostas}
            \end{figure}
            \end{document}
            '''

            parser = argparse.ArgumentParser()
            parser.add_argument('-c', '--course')
            parser.add_argument('-t', '--title', default= 'Relatorio')
            parser.add_argument('-n', '--name',) 
            parser.add_argument('-s', '--school', default= 'Universidade Federal de Juiz de Fora')
            parser.add_argument('-tv', '--testeVariable', default = "Testando a variavel")
            parser.add_argument('--graficoResposta', default='teste.pdf')

            args = parser.parse_args()

            with open('report.tex','w') as f:
                f.write(content%args.__dict__)

            cmd = ['pdflatex', '-interaction', 'nonstopmode', 'report.tex']
            proc = subprocess.Popen(cmd)
            proc.communicate()

            retcode = proc.returncode
            if not retcode == 0:
                os.unlink('report.pdf')
                raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 

            os.unlink('report.tex')
            os.unlink('report.log')

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'Tipo de dado após tratar {self._t[1]}')
            print('PDF criado com sucesso!')

        except Exception as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Erro: ",e)



    def acessData(self):
        dat = sqlite3.connect(self._dbpath)
        query = dat.execute("SELECT * From Aspera")
        cols = [column[0] for column in query.description]
        self._data = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

        # Trata os dados de tempo
        self._time = [self._data['timestamp'][i].split(' ')[1] for i in range(len(self._data['timestamp']))]
        self._time = [datetime.strptime(self._time[i], '%H:%M:%S.%f') for i in range(len(self._time))]

    def makeGraphs(self):     

        plt.figure(figsize = (self._width, self._heigth))
        # self._t = pld.date2num(self._data['timestamp'])
        self._t = pld.date2num(self._time)
        plt.plot_date(self._t, self._data['Altitude'], '-', linewidth = 3, label = 'Altitude')
        plt.xlim([self._t[0], self._t[-1]])
        plt.grid()
        plt.legend()
        plt.savefig('figuras/teste.pdf', bbox_inches = 'tight')
        plt.show()





if __name__ == '__main__':
    path = 'C:\\Users\Administrador\\Desktop\\SSR\\db\\scada.db'
    teste = AutoReport(path)
    teste.acessData()
    teste.makeGraphs()
    teste.makePDF()