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
    _width = 12
    _scaleFactor = 2.6685633001422477
    _heigth = _width / _scaleFactor

    _width2 = 12
    _scaleFactor2 = 1.5
    _heigth2 = _width2 / _scaleFactor2

    # _width3 = 
    # _scaleFactor3 = 
    # _height3 = 
    def __init__(self, dbpath):
        """
        Construtor da classe para criação de relatorios automatizado.
        """
        self._dbpath = dbpath

    def makePDF(self):
        try:
            content = r'''\documentclass[11pt]{article}
                            \usepackage[brazilian]{babel}
                            \usepackage[utf8]{inputenc}
                            \usepackage[T1]{fontenc}
                            \usepackage{amsmath}
                            \usepackage{indentfirst}
                            \usepackage{graphicx}
                            \usepackage{multicol,lipsum}
                            \usepackage{float}
                            \usepackage[hidelinks]{hyperref}
                            \usepackage[right = 1cm, left=1cm, top=1cm, bottom=2cm]{geometry}
                            \usepackage{multicol}
                            \usepackage{anyfontsize}
                            \usepackage[export]{adjustbox}
                            \usepackage{tikz}
                            \usepackage{xcolor}
                            \definecolor{my_background}{HTML}{F2F4F3}
                            \begin{document}


                            
                            \noindent \fcolorbox{black}{my_background} {\fcolorbox{black}{my_background}{% 
                                
                                \parbox{\textwidth}{%
                                
                                    \begin{minipage}[left]{.48\linewidth}
                            \begin{figure}[H]
                                \flushleft
                                \includegraphics[height = 150px, left]{figuras/logo_supernova (2).png}
                            \end{figure}
                            \end{minipage}
                            \begin{minipage}[right]{.48\linewidth}
                            \begin{figure}[H]
                                \includegraphics[height = 150px, right]{figuras/lasc.png}
                            \end{figure}
                            \end{minipage}\vspace{10pt}



                            \begin{minipage}[left]{.55\linewidth}
                            {\Large
                            \textbf{Equipe:} \vspace{6pt}

                            \textbf{Competição:} \vspace{6pt}

                            \textbf{Projeto:}\vspace{10pt}

                            \textbf{Missão:}\vspace{6pt}
                            }

                            \end{minipage}
                            \begin{minipage}[right]{.42\linewidth}
                            {\Large
                            \textbf{Data:}\vspace{6pt}

                            \textbf{Categoria:}\vspace{6pt}

                            \textbf{Local de lançamento:}\vspace{10pt}

                            \textbf{Janela de lançamento:}\vspace{6pt}
                            }
                            \end{minipage}
                                }%
                            }}

                            \end{document}
            '''

            parser = argparse.ArgumentParser()
            parser.add_argument('-c', '--course')
            parser.add_argument('-t', '--title', default= 'Relatorio')
            parser.add_argument('-n', '--name',) 
            parser.add_argument('-s', '--school', default= 'Universidade Federal de Juiz de Fora')
            parser.add_argument('-tv', '--testeVariable', default = "Testando a variavel")
            parser.add_argument('--altitude', default='altitude.pdf')

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
            print('PDF criado com sucesso!')

        except Exception as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Erro: ",e)



    def acessData(self):
        '''
        Método que acessa o banco de dados e extrai todos os dados
        '''
        dat = sqlite3.connect(self._dbpath)
        query = dat.execute("SELECT * From Aspera")
        cols = [column[0] for column in query.description]
        self._data = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

        # Trata os dados de tempo
        self._time = [self._data['timestamp'][i].split(' ')[1] for i in range(len(self._data['timestamp']))]
        self._time = [datetime.strptime(self._time[i], '%H:%M:%S.%f') for i in range(len(self._time))]
        self._time = pld.date2num(self._time)
        print(self._time)

    def makeGraphs(self):     
        '''
        Método que cria todas as figuras/gráficos para implementar no relatorio.
        '''
        #  Gráfico de Altitude
        fig, axs = plt.subplots(figsize = (self._width, self._heigth))        
        plt.plot_date(self._time, self._data['Altitude'], '-', linewidth = 1.5, label = 'Altitude')
        plt.xlim([self._time[0], self._time[-1]])
        plt.grid()
        plt.legend()
        axs.xaxis.set_major_formatter(pld.DateFormatter('%H:%M:%S'))
        plt.xlabel('Horário')
        plt.ylabel('Altitude [m]')
        plt.title('Variação da altitude do foguete')
        plt.savefig('figuras/altitude.pdf', bbox_inches = 'tight')


        # Gráfico de posicao geografica
        fig, axs = plt.subplots(2, figsize = (self._width2, self._heigth2))
        axs[0].set_title('Variação da posição geografica do foguete')
        axs[0].plot(self._time, self._data['Latitude'], '-', linewidth = 1, label ='Latitude')
        axs[0].set_xlim([self._time[0], self._time[-1]])
        axs[0].xaxis.set_major_formatter(pld.DateFormatter('%H:%M:%S'))
        axs[0].legend(loc='upper right')
        axs[0].set_ylabel('Coordenada')
        axs[0].grid()

        axs[1].plot(self._time, self._data['Longitude'], '-', linewidth = 1, label ='Longitude', color = 'tab:orange')
        axs[1].set_xlim([self._time[0], self._time[-1]])
        axs[1].xaxis.set_major_formatter(pld.DateFormatter('%H:%M:%S'))
        axs[1].legend(loc='upper right')
        axs[1].grid()
        axs[1].set_xlabel('Tempo')
        axs[1].set_ylabel('Coordenada')

        plt.savefig('figuras/posicaoGeografica.pdf', bbox_inches = 'tight')


        plt.show()









if __name__ == '__main__':
    path = 'C:\\Users\Administrador\\Desktop\\SSR\\db\\scada.db'
    teste = AutoReport(path)
    teste.acessData()
    teste.makeGraphs()
    teste.makePDF()