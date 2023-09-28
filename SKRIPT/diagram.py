import numpy as np
import matplotlib.pyplot as plt
import variabler as v
import functions as func

def antall_funn(xakse=0,yakse=0):
    # Definere en cursor
    mariaDB_connection, DB_cursor = func.database_connection()



    SQL_antall_funn = """
    SELECT Xmjosnr, count(*)
    FROM Logger
    WHERE Loggtype = "Found it"
    GROUP BY Xmjosnr
    """
    DB_cursor.execute(SQL_antall_funn)
    # Gjør om "liste av tuple" til "to lister". Dette for at den ene listen representerer x-aksen og den andre y-aksen
    xakse,yakse = list(map(list, zip(*DB_cursor.fetchall())))

    antall_funn = yakse
    bars = []
    # Gjør så Xmjosnr under 10 vil starte med 0
    for each in xakse:
        bars.append(str(each).zfill(2))


    # # Generering av tilfeldig testdata
    # bars = []
    # antall_funn = []
    # xakse = []
    # for i in range(0,24):
    #     xakse.append(i+1)
    #     antall_funn.append(random.randint(10,40))
    #     bars.append(str(i+1).zfill(2))
    # print(antall_funn)
    # print(bars)

    white = "white"
    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(111)
    y_pos = np.arange(len(bars))

    # Create names on the x-axis
    plt.yticks(y_pos, bars)

    # Legg til grid
    plt.grid(axis = 'x', linestyle = 'dotted', linewidth = 0.5, color="#b0b0b0")

    # Fargelegging
    ax.spines['top'].set_color(white)
    ax.spines['right'].set_color(white)
    ax.spines['bottom'].set_color(white)
    ax.spines['left'].set_color(white)
    ax.xaxis.label.set_color(white)
    ax.yaxis.label.set_color(white)
    ax.tick_params(axis='both', colors=white)

    # We change the fontsize of minor ticks label 
    ax.tick_params(axis='both', which='major', labelsize=14)

    #specify axis tick step sizes
    plt.xticks(np.arange(0, max(antall_funn)+5, 5))
    plt.yticks(np.arange(0, max(xakse), 1))
    
    # Legg til titler
    plt.title("Antall funn per cache",fontsize=24).set_color(white)
    plt.xlabel("Antall funn",fontsize=19)
    plt.ylabel("Hvilken dag",fontsize=19)

    # Lage bars
    plt.barh(y_pos, antall_funn, height=0.6, color="#39007a")

    # Lagre / vise diagrammet
    plt.savefig(v.filnavn_GRAF_antall_funn_per_dag, transparent=True)
    # plt.show()
    return

if __name__ == "__main__":
    # Dette er testdata
    result = [[1, 2, 3, 4, 5, 6], [17, 5, 15, 7, 12, 6]]
    xmjosnr,antall_funn_data = result
    antall_funn(xmjosnr,antall_funn_data)
