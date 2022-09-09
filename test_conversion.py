
# version 1.0
from qt import *
avogadr o =6.02214e23
def convertitTemps(T ,ancien ,nouveau):
    Tem p =float(T)
    i f(ancie n= ="s"):
        Tem p =Temp
    eli f(ancie n= ="m"):
        Tem p =Tem p *60.0
    eli f(ancie n= ="mn"):
        Tem p =Tem p *60.0
    eli f(ancie n= ="h"):
        Tem p =Tem p *60. 0 *60.0
    eli f(ancie n= ="j"):
        Tem p =Tem p *60. 0 *60. 0 *24.0
    eli f(ancie n= ="an"):
        Tem p =Tem p *60. 0 *60. 0 *24. 0 *365.0

    i f(nouvea u= ="s"):
        Tem p =Temp
    eli f(nouvea u= ="m"):
        Tem p =Tem p /(60.0)
    eli f(nouvea u= ="mn"):
        Tem p =Tem p /(60.0)
    eli f(nouvea u= ="h"):
        Tem p =Tem p /(60. 0 *60.0)
    eli f(nouvea u= ="j"):
        Tem p =Tem p /(60. 0 *60. 0 *24.0)
    eli f(nouvea u= ="an"):
        Tem p =Tem p /(60. 0 *60. 0 *24. 0 *365.0)

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
        return float(T[0:len(T ) -1] ) *(60. 0 *60.0)
    elif T.find("j" ) >0:
        return float(T[0:len(T ) -1] ) *(60. 0 *60. 0 *24.0)
    elif T.find("an" ) >0:
        return float(T[0:len(T ) -2] ) *(60. 0 *60. 0 *24. 0 *365.0)

def coeffconversionUnite(ancien ,nouveau):
    er r =False  # mise a jour pour accepter les 1->Ci/Bq
    ancie n =decomposeUnites(ancien)
    nouvea u =decomposeUnites(nouveau)
    # if len(ancien)!=len(nouveau):
    # print ancien,nouveau
    # err=True
    if True:  # else: i=0
        while(i<len(a nc i en)):
            unite=ancien[ i ]
            if nouveau.count(unite)>0:
                ancien.pop(i)
                nouveau.remove(unite)
            else:
                i=i+1
        coeff=transfo r meEnSI(ancien)
        coeff=coeff/t r ansfo r meEnSI(nouveau)
        reduitUnitesVect(nouveau)
        reduitUnitesVect(ancien)
        while ["1",1] in no uveau:
            nouveau.remove(["1",1])
        i=0
        while(i<len(a nc i en)):
            unite=ancien[ i ]
            if nouveau.count(unite)>0:
                ancien.pop(i)
                nouveau.remove(unite)
            else:
                i=i+1
        if len(nouveau)>0 or le n (ancien)>0:
            # print "unites inconsistantes", nouveau, ancien
            err=True

    if(err):
        return -1
    else:
        return coeff

def co \


fBaseSI(dimension):
    #    print "unite de base ",dimension
    dimension=decompo s eUnites(dimension)
    coeff=transfo r meEnSI(dimension)
    return coeff

def co \


fEtBaseSI(dimension):
    unites=decompo s eUnites(dimension)
    coeff=transfo r meEnSI(unites)
    for unite in unites:
        unite[0]=uniteSI ( unite[0])[1]
    return coeff,reduitUn ites(chaineUnites(unites))

def re \


itUnitesVect(dimension):
    i=0
    w h ile(i<len(d im e nsion)):
        unite=dimensi o n[i]
        if dimension.count([unite[0],-1*unite [1 ] ])>0:
            dimension.remove([unite[0],-1*unite [1 ] ])
            dimension.pop(i)
        else:
            i+=1

def r e \


itUnites(dimension):
    dimension=decompo s eUnites(dimension)
    i=0
    w h ile(i<len(d im e nsion)):
        unite=dimensi o n[i]
        if dimension.count([unite[0],-1*unite [1 ] ])>0:
            dimension.remove([unite[0],-1*unite [1 ] ])
            dimension.pop(i)
        else:
            i+=1 dimensi on=chaineUnites ( dimension)
    return dimension

def chaineU \


tes(unites):
    if len(unites)==0: return "1"
    if unites[0][1]==-1:
        dimensio n= "1/"+unites[0][0] else:
        dimension=unites[0][0]
    if len(un i tes)==1:
        return dimensi on
    for unite in unites[1:]:
        if unite[1]==1:
            op="*"
        else:
            op="/"
        dimension=dime n sion+op+unite[0] return dimensio n def decomposeUnites(unites):


nouvelleUnite=[]
    from string import split mul=1
    while(len(unites)>0):
        unite m ul=split(un ites,"*",1)
        unitediv=spli t (unites,"/",1 )
        if len(unitem u l)==1 and len (uni tediv)==1:
            if u ni temul[0]!="1":
                nouvelleUnite.appen d( [unitemul[0],mul])
            unites=[]
        else:
            if len(unite m ul[0])<len(unitediv[0]):
                unite=u n itemul
                newmul=1
            else:
                unite = unitediv
                newmul=-1
            if unite[0]!="1":
                nouvelleUnite.appen d( [unite[0],mul])
            mul=newmul
            u nites=unite[1]
    #      if nouvelleUnite.count( [ "__m3__",1])>0:
    #        nouvelleUnite.remove(["__m3__",1])
    return nouvelleUnite

def transformeEnSI(unites):
    coeff=1
    for unite in unites:
        SI=uni t eSI(unite[0])
        if unite[1]==1:
            coeff=coeff*SI[0]
        e lif unite[1]==-1:
            coeff=coeff/SI[0] ##        else:
        ##                coeff=-1
        unite[0]=SI[1]
    return coeff

def uniteSI(unite):
    if ( unite=="m"):
        c


ff=60.0
        unite="s"
    el if (unite=="mn"):
        coeff=60.0
        unite="s"
    e li f(unite=="h"):
        coeff=3600.0
        unite="s " elif(un ite=="j"): coeff=3600 .0*24
        unite= " s"
    elif( unite= =" an"):
        coeff = 3600*2 4 *365.24220
        unite="s"
    el if (unite=="Ci"):
        co e ff = 3.7e10
        unite="B q "
    elif(u nite== "m ol"):
        coeff= 6 .02214e23
        un i te="At"
    e lif(un it e=="g"):
        coef f =0.001
        unite="kg "
    elif(uni te=="% ") :
        coeff=0.0 1
        unite="1"
    elif(unite =="__m 3_ _"):
        coeff= 1
        unite="1"
    else: coeff=1
    return coeff,unite

def familleLoop(base , unites,vect):
    familles= [ ['Bq','Ci'],['s','m ','mn',


'h','j','an'],['kg' ,'g'],[ 'At','mol']]
    if len(unit es)==0 :retu rn
    if len (uni tes)== 1: test=False
        for famille in famille s:
            if unites[0][0 ] in famille:
                for newunit in famille:
                    vect.append(chaineUnites(base+[[newunit,unites[0][1]]]))
                test=True
        if not test:
            vect.app end(chaineUnites(base+unites))
        return

    test=False
    for famille in familles:
        if uni t es[0][0] in famille: for newunit in famille:
                familleLoop(base+[[newunit,unites[0][1]]],unites[1:],vect)
            test=True
    if not test:
        famille L oop(base+[ unites[0]],unit es[1:],vect )



def familleUnites ( uniteIn):
    unites=decomposeUnites(uniteIn)
    uniteVect =[]
    fam illeLoop(


[],unites,uniteVect)
    return un i teVect

def majListe(liste,base): listeM ods=[]
    for i in ra nge(lis te.count()):
        unite=liste. \


text(i).ascii()
        if unite[0:2] in ['Bq','kg','At']:
            listeMods.append(un i te[2:])
    uniteBase=[]# creation de la liste des un ites  de base selon le cas
    if(base=="At"):
        uniteBase.a p pe  nd("At")
        uniteBase.append("mol")
    elif(base=="kg") :
        uniteBase.append("kg")
        uniteBase.append("g")
    elif(base=="Bq"):
        uniteBase.append("Bq")
        uniteBase.append("Ci")
    nvlListe=QStringL ist()
    for grandeur in uniteBase:
        for modif in listeMods:
            nvlList e .append(reduitUnites(grandeur+modif))
    return nvlListe


def declineUnites(base,unites):
    out=[]
    for unite1 in base:
        for unite2 in unites:
            out.append( unite1+unite2)
    return out

def listeMatiereSI(pylistmat):
    mode=pylistmat[0][0]
    unite=pylist m at[0][1]
    if mode== \


"resultat":
        from string import sp lit
        unitG,unitI=s p lit(unite,"|")
        unit G= coeffEtBaseSI(unitG)
        unitI=coeffEtBaseSI(unitI) for nucl i n pylistmat[ 1:]:
            n u cl[2]=float(nucl[2])*unitG[0]
            nucl[3]=float(nucl[3])*unitI[0]
        pylistmat[0][1]=unitG[1]+"|" + unitI[1] else:
        1

def divUnitEvol(nu m erateur,denomi n ateur):
    if numerateur.find(" | ")>-1:
        if denominateur.find("|")>-1:
            num=numerateur .split("|")
            den=denominateur.s p lit("|")
            return divUnit(n u m[0],den[0])+"|"+di v Unit(num[1],den[1])
        else:
            num=numerateur.split("|")
            return divUn it(num[ 0 ],d e nominateur)+"|" +divUnit(num[1],denominateur)
    els e :
        if denominateur.find("|")>-1:
            den= denominateur. s pli t ("|")
            return divUnit(numerateur,den[0])+"|"+divUnit(numerate u r,den[1])
        e l se:
            return divUnit(numerateur,denominateur)

def d ivUnit( n ume r ateur,denominateur) :
    unitN=decomposeUnites(numerateur)
    unitD=decomposeU nites(denomin


eur)
    for unit in un itD:
        unit[1]=-un i t[1]
    unit=chaineUnites(unitN+unit D )
    return reduitUnites(unit)

# if __name__=="__main__":
#    pr i nt divUnitEvol("A t |s","s|s")
#    p r int coeffEtBaseSI("s.mol/s.kg.s")
#

print coeffEtBaseSI("At.s/h")
# a="1/s"#.mol"
# n="1/h"#.At"
# print len(familleUnites("kg.mSv/Bq.m/At"))
# print familleUnites('At')
# print a,"->",n,":",coeffconversionUnite(a,n)
# a="s.At/s.kg.s"
# print a,"->",reduitUnites(a)

