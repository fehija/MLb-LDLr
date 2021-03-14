# 0.- PARTE WEB- FORMULARIO para INPUT DE DATOS
from flask import Flask, render_template, request

app = Flask(__name__) # __name__ función de python que sirve para asegurarse de que arrancamos del archivo inicial

# Clase para crear un array de objetos con las variables de la query 
class queryClass:  
    def __init__(self, analyzed_mutation, pathogenic_mutation, affected_domain, position_conservation, size_change, hydrophobicity_change, charge_change):  
        self.analyzed_mutation = analyzed_mutation  
        self.pathogenic_mutation = pathogenic_mutation
        self.affected_domain = affected_domain 
        self.position_conservation = position_conservation  
        self.size_change = size_change 
        self.hydrophobicity_change = hydrophobicity_change  
        self.charge_change = charge_change 

# Inicializamos la lista de queries vacía 
querylist = []  

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/output', methods=['POST'])
def output():
    
    if request.method =='POST':
        data_input =request.form['data_input']
        # PROGRAMA dentro del if (para que corra hasta que haya datos ????)
        # dividir input en diferentes inputs
        if len(data_input) < 2:
            dataList = "No data inserted !!! ; Return to Home and try again !!!"
            return render_template ('error_1.html')
        else:
            querylist.clear() 
            dataList = data_input.split(",")
            print ("mutation list is: ", dataList)
            print (data_input)
        
            print (type(dataList))
            mutNumber = int(len(dataList)) # definir variable como número que corresponden al número de elementos de las lista
            print(mutNumber)
            print(type(mutNumber))
            
        #if mutNumber > 5:
        #    return render_template ('error_2.html')
        #else:
            
            # Generating lists from data input (using list comprehension + split() )
            # Extracting positions and aa's or nt from list of strings 
            StringInput = str (dataList)
            
            if  ":" in StringInput :
                DNAposList = [str(sub.split(':')[0]) for sub in dataList] 
                ntList = [str(sub1.split(':')[1]) for sub1 in dataList]
                # print DNA Data Input 
                print("The list of nt positions: " + str(DNAposList))
                print("The list of mutant nt's : " + str(ntList))
                print("\n")

                #Convertir datos DNA a AA
                from DNAsequence import DNAseq
                from PositionInCodon import PosInCodon
                from GeneticCODE import GCODE

                archivo3 = open("static/DNAquery.txt","w")
                archivo3.write(" [DNA input] ")

                posList = []
                aaList = []
                for (ntposition,nt2) in zip (DNAposList,ntList):
                #INFO FROM POSITION
                    nt1 = (DNAseq.get(ntposition))
                    Ncodon = str(round(int(ntposition)/3 + 0.2))
                    ntCode = str(round(int(ntposition)/3, 1))
                    ORFtype = (PosInCodon.get(ntCode))
                    print ("Original nucleotide is: ", nt1)
                    print ("Codon or aa Number = ", Ncodon)
                    print ("ntCode = ", ntCode)
                    print ("ORF Type is: ", ORFtype)
                    if ORFtype == "a":
                        beta = (DNAseq.get(str(int(ntposition)+1)))
                        gamma = (DNAseq.get(str(int(ntposition)+2)))
                        OldCodon = (nt1 + beta + gamma)
                        NewCodon = (nt2 + beta + gamma)
                    elif ORFtype == "b":
                        alfa =  (DNAseq.get(str(int(ntposition)-1)))
                        gamma = (DNAseq.get(str(int(ntposition)+1)))
                        OldCodon = (alfa + nt1 + gamma)
                        NewCodon = (alfa + nt2 + gamma)
                    else :
                        alfa = (DNAseq.get(str(int(ntposition)-2)))
                        beta = (DNAseq.get(str(int(ntposition)-1)))
                        OldCodon = (alfa + beta + nt1)
                        NewCodon = (alfa + beta + nt2)
                    
                    print ("CODONS are:", OldCodon, NewCodon)

                    a1 = (GCODE.get(OldCodon))
                    a2 = (GCODE.get(NewCodon))
                    print (a1,a2)
                    
                    posList.append (Ncodon)
                    aaList.append (a2)
                    print (posList, aaList)
                    

                    archivo3.write( nt1 )
                    archivo3.write( str(ntposition) )
                    archivo3.write( nt2 )
                    archivo3.write(",")    
                archivo3.close()

            elif "." in StringInput :
                posList = [str(sub.split('.')[0]) for sub in dataList] 
                aaList = [str(sub1.split('.')[1]) for sub1 in dataList] 
                # print Aminoacid Data Input 
                print("The list of positions: " + str(posList))
                print("The list of mutant aa's : " + str(aaList))
                print("\n")
            else:     
                return render_template ('error_1.html')
            # ITERATIVE PROGRAM
            #from functions import maths1
            from sequence import seq,trans
            from charge_mod import charge, C_change
            from aa_prob import ori, nue

            archivo = open("static/results.txt","w")
            archivo2 = open("static/query.txt","w")
            archivo2.write(" [Aminoacid change(s)] ")
            
            for (position,aa2) in zip (posList,aaList):
            #INFO FROM POSITION
                aa1 = (seq.get(position))
                a1 = (trans.get(aa1))
                ori_prob = ori.get(a1)
                #Lo que hacía la función "maths1(position)""
                from cons_prob import Pos_Cons
                cons = (Pos_Cons.get(position))
                
                if cons < 0.3:
                    Cons_Prob = 0.363636363636364
                    PosCons = "Very Low"
                    print("WARNING! too low conservation value --> Probability value assigned from the FIRST CATHEGORY") 
                elif cons >= 0.3 and cons <=0.4178:
                    Cons_Prob = 0.363636363636364
                    PosCons = "Low"
                elif cons > 0.4178 and cons <=0.5326:
                    Cons_Prob = 0.45
                    PosCons = "Medium"
                elif cons > 0.5326 and cons <=0.6474:
                    Cons_Prob = 0.726190476190476
                    PosCons = "Medium"
                elif cons > 0.6474 and cons <=0.7622:
                    Cons_Prob = 0.95959595959596
                    PosCons = "Medium"
                elif cons > 0.7622 and cons <=0.881:
                    Cons_Prob = 0.992957746478873
                    PosCons = "High"
                elif cons > 0.881:
                    Cons_Prob = 0.992957746478873
                    PosCons = "Very High"
                    print("WARNING! too high conservation value --> Probability value assigned from the LAST CATHEGORY")
                else:
                    print("Conservation probability value not found")

                print("For position ", position, "the Original aminoacid is ",aa1,"(",a1,")"," ; conservation factor= ",cons, "; Assigned probability= ", Cons_Prob)


                print("Prob of original aa: ",ori_prob)

                # Probabilidad asociada al dominio donde se da la mutación
                from domain import domProb
                posi = int(position) #para convertir el input en número entero
                if posi >= 0 and posi <= 21:
                    d_pos = "Signal sequence"
                elif posi >= 22 and posi <= 293:
                    d_pos = "LBD"
                elif posi >=294 and posi <= 332:
                    d_pos = "EGF-A"
                elif posi >=333 and posi <= 376:
                    d_pos = "EGF-B"
                elif posi >= 377 and posi <= 642:
                    d_pos = "B-propeller"
                elif posi >= 643 and posi <= 699:
                    d_pos = "EGF-C"
                elif posi >= 700 and posi <= 747:
                    d_pos = "O-linked"
                elif posi >= 748 and posi <= 810:
                    d_pos = "Intermembrane"
                elif posi >= 811 and posi <= 860:
                    d_pos = "Cytosolic"    
                else:
                    print("Position without domain assigment")

                print("The domain affected is: ", d_pos)

                d_prob = (domProb.get(d_pos))
                print("The probability related to the affected domain: ",d_prob)
                

            #INFO FROM NEW OR MUTANT AA
                if aa2 in trans:
                    a2 = (trans.get(aa2))
                    print("The new aa: ", a2, "(inserted in 1 letter code)")
                else :
                    a2 = aa2
                    print("The new aa: ", aa2,"(inserted in 3 letter code)")
                
                nue_prob = nue.get(a2)
                print("Prob of mutant aa: ",nue_prob)
                
                change = (charge.get(a1)+charge.get(a2))
                cc = C_change.get(change)
                print("Charge change: ", change, " Assigned Probability: ", cc)

                if change == "uu" :
                    Cchange = "No"
                    print("uu found")
                elif change == "pp" :
                    Cchange = "No"
                    print("pp found")
                elif change == "nn" :
                    Cchange = "No"
                    print("nn found")
                else :
                    Cchange = "Yes"

                # Probabilidad asociada al cambio de hidrofobicidad
                from hydro import hyd

                h_old = (hyd.get(a1))
                h_new = (hyd.get(a2))
                hyd_change = h_new - h_old

                # Para EVITAR QUE CUANDO NO EXISTA CAMBIO DE AMINOÁCIDO DE UN RESULTADO DE PROBALIDAD
                if hyd_change == 0 :
                    hydProb = 0.861111111111111
                    Hchange = "No"                
                elif hyd_change >= -8.5 and hyd_change <= -4.8:
                    hydProb = 0.966101694915254
                    Hchange = "High"
                elif hyd_change > -4.8 and hyd_change <= -1.6:
                    hydProb = 0.902857142857143
                    Hchange = "Medium"
                elif hyd_change > -1.6 and hyd_change <= 1.6:
                    hydProb = 0.861111111111111
                    Hchange = "Low"
                elif hyd_change > 1.6 and hyd_change <= 4.8:
                    hydProb = 0.895238095238095
                    Hchange = "Medium"
                elif hyd_change > 4.8 and hyd_change <= 8.5:
                    hydProb = 0.951219512195122
                    Hchange = "High"
                else:
                    print("Hydrophobicity probability value not found")

                print("The hydrophobicity value goes from ", h_old," and ",h_new, ". Result = ", hyd_change)
                print("Probability associated to hydrophobicity change: ", hydProb)

                # Probabilidad asociada al cambio de tamaño de los aminoácidos
                from size import Size

                s_a1 = (Size.get(a1))
                s_a2 = (Size.get(a2))
                Size_change = s_a2 - s_a1
                print("The original aa's size: ",s_a1," and the new size is ", s_a2, ". Size change = ", Size_change)
                
                # Para EVITAR QUE CUANDO NO EXISTA CAMBIO DE AMINOÁCIDO DE UN RESULTADO DE PROBALIDAD
                if Size_change == 0 :
                    SizeProb = 0.861244019138756
                    SizeChange = "No"         
                elif Size_change >= -168 and Size_change <= -102:
                    SizeProb = 1
                    SizeChange = "High"
                elif Size_change > -102 and Size_change <= -35:
                    SizeProb = 0.96
                    SizeChange = "Medium"
                elif Size_change > -35 and Size_change <= 32:
                    SizeProb = 0.861244019138756
                    SizeChange = "Low"
                elif Size_change > 32 and Size_change <= 99:
                    SizeProb = 0.931818181818182
                    SizeChange = "Medium"
                elif Size_change > 99 and Size_change <= 168:
                    SizeProb = 0.933333333333333
                    SizeChange = "High"
                else:
                    print("Size probability value not found")

                print("The probabilitiy related to the size change: ", SizeProb)
                
            # CALCULO DE LA PROBABILIDAD TOTAL DE PATOGENICIDAD
                from Factors import factor

                a =  (factor.get("A"))
                b =  (factor.get("B"))
                c =  (factor.get("C"))
                d =  (factor.get("D"))
                x =  (factor.get("X"))
                y =  (factor.get("Y"))
                z =  (factor.get("Z"))

                refProb = a+b+c+d+x+y+z
                print("Addition of weight factors has being Substituted by a fixed value close to that is obtained for the most pathogenic known mutation =", refProb)

                Threshold = 0.666403377971394
                print ("Threshold = ", Threshold)

                # Para EVITAR QUE CUANDO NO EXISTA CAMBIO DE AMINOÁCIDO DE UN RESULTADO DE PROBALIDAD
                if a1 == a2:
                    ProbTotal = Threshold
                    print ("Final Result: NO MUTATION INSERTED ! ")
                else :
                    ProbTotal = Cons_Prob * a + cc * b + ori_prob * c + nue_prob * d + hydProb * x + SizeProb * y + d_prob * z
                    print ("Final Result: ",ProbTotal)

                if ProbTotal > Threshold :
                    clasification = "PATHOGENIC MUTATION ( "
                    print ( clasification )
                else :
                    clasification = "Non Pathogenic ( "
                    print ( clasification )
             
                PathoIndex = round(((ProbTotal-Threshold) / (0.74 - Threshold))*10,2)
                print("--> Patho_Index = ", PathoIndex)

                if ProbTotal > Threshold :
                    FinalResult = PathoIndex*5+50
                    print ( FinalResult )
                # Para EVITAR QUE CUANDO NO EXISTA CAMBIO DE AMINOÁCIDO DE UN RESULTADO DE PROBALIDAD
                elif a1 == a2 :
                    FinalResult = 100
                else :
                    FinalResult = 100-(PathoIndex*5+50)
                    print ( FinalResult )      
                print("\n")


                # insertamos una instancia de la clase query por cada consulta realizada a la lista de queries  
                querylist.append( queryClass(a1+str(position)+a2, str(round(FinalResult,1) )+" % ).", d_pos, PosCons, SizeChange, Hchange, Cchange) ) 
                
                archivo.write(" ")
                archivo.write("Analyzed mutation: ")
                archivo.write( a1 )
                archivo.write( str(position) )
                archivo.write( a2 )
                archivo.write(" ")
                archivo.write( clasification )
                archivo.write( str(round(FinalResult,1) ) )
                archivo.write(" % ).")
                archivo.write("\n")
                archivo.write(" - Affected domain: ")
                archivo.write( d_pos )
                archivo.write("\n")
                archivo.write(" - Position conservation: ")
                archivo.write( PosCons )
                archivo.write("\n")
                archivo.write(" - Size change: ")
                archivo.write( SizeChange )
                archivo.write("\n")
                archivo.write(" - Hydrophobicity change: ")
                archivo.write( Hchange )
                archivo.write("\n")
                archivo.write(" - Charge change: ")
                archivo.write( Cchange )
                archivo.write("\n")
                archivo.write("\n")
                archivo2.write( a1 )
                archivo2.write( str(position) )
                archivo2.write( a2 )
                archivo2.write(",")
                    

            archivo.close()
            archivo2.close()

            
            if ":" in StringInput :
                f = open ('static/DNAquery.txt','r')
                query = f.read()
                print("DNA input: ", query)
                f.close()
            else :
                f = open ('static/query.txt','r')
                query = f.read()
                print("AA input: ", query)
                f.close()

            # Contar lineas de un text file
            CountedLines = len(open('static/results.txt').readlines())
            print("Results.txt contains " + str(CountedLines) +" lines")



              
            headers = {"Cache-Control": "no-cache","Pragma": "no-cache"}
            
            # Para pasar todas las variables locales variable al html hay que escribir << **locals() >>
            return render_template ('output.html', **locals(), querylist=querylist )    
            
            #os.path.join(fileDir, 'Folder1.1/same.txt')



# SERVIDOR WEB
# Para que esté todo el tiempo activo y actualice cambios automáticamente
if __name__ == '__main__': # validación para asegurarse de que arrancamos desde el archivo principal y no desde un módulo
    app.run(port = 3000, debug = True) # para ejecutar la aplicación; el debug=True es el modo prueba para que los cambios se actualicen solos
