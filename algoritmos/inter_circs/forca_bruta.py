from desenhos import sleep

def forca_bruta (l):
    "Algoritmo força bruta para encontrar todos as interseções entre uma lista de círculos"

    for i in range (len(l)):
        l[i].hilight (cor_borda = 'orange', grossura = 2)
        sleep()
        for j in l[i+1:]:
            j.hilight (cor_borda = 'green')
            sleep()
            for p in l[i].intersection(j):
                p.hilight ('yellow')
            j.unhilight ()
        l[i].unhilight ()
    
    
