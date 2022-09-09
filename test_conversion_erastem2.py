
# version 1.0
#from qt import *

avogadro = 6.02214e23

def convertitTemps(T ,ancien ,nouveau):
    Temp =float(T)
    if(ancien=="s"):
        Temp =Temp
    elif(ancien=="m"):
        Temp =Temp * 60.0
    elif(ancien=="mn"):
        Temp =Temp * 60.0
    elif(ancien=="h"):
        Temp =Temp *60.0 * 60.0
    elif(ancien=="j"):
        Temp =Temp * 60.0 * 60.0 * 24.0
    elif(ancien=="an"):
        Temp =Temp *60.0 * 60.0 * 24.0 *365.0

    if(nouveau=="s"):
        Temp =Temp
    elif(nouveau=="m"):
        Temp =Temp /(60.0)
    elif(nouveau=="mn"):
        Temp =Temp /(60.0)
    elif(nouveau=="h"):
        Temp =Temp /(60.0 * 60.0)
    elif(nouveau=="j"):
        Temp =Temp /(60.0 * 60.0 * 24.0)
    elif(nouveau=="an"):
        Temp =Temp /(60.0 * 60.0 * 24.0 * 365.0)

    return Temp

def enSecondes(T):
    from string import find
    if T.find("s" ) >0:
        return float(T[0:len(T ) -1])
    elif T.find("mn" ) >0:
        return float(T[0:len(T ) -2] ) *60.0
    elif T.find("m" ) >0:
        # print "attention unite desuete"
        return float(T[0:len(T ) -1] ) *60.0
    elif T.find("h" ) >0:
        return float(T[0:len(T ) -1] ) *(60.0 * 60.0)
    elif T.find("j" ) >0:
        return float(T[0:len(T ) -1] ) *(60.0 * 60.0 * 24.0)
    elif T.find("an" ) >0:
        return float(T[0:len(T ) -2] ) *(60.0 * 60.0 * 24.0 * 365.0)

def coeffconversionUnite(ancien ,nouveau):
    err = False  # mise a jour pour accepter les 1->Ci/Bq
    ancien = decomposeUnites(ancien)
    nouveau = decomposeUnites(nouveau)
    # if len(ancien)!=len(nouveau):
    # print ancien,nouveau
    # err=True
    print("1 OK")
    if True:  # else:
        i=0
        while(i<len(ancien)):
            print("2 OK")
            unite=ancien[i]
            if nouveau.count(unite)>0:
                ancien.pop(i)
                nouveau.remove(unite)
            else:
                i=i+1
        coeff=transformeEnSI(ancien)
        coeff=coeff/transformeEnSI(nouveau)
        reduitUnitesVect(nouveau)
        reduitUnitesVect(ancien)
        while ["1",1] in nouveau:
            nouveau.remove(["1",1])
        i=0
        while(i<len(ancien)):
            unite=ancien[ i ]
            if nouveau.count(unite)>0:
                ancien.pop(i)
                nouveau.remove(unite)
            else:
                i=i+1
        if len(nouveau)>0 or len(ancien)>0:
            print("dans if")
            # print "unites inconsistantes", nouveau, ancien
            err=True
    print("3 OK, err = ", err)
    if(err):
        return -1
    else:
        print("4 OK")
        return coeff

def coeffBaseSI(dimension):
    #    print "unite de base ",dimension
    dimension=decomposeUnites(dimension)
    coeff=transformeEnSI(dimension)
    return coeff

def coeffEtBaseSI(dimension):
    unites=decomposeUnites(dimension)
    coeff=transformeEnSI(unites)
    for unite in unites:
        unite[0]=uniteSI(unite[0])[1]
    return coeff,reduitUnites(chaineUnites(unites))

def reduitUnitesVect(dimension):
    i=0
    while(i<len(dimension)):
        unite=dimension[i]
        if dimension.count([unite[0],-1*unite [1 ] ])>0:
            dimension.remove([unite[0],-1*unite [1 ] ])
            dimension.pop(i)
        else:
            i+=1

def  reduitUnites(dimension):
    dimension=decomposeUnites(dimension)
    i=0
    while(i<len(dimension)):
        unite=dimension[i]
        if dimension.count([unite[0],-1*unite [1 ] ])>0:
            dimension.remove([unite[0],-1*unite [1 ] ])
            dimension.pop(i)
        else:
            i+=1
    dimension = chaineUnites(dimension)
    return dimension

def chaineUnites(unites):
    if len(unites)==0: return "1"
    if unites[0][1]==-1:
        dimensin= "1/"+unites[0][0]
    else:
        dimension=unites[0][0]
    if len(unites)==1:
        return dimension
    for unite in unites[1:]:
        if unite[1]==1:
            op="*"
        else:
            op="/"
        dimension=dimension+op+unite[0]
    return dimension


def decomposeUnites(unites):
    nouvelleUnite=[]
    #from string import split
    mul=1
    while(len(unites)>0):
        # unitemul=split(unites,"*",1)
        unitemul = unites.split("*", 1)
        # unitediv=split(unites,"/",1 )
        unitediv = unites.split("/", 1 )

        if len(unitemul)==1 and len (unitediv)==1:
            if unitemul[0]!="1":
                nouvelleUnite.append( [unitemul[0],mul])
            unites=[]
        else:
            if len(unitemul[0])<len(unitediv[0]):
                unite=unitemul
                newmul=1
            else:
                unite = unitediv
                newmul=-1
            if unite[0]!="1":
                nouvelleUnite.append( [unite[0],mul])
            mul=newmul
            unites=unite[1]
    #      if nouvelleUnite.count( [ "__m3__",1])>0:
    #        nouvelleUnite.remove(["__m3__",1])
    return nouvelleUnite

def transformeEnSI(unites):
    coeff=1
    for unite in unites:
        SI=uniteSI(unite[0])
        if unite[1]==1:
            coeff=coeff*SI[0]
        elif unite[1]==-1:
            coeff=coeff/SI[0] ##        else:
        ##                coeff=-1
        unite[0]=SI[1]
    return coeff

def uniteSI(unite):
    if(unite == "m"):
        coeff=60.0
        unite="s"
    elif(unite=="mn"):
        coeff=60.0
        unite="s"
    elif(unite == "h"):
        coeff=3600.0
        unite="s "
    elif(unite == "j"):
        coeff=3600.0*24
        unite= "s"
    elif(unite == "an"):
        coeff = 3600 * 24 * 365.24220
        unite="s"
    elif(unite=="Ci"):
        coeff = 3.7e10
        unite="Bq"
    elif(unite == "mol"):
        coeff= 6.02214e23
        unite="At"
    elif(unite == "g"):
        coeff =0.001
        unite="kg "
    elif(unite == "%") :
        coeff=0.01
        unite="1"
    elif(unite =="__m3__"):
        coeff= 1
        unite="1"
    else:
        coeff=1
    return coeff,unite

def familleLoop(base , unites,vect):
    familles= [ ['Bq','Ci'],['s','m ','mn','h','j','an'],['kg' ,'g'],[ 'At','mol']]
    if len(unites)==0 :return
    if len (unites)== 1:
        test=False
        for famille in familles:
            if unites[0][0] in famille:
                for newunit in famille:
                    vect.append(chaineUnites(base+[[newunit,unites[0][1]]]))
                test=True
        if not test:
            vect.append(chaineUnites(base+unites))
        return

    test=False
    for famille in familles:
        if unites[0][0] in famille:
            for newunit in famille:
                familleLoop(base+[[newunit,unites[0][1]]],unites[1:],vect)
            test=True
    if not test:
        familleLoop(base+[ unites[0]],unites[1:],vect )



def familleUnites (uniteIn):
    unites=decomposeUnites(uniteIn)
    uniteVect =[]
    familleLoop([],unites,uniteVect)
    return uniteVect

def majListe(liste,base):
    listeMods=[]
    for i in range(liste.count()):
        unite=liste.text(i).ascii()
        if unite[0:2] in ['Bq','kg','At']:
            listeMods.append(unite[2:])
    uniteBase=[]# creation de la liste des un ites  de base selon le cas
    if(base=="At"):
        uniteBase.append("At")
        uniteBase.append("mol")
    elif(base=="kg") :
        uniteBase.append("kg")
        uniteBase.append("g")
    elif(base=="Bq"):
        uniteBase.append("Bq")
        uniteBase.append("Ci")
    nvlListe=QStringList()
    for grandeur in uniteBase:
        for modif in listeMods:
            nvlListe.append(reduitUnites(grandeur+modif))
    return nvlListe


def declineUnites(base,unites):
    out=[]
    for unite1 in base:
        for unite2 in unites:
            out.append( unite1+unite2)
    return out

def listeMatiereSI(pylistmat):
    mode = pylistmat[0][0]
    unite = pylistmat[0][1]
    if mode== "resultat":
        from string import split
        unitG,unitI=split(unite,"|")
        unitG= coeffEtBaseSI(unitG)
        unitI=coeffEtBaseSI(unitI)
        for nucl in pylistmat[ 1:]:
            nucl[2]=float(nucl[2])*unitG[0]
            nucl[3]=float(nucl[3])*unitI[0]
        pylistmat[0][1]=unitG[1]+"|" + unitI[1]
    else:
        1

def divUnitEvol(numerateur,denominateur):
    if numerateur.find("|")>-1:
        if denominateur.find("|")>-1:
            num=numerateur.split("|")
            den=denominateur.split("|")
            return divUnit(num[0],den[0])+"|"+divUnit(num[1],den[1])
        else:
            num=numerateur.split("|")
            return divUnit(num[0],denominateur)+ "|" + divUnit(num[1],denominateur)
    else :
        if denominateur.find("|")>-1:
            den= denominateur.split("|")
            return divUnit(numerateur,den[0])+"|"+divUnit(numerateur,den[1])
        else:
            return divUnit(numerateur,denominateur)

def divUnit(numerateur,denominateur) :
    unitN=decomposeUnites(numerateur)
    unitD=decomposeUnites(denominateur)
    for unit in unitD:
        unit[1]=-unit[1]
    unit=chaineUnites(unitN+unitD)
    return reduitUnites(unit)

if __name__=="__main__":
    print(divUnitEvol("At|s", "s|s"))
    print(coeffEtBaseSI("s.mol/s.kg.s"))


    print(coeffEtBaseSI("At.s/h"))
    a="1/s" #.mol"
    n="1/h" #.At"
    print(len(familleUnites("kg.mSv/Bq.m/At")))
    print(familleUnites('At'))
    print(a, "->", n, ":")
    print(coeffconversionUnite(a,n))
    a="s.At/s.kg.s"
    print(a,"->",reduitUnites(a))

