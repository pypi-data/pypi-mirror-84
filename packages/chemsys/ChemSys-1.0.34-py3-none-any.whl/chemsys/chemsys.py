# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 01:14:06 2020

Github: https://github.com/tjczec01

@author: Travis J Czechorski

E-mail: tjczec01@gmail.com

"""

import sympy as sp
from sympy import diff, Matrix, symbols, Add, Mul, Pow, Symbol, Integer, latex, exp, simplify
from sympy.matrices.dense import matrix2numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import display, Latex
from tkinter import Tk, ttk, IntVar, StringVar, N, W, E, S, Checkbutton, Label, Entry, Button
from tkinter.ttk import Combobox
import pickle
import os
import subprocess
from shutil import which
import warnings

__all__ = ["gui", "symbolgen", "kJtoJ", "create_pdf"]

warnings.filterwarnings("ignore")  # ,category=matplotlib.cbook.mplDeprecation
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.grid'] = False
plt.rcParams['text.latex.preamble'] = [r'\usepackage{mathtools}', r'\usepackage{bm}']


def create_pdf(file_in, file_out):
    cmds = str('"{}"'.format(which("pdflatex").replace("EXE", "exe") + ' -output-format=pdf ' + r"-output-directory={} ".format(file_out) + "-enable-pipes " + "-enable-mltex " + r"{}".format(file_in)))
    os.system(cmds)
    process = subprocess.Popen([which("pdflatex").replace("EXE", "exe"), '-output-format=pdf', r"-output-directory={}".format(file_out), "-enable-pipes", "-enable-mltex", r"{}".format(file_in)])
    process.wait()


def kJtoJ(EA_listkJ):
    EA_listJ = [i*1000.0 for i in EA_listkJ]  # kJ to J
    return EA_listJ


class gui:

    def __init__(self):
        self.chemnumsl = []
        self.rxnsvl = []
        self.chemnamesl = []
        self.reactants_num = []
        self.products_num = []
        self.reverse = []
        self.coeffsr = []
        self.coeffsp = []
        self.Initreactions = []
        self.Eqlist = []
        self.indvdf = []
        self.ffpath = []
        self.kk = []
        self.eaf = []
        self.RR = []

    def chemnumsll(self):
        return self.chemnumsl

    def rxnsvll(self):
        return self.rxnsvl

    def chemnamesll(self):
        return self.chemnamesl

    def reactants_numl(self):
        return self.reactants_num

    def products_numl(self):
        return self.products_num

    def reversel(self):
        return self.reverse

    def coeffsrl(self):
        return self.coeffsr

    def coeffspl(self):
        return self.coeffsp

    def Initreactionsl(self):
        return self.Initreactions

    def Eqlistl(self):
        return self.Eqlist

    def indvdfl(self):
        return self.indvdf

    def ffpathl(self):
        return self.ffpath

    def kkl(self):
        return self.kk

    def eafl(self):
        return self.eaf

    def RRl(self):
        return self.RR

    Initreactions4b = []
    Eqlist4b = []

    def pathf():
        cwd = os.getcwd()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            path_fol = r"{}\Jacobian".format(cwd)

        except Exception:
            path_fol = r"{}\Jacobian".format(dir_path)

        try:
            os.mkdir(path_fol)

        except Exception:
            pass

        return path_fol

    def close_window(self):
        global entry
        entry = int(self.chems.get())
        self.chemnumsl.append(entry)
        entry2 = int(self.rxns.get())
        self.rxnsvl.append(entry2)
        entry3 = str(self.indvard.get())
        self.indvdf.append(r'{}'.format(entry3))
        entry4 = str(r'{}'.format(self.filev.get()))
        self.ffpath.append(entry4)
        rval = float(self.rg.get())
        self.RR.append(rval)
        self.root.destroy()

    def close_window2(self):
        global entry
        for i in range(0, self.chemnumsl[0], 1):
            entry2 = str(self.entries[i].get())
            self.chemnamesl.append(entry2)
        self.root2.destroy()

    def close_window3(self):
        global entry
        for i in range(0, self.self.rxnsvl[0], 1):
            entry3a = int(self.entriesr[i].get())
            self.reactants_num.append(entry3a)
            entry3b = int(self.entriesp[i].get())
            self.products_num.append(entry3b)
            entry3c = int(self.intvars[i].get())
            entryk = float(self.entriesk[i].get())
            self.kk.append(entryk)
            entryea = float(self.entriesea[i].get())
            self.eaf.append(entryea)
            self.reverse.append(entry3c)
        self.root3.destroy()

    def close_window4(self):
        global entry
        num_chems = int(len(self.chemnamesl))
        for i in range(0, self.self.rxnsvl[0], 1):
            cfsr = [0*ij for ij in range(0, num_chems, 1)]
            cfsp = [0*ik for ik in range(0, num_chems, 1)]
            for j in range(0, self.reactants_num[i], 1):
                entry4r = self.entriesrc[i][j].get()
                indexr = self.chemnamesl.index(entry4r)
                cfsr[indexr] = int(self.entriesr4[i][j].get())
            self.coeffsr.append(cfsr[:])
            cfsr.clear()
            for k in range(0, self.products_num[i], 1):
                entry4p = self.entriespc[i][k].get()
                indexp = self.chemnamesl.index(entry4p)
                cfsp[indexp] = int(self.entriesp4[i][k].get())
            self.coeffsp.append(cfsp[:])
            cfsp.clear()
        self.root4.destroy()

    def first():

        chemnumsl1 = []
        rxnsvl1 = []
        RR1 = []
        indvdf1 = []
        ffpath1 = []
        path_fol = gui.pathf()

        def close_window1():
            global entry
            entry = int(chems.get())
            chemnumsl1.append(entry)
            entry2 = int(rxns1.get())
            rxnsvl1.append(entry2)
            entry3 = str(indvard1.get())
            indvdf1.append(r'{}'.format(entry3))
            entry4 = str(r'{}'.format(filev1.get()))
            ffpath1.append(entry4)
            rval1 = float(rg1.get())
            RR1.append(rval1)
            root1b.destroy()

        root1b = Tk()
        root1b.title("Number of chemical species")
        mainframe = ttk.Frame(root1b, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root1b.columnconfigure(0, weight=1)
        root1b.rowconfigure(0, weight=1)
        chemnums = StringVar()
        chems = Entry(mainframe, width=7, textvariable=chemnums)
        chems.grid(column=2, row=1, sticky=(W, N, E, S))
        Label(mainframe, text="Enter total number of chemical species ").grid(column=1, row=1, sticky=(W, N, E, S))
        rnums = StringVar()
        rxns1 = Entry(mainframe, width=7, textvariable=rnums)
        rxns1.grid(column=2, row=2, sticky=(W, N, E, S))
        Label(mainframe, text="Enter total number of chemical reactions ").grid(column=1, row=2, sticky=(W, N, E, S))
        indvard1 = StringVar()
        inv = Entry(mainframe, width=7, textvariable=indvard1)
        inv.grid(column=2, row=3, sticky=(W, N, E, S))
        Label(mainframe, text="Enter independent variable ").grid(column=1, row=3, sticky=(W, N, E, S))
        filep1 = StringVar(value=path_fol)
        filev1 = Entry(mainframe, width=50, textvariable=filep1)
        filev1.grid(column=2, row=4, sticky=(W, N, E, S))
        Label(mainframe, text="Enter file path ").grid(column=1, row=4, sticky=(W, N, E, S))
        rgas1 = StringVar(value="8.31446261815324")
        rg1 = Entry(mainframe, width=7, textvariable=rgas1)
        rg1.grid(column=2, row=5, sticky=(W, N, E, S))
        Label(mainframe, text="Enter Gas Constant ").grid(column=1, row=5, sticky=(W, N, E, S))
        Button(root1b, text="OK", command=close_window1).grid(column=3, row=1)
        root1b.mainloop()
        return chemnumsl1, rxnsvl1, indvdf1, RR1, ffpath1

    def second(chems_value):

        chemnamesl = []

        def close_window2b():
            global entry
            for i in range(0, chems_value, 1):
                entry2 = str(entries2B[i].get())
                chemnamesl.append(entry2)
            root2b.destroy()

        root2b = Tk()
        root2b.title("Name of chemical species")
        mainframe2b = ttk.Frame(root2b, padding="3 3 12 12")
        mainframe2b.grid(column=0, row=0, sticky=(N, W, E, S))
        root2b.columnconfigure(0, weight=1)
        root2b.rowconfigure(0, weight=1)
        stringvars2b = []
        entries2B = []
        for i in range(0, chems_value, 1):
            stringvars2b.append(StringVar())
        for i in range(0, chems_value, 1):
            entries2B.append(Entry(mainframe2b, width=20, textvariable=stringvars2b[i]))
            entries2B[i].grid(column=2, row=int(i + 1), sticky=(W, N, E, S))
            Label(mainframe2b, text="Enter name of chemical species {} ".format(i + 1)).grid(column=1, row=int(i + 1), sticky=(W, N, E, S))
        Button(root2b, text="OK", command=close_window2b).grid(column=3, row=1)
        root2b.mainloop()

        return chemnamesl

    def third(rxnnumr, rxnnum):

        reactants_num3b = []
        products_num3b = []
        kk3b = []
        eaf3b = []
        reverse3b = []

        def close_window3b():
            global entry
            for i in range(0, rxnnum, 1):
                entry3a = int(entriesr3b[i].get())
                reactants_num3b.append(entry3a)
                entry3b = int(entriesp3b[i].get())
                products_num3b.append(entry3b)
                entry3c = int(intvars3b[i].get())
                entryk = float(entriesk3b[i].get())
                kk3b.append(entryk)
                entryea = float(entriesea3b[i].get())
                eaf3b.append(entryea)
                reverse3b.append(entry3c)
            root3b.destroy()

        root3b = Tk()
        root3b.title("Reactants & Products")
        mainframe3b = ttk.Frame(root3b, padding="3 3 12 12")
        mainframe3b.grid(column=0, row=0, sticky=(N, W, E))
        root3b.columnconfigure(0, weight=1)
        root3b.rowconfigure(0, weight=1)
        root3b.rowconfigure(1, weight=1)
        stringvarsr3b = []
        stringvarsp3b = []
        stringvarsk3b = []
        stringvarsea3b = []
        intvars3b = []
        entriesr3b = []
        entriesp3b = []
        entriesc3b = []
        entriesk3b = []
        entriesea3b = []
        for i in rxnnumr:
            stringvarsr3b.append(StringVar())
            stringvarsp3b.append(StringVar())
            stringvarsk3b.append(StringVar())
            stringvarsea3b.append(StringVar())
            intvars3b.append(IntVar())
        for i in rxnnumr:
            mainframe3b.rowconfigure(i, weight=1)
            coli0 = 0
            coli1 = coli0 + 1
            coli2 = coli1 + 1
            coli3 = coli2 + 1
            coli4 = coli3 + 1
            coli5 = coli4 + 1
            coli6 = coli5 + 1
            coli7 = coli6 + 1
            coli8 = coli7 + 1
            coli9 = coli8 + 1
            coli10 = coli9 + 1
            clist = [i for i in range(coli10 + 1)]
            for ci in clist:
                mainframe3b.columnconfigure(ci, weight=1)
            Pad_x = 5
            Pad_y = 2
            CE = 2
            Box_1 = Entry(mainframe3b, width=7, textvariable=stringvarsr3b[i - 1])
            Box_1.grid(column=coli1, row=i, columnspan=CE, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            Label_0 = Label(mainframe3b, text="Reaction {} ".format(i), padx=Pad_x, pady=Pad_y)
            Label_0.grid(column=coli0, row=i, sticky=(W, N, E, S))
            Label_0.rowconfigure(int(i), weight=1)
            Label_0.columnconfigure(coli0, weight=1)
            entriesr3b.append(Box_1)
            entriesp3b.append(Entry(mainframe3b, width=7, textvariable=stringvarsp3b[i - 1]))
            entriesp3b[i - 1].grid(column=coli3, row=i, columnspan=CE, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            entriesk3b.append(Entry(mainframe3b, width=7, textvariable=stringvarsk3b[i - 1]))
            entriesk3b[i - 1].grid(column=coli6, row=i, columnspan=1, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            if len(str(i)) >= 2:
                Label(mainframe3b, text='k{}{}'.format(chr(0x2080 + int(str(i)[0])), chr(0x2080 + int(str(i)[-1])))).grid(column=coli5, row=i, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            elif len(str(i)) == 1:
                Label(mainframe3b, text='k{}'.format(chr(0x2080 + int(str(i)[0])))).grid(column=coli5, row=i, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            entriesea3b.append(Entry(mainframe3b, width=7, textvariable=stringvarsea3b[i - 1]))
            entriesea3b[i - 1].grid(column=coli8, row=i, columnspan=1, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            if len(str(i)) >= 2:
                Label(mainframe3b, text='Ea{}{} [kJ/mol]'.format(chr(0x2080 + int(str(i)[0])), chr(0x2080 + int(str(i)[-1])))).grid(column=coli7, row=i, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            elif len(str(i)) == 1:
                Label(mainframe3b, text='Ea{} [kJ/mol]'.format(chr(0x2080 + int(str(i)[0])))).grid(column=coli7, row=i, sticky=(W, N, E, S), padx=Pad_x, pady=Pad_y)
            entriesc3b.append(Checkbutton(mainframe3b, text="Reaction {} Reversable".format(i), variable=intvars3b[i - 1]).grid(column=coli9, row=i, columnspan=2, sticky=(W, N, E, S)))
        Button(root3b, text="OK", command=close_window3b).grid(column=coli9, row=1, padx=Pad_x, pady=Pad_y)
        root3b.mainloop()

        return reactants_num3b, products_num3b, kk3b, eaf3b, reverse3b

    def fourth(self, chemnamesl, rxnnum, reactants_num, products_num, reverse):
        coeffsp4b = []
        coeffsr4b = []

        def close_window4b():
            global entry
            num_chems = int(len(chemnamesl))
            for i in range(0, rxnnum, 1):
                cfsr = [0*ij for ij in range(0, num_chems, 1)]
                cfsp = [0*ik for ik in range(0, num_chems, 1)]
                for j in range(0, reactants_num[i], 1):
                    entry4r = entriesrc[i][j].get()
                    indexr = chemnamesl.index(entry4r)
                    cfsr[indexr] = int(entriesr4[i][j].get())
                coeffsr4b.append(cfsr[:])
                cfsr.clear()
                for k in range(0, products_num[i], 1):
                    entry4p = entriespc[i][k].get()
                    indexp = chemnamesl.index(entry4p)
                    cfsp[indexp] = int(entriesp4[i][k].get())
                coeffsp4b.append(cfsp[:])
                cfsp.clear()
            root4b.destroy()

        root4b = Tk()
        root4b.title("Reactions")
        mainframe4b = ttk.Frame(root4b, padding="3 3 12 12")
        mainframe4b.grid(column=0, row=0, sticky=(N, W, E, S))
        root4b.columnconfigure(0, weight=1)
        root4b.rowconfigure(0, weight=1)
        stringvarsr4 = []
        stringvarsp4 = []
        stringvarsrc = []
        stringvarspc = []
        entriesr4a = []
        entriesp4a = []
        entriesr4 = []
        entriesp4 = []
        entriesrca = []
        entriespca = []
        entriesrc = []
        entriespc = []
        rstrings = []

        for i in range(0, rxnnum, 1):
            rval = reverse[i]
            if rval == 0:
                rstrings.append(u"\u2192")
            elif rval == 1:
                rstrings.append(u"\u21CB")
        for i in range(0, rxnnum, 1):
            stringvarsr4.append([StringVar(value="1") for i in range(0, reactants_num[i], 1)])
            stringvarsp4.append([StringVar(value="1") for i in range(0, products_num[i], 1)])
            stringvarsrc.append([StringVar(value="1") for i in range(0, reactants_num[i], 1)])
            stringvarspc.append([StringVar(value="1") for i in range(0, products_num[i], 1)])

        for i in range(0, rxnnum, 1):
            mainframe4b.rowconfigure(i + 1, weight=1)
            int1 = 1
            int2 = 2
            jval = 1
            for j in range(0, reactants_num[i], 1):
                mainframe4b.columnconfigure(jval, weight=1)
                entriesr4a.append(Entry(mainframe4b, width=7, textvariable=stringvarsr4[i][j]))
                entriesr4a[-1].grid(column=jval, row=int(i + 1))
                jval += 1
                mainframe4b.columnconfigure(jval, weight=1)
                combbo = Combobox(mainframe4b, values=chemnamesl)
                combbo.grid(column=jval, row=int(i + 1))
                jval += 1
                mainframe4b.columnconfigure(jval, weight=1)
                entriesrca.append(combbo)
                if j < reactants_num[i]-1:
                    mainframe4b.columnconfigure(jval, weight=1)
                    Label(mainframe4b, text=" + ").grid(column=jval, row=int(i + 1))
                    jval += 1
                elif j == reactants_num[i]-1:
                    mainframe4b.columnconfigure(jval, weight=1)
                    Label(mainframe4b, text=" {} ".format(rstrings[i])).grid(column=jval, row=int(i + 1))
                    jval += 1
                int1 += 1
                int2 += 1
            entriesr4.append(entriesr4a[:])
            entriesr4a.clear()
            entriesrc.append(entriesrca[:])
            entriesrca.clear()
            for k in range(0, products_num[i], 1):
                mainframe4b.columnconfigure(jval, weight=1)
                entriesp4a.append(Entry(mainframe4b, width=7, textvariable=stringvarsp4[i][k]))
                entriesp4a[-1].grid(column=jval, row=int(i + 1))
                jval += 1
                mainframe4b.columnconfigure(jval, weight=1)
                combbb = Combobox(mainframe4b, values=chemnamesl)
                combbb.grid(column=jval, row=int(i + 1))
                jval += 1
                mainframe4b.columnconfigure(jval, weight=1)
                entriespca.append(combbb)
                if k < products_num[i]-1:
                    Label(mainframe4b, text=" + ").grid(column=jval, row=int(i + 1))
                    jval += 1
                    mainframe4b.columnconfigure(jval, weight=1)
                else:
                    mainframe4b.rowconfigure(int(rxnnum) + 2, weight=1)
                    Button(root4b, text="OK", command=close_window4b).grid(column=2, row=int(rxnnum+2))
            entriesp4.append(entriesp4a[:])
            entriesp4a.clear()
            entriespc.append(entriespca[:])
            entriespca.clear()
        root4b.mainloop()

        rxns_strs = ["Reaction {}".format(int(i + 1)) for i in range(0, rxnnum, 1)]

        for i in range(0, rxnnum, 1):
            indexnum = int(i + 1)
            keys = chemnamesl
            valuesr = coeffsr4b[i][:]
            valuesp = coeffsp4b[i][:]
            dictionary = {"Ea": indexnum, "K_Value": indexnum, "Reverse": reverse[i], "Reactants": dict(zip(keys, valuesr)), "Products": dict(zip(keys, valuesp))}
            self.Initreactions4b.append(dictionary)

        for i in range(0, len(chemnamesl), 1):
            indexnum = int(i + 1)
            namev = chemnamesl[i]
            name_index = chemnamesl[i].index(namev)
            keys = rxns_strs
            valuesfor = [0*ij for ij in range(0, rxnnum, 1)]
            valuesrev = [0*ik for ik in range(0, rxnnum, 1)]
            for j in range(0, rxnnum, 1):
                valuef = coeffsr4b[j][name_index]
                if valuef != 0 and coeffsp4b[j][name_index] == 0:
                    valuesfor[j] = int(-1)
                    valuesrev[j] = int(1*reverse[j])
                elif coeffsp4b[j][name_index] != 0:
                    valuesfor[j] = int(1)
                    valuesrev[j] = int(-1*reverse[j])
            dictionary2 = {"Name": "{}".format(str(namev)), "Reactions": dict(zip(keys, valuesfor)), "Reverse": dict(zip(keys, valuesrev))}
            self.Eqlist4b.append(dictionary2)

        return self.Initreactions4b, self.Eqlist4b

    def fullgui():
        chemnumsl, rxnsvl, indvdf, RR, ffpath = gui.first()
        chems_value = chemnumsl[0]
        rxnnum = int(rxnsvl[0])
        rxnnumr = [int(i + 1) for i in range(rxnnum)]
        chemnamesl = gui.second(chems_value)
        reactants_num, products_num, kk, eaf, reverse = gui.third(rxnnumr, rxnnum)
        Initreactions, Eqlist = gui.fourth(chemnamesl, rxnnum, reactants_num, products_num, reverse)
        return chemnamesl, rxnnum, Initreactions, Eqlist, indvdf[0], ffpath[0], kk, kJtoJ(eaf), RR[0]


class symbolgen:

    def __init__(self, nlist, Initlist, EQlist):
        self.nameslist = nlist
        self.rxnnum = len(self.nameslist)
        self.initlist = Initlist
        self.Eqlist = EQlist

    def initl(self):
        return self.initlist

    def latexin(self):
        latexs = self.eqlist(self.Eqlist, self.reactants, self.products)[1]
        return latexs

    def symsinit(self):
        return self.symfunc(self.nameslist, self.rxnnum)[0]

    def rinit(self):
        return self.initfunc(self.initreactions, self.C)[0]

    def pinit(self):
        return self.initfunc(self.initreactions, self.C)[1]

    initreactions = property(initl)
    C = property(symsinit, symsinit)
    reactants = property(rinit)
    products = property(pinit)
    latexs = property(latexin)

    def mfunci(funcsl, ylist, i, j):
        return diff(funcsl[i], ylist[j])

    def symfunc(names, rxnum):
        Csyms = [symbols(r'C_{}'.format('{}'.format(i))) for i in names]
        Ksyms = [symbols(r'K_{}'.format(j)) for j in range(rxnum)]
        EAsyms = [symbols(r'Ea_{}'.format(k)) for k in range(rxnum)]
        Tsyms = [symbols('T')]

        return Csyms, Ksyms, EAsyms, Tsyms

    def numfunc(Cs):
        cl = len(Cs)
        fcs = []
        for i in range(cl):
            As = []
            Ns = []
            NNs = []
            val3 = Cs[i]
            se = list(val3)
            count = 0
            sb = list(val3)
            SG = []
            fnum = len(se) - 1
            fend = len(se) - 1
            for sv in range(len(sb)):
                fend = len(se)
                vv = sb[sv]
                N = vv.isnumeric()
                A = vv.isalpha()
                ff = fend - sv
                if A is True and count == 0:
                    As.append(vv)
                    SG.append(vv)
                    count = 0
                    fnum -= 1
                if A is True and count > 0:

                    NNa = "".join(Ns)
                    SG.append(NNa)
                    SG.append(vv)
                    Ns.clear()
                    count = 0
                    fnum -= 1
                if A is True and count >= 2:

                    NNa = "".join(Ns)
                    NNs.append(NNa)
                    Ns.clear()
                    SG.append(NNa)
                    SG.append(vv)
                    count = 0
                    fnum -= 1

                if N is True and ff > 1:
                    Ns.append(vv)
                    count += 1
                if N is True and ff <= 1:
                    Ns.append(vv)

                    if len(Ns) >= 2:
                        NNa = "".join(Ns)
                        NNs.append(NNa)
                        SG.append(NNa)

                    else:
                        SG.append(vv)

            count = 0
            Ns.clear()
            As.clear()
            val2 = str(Cs[i])
            s = list(val2)
            for j in range(len(SG)):
                charv = SG[j]
                try:
                    charvi = int(SG[j])
                    SG[j] = charv.replace('{}'.format(charvi), ('_{' + '{}'.format(charvi) + '}'))
                except Exception:
                    pass
            ss = "".join(SG)
            s.clear()
            fcs.append(ss)
        return fcs

    def rterm(Ci, a):
        termi = Mul(a, Pow(Ci, abs(int(a))))
        return termi

    def rprod(Ci, a, Cj, b):
        term1 = symbolgen.rterm(Ci, a)
        term2 = symbolgen.rterm(Cj, b)
        term3 = Mul(term1, term2)
        return term3

    def initfunc(initlist, C):
        reactants = []
        products = []
        for i, j in enumerate(initlist):
            Reactants = initlist[i]['Reactants']
            Products = initlist[i]['Products']
            Rvals = list(Reactants.values())
            Pvals = list(Products.values())
            Ks = symbols('k_{}'.format(i + 1))
            Eas = symbols('Ea_{}'.format(i + 1))
            RT = Mul(Symbol('R'), Symbol('T'))
            RTI = Pow(RT, Integer(-1))
            EART = Mul(Eas, RTI)
            EARTI = Mul(EART, Integer(-1))
            ee = exp(EARTI)
            rterms = []
            pterms = []
            rtotal = Integer(1)
            ptotal = Integer(1)
            for k, li in zip(C, Rvals):
                if li != 0:
                    term = symbolgen.rterm(k, li)
                    rterms.append(term)
            for t in rterms:
                rtotal = Mul(rtotal, t)
            for m, n in zip(C, Pvals):
                if n != 0:
                    pterm = symbolgen.rterm(m, n)
                    pterms.append(pterm)
            for tt in pterms:
                ptotal = Mul(ptotal, tt)
            reactants.append(Mul(Ks, Mul(rtotal, ee)))
            products.append(Mul(Ks, Mul(ptotal, ee)))
        return [reactants, products]

    def eqlist(eqlistl, R, P):
        reactants = R
        products = P
        EQS = []
        leqns = []
        for i, j in enumerate(eqlistl):
            Reactions = eqlistl[i]['Reactions']
            Reverse = eqlistl[i]['Reverse']
            Rxn = list(Reactions.values())
            RxnR = list(Reverse.values())
            eqn = []
            Reacts = [i*j for i, j in zip(Rxn, reactants) if i != 0]
            Prods = [i*j for i, j in zip(RxnR, products) if i != 0]
            if not Prods:
                eee = sum(Reacts)
                rlatex = latex(eee)
                leqns.append(rlatex)
                EQS.append(eee)
            else:
                eqn = sum(Reacts)
                peqn = sum(Prods)
                eeqn = Add(eqn, peqn)
                rlatex = latex(eeqn)
                leqns.append(rlatex)
                EQS.append(eeqn)
        return [EQS, leqns]

    def dislat(lnames, latexs, indvar):
        Latexs = []
        Displays = []
        Dbs = []
        for i in range(len(latexs)):
            dd = '{d' + 'C_{}{}{}'.format("{", symbols(lnames[i]), "}") + '}'
            dt = '{d' + '{}'.format(symbols(indvar)) + '}'
            dde = r'$\dfrac{}{}'.format(dd, dt) + ' = ' + '{}$'.format(latexs[i])
            ddeb = r'\dfrac{}{}'.format(dd, dt) + ' = ' + '{}'.format(latexs[i])
            ddg = Latex(dde)
            Latexs.append(dde)
            Displays.append(ddg)
            Dbs.append(ddeb)
        return Displays, Latexs, Dbs

    def chemeq(Cs, rxn, inits):
        ceqs = []
        ceqsD = []
        ceqsw = []
        for i in range(rxn):
            Reactants = inits[i]['Reactants']
            Products = inits[i]['Products']
            Reverse = inits[i]['Reverse']
            Rvals = list(Reactants.values())
            rvals = [Rvals[kk] for kk in range(len(Rvals)) if Rvals[kk] != 0]
            Rname = symbolgen.numfunc(list(Reactants.keys()))
            rname = [symbols('{}'.format(Rname[h])) for h in range(len(Rname)) if Rvals[h] != 0]
            Pvals = list(Products.values())
            pvals = [Pvals[kk] for kk in range(len(Pvals)) if Pvals[kk] != 0]
            Pname = symbolgen.numfunc(list(Products.keys()))
            pname = [symbols('{}'.format(Pname[h])) for h in range(len(Pname)) if Pvals[h] != 0]
            CRvals = sum([Mul(Integer(ii), jj) for ii, jj in zip(rvals, rname) if ii != 0])
            CPvals = sum([Mul(Integer(ii), jj) for ii, jj in zip(pvals, pname) if ii != 0])
            if Reverse == 0:
                cheme = r'${} \longrightarrow {}$'.format(CRvals, CPvals)
            if Reverse == 1:
                cheme = r'${} \rightleftharpoons {}$'.format(CRvals, CPvals)
            ceqsD.append(Latex(cheme))
            ceqs.append(cheme)
            if Reverse == 0:
                chemw = r'{} \\longrightarrow {}'.format(CRvals, CPvals)
            if Reverse == 1:
                chemw = r'{} \\rightleftharpoons {}'.format(CRvals, CPvals)
            ceqsw.append(chemw)
        return ceqs, ceqsD, ceqsw

    def rhseqs(equations, kk, ea, r):
        EQLIST = []
        EQLISTF = []
        for ind, e in enumerate(equations):
            eqn = [r'{}'.format(e).replace('{', '').replace('}', '')]
            Ksyms = [symbols('k_{}'.format(i + 1)) for i in range(len(kk))]
            EAsyms = [symbols('Ea_{}'.format(i + 1)) for i in range(len(ea))]
            kdictionary = dict(zip(Ksyms, kk))
            eadictionary = dict(zip(EAsyms, ea))
            eqn3 = e.subs(kdictionary)
            eqn4 = eqn3.subs(eadictionary)
            eqn5 = eqn4.subs({'R': 8.31446261815324})
            eqn6b = eqn5.subs({'*exp': '*sp.exp'})
            EQLISTF.append(eqn6b)
            EQLIST.append(eqn[0])

        return EQLIST, EQLISTF

    def jacobian(rhs, y):
        eqnl = len(rhs)
        cl = len(y)

        def mfunc(i, j):
            return diff(rhs[i], y[j])
        J = [[i for i in range(cl)] for j in range(eqnl)]
        Jf = [[sp.diff(rhs[j], y[i]) for i in range(cl)] for j in range(eqnl)]
        Jn = [[i for i in range(cl)] for j in range(eqnl)]
        Jm = [[i for i in range(cl)] for j in range(eqnl)]
        ix, jx = symbols("ix jx")
        Ja = Matrix(len(rhs), len(y), lambda i, j: mfunc(i, j))
        for i in range(eqnl):
            for j in range(cl):
                J[i][j] = str('{}'.format('{}'.format(mfunc(i, j)).replace('*exp', '*sp.exp')))
        for i in range(eqnl):
            for j in range(cl):
                Jn[i][j] = str('{}'.format('{}'.format(mfunc(i, j)).replace('*exp', '*np.exp')))
                Jm[i][j] = str('{}'.format('{}'.format(mfunc(i, j)).replace('*exp', '*math.exp')))
        MatrixJ = simplify(Matrix(Ja))
        LatexMatrix = sp.latex(matrix2numpy(Matrix(Jf)))
        lm = latex(MatrixJ, mode='inline', itex=True, mat_delim="(", mat_str='array')
        return J, Jn, Jm, MatrixJ, lm, LatexMatrix

    def sysgen(self):
        equations, latexs = self.eqlist(self.Eqlist, self.reactants, self.products)
        return equations

    def sysdis(self):
        equations, latexs = self.eqlist(self.Eqlist, self.reactants, self.products)
        slatex, dlatex = self.dislat(self.nameslist, self.latexs, self.indvar)
        return dlatex

    def dis(self):
        slatex, dlatex = self.dislat(self.nameslist, self.latexs, self.indvar)
        for i in slatex:
            display(i)

    def gen(names, rxn, inits, eqs, intz):
        Cs, Ks, EAs, Ts = symbolgen.symfunc(names, rxn)
        reacts, prods = symbolgen.initfunc(inits, Cs)
        equats, latexss = symbolgen.eqlist(eqs, reacts, prods)
        slat, dlat = symbolgen.dislat(names, latexss, intz)
        Chem, ChemD, ChemW = symbolgen.chemeq(Cs, rxn, inits)
        return Cs, reacts, prods, equats, slat, dlat, Chem, ChemD, ChemW

    def fullgen(names, rxn, inits, eqs, intz, filepathf, kk, ea, r, namesl):
        Cs, Ks, EAs, Ts = symbolgen.symfunc(names, rxn)
        reacts, prods = symbolgen.initfunc(inits, Cs)
        equats, latexss = symbolgen.eqlist(eqs, reacts, prods)
        slat, dlat, dlatb = symbolgen.dislat(names, latexss, intz)
        Chem, ChemD, ChemW = symbolgen.chemeq(Cs, rxn, inits)
        Cs.append("T")
        RHS, RHSf = symbolgen.rhseqs(equats, kk, ea, r)
        Jac, JacNumpy, JacMath, JacSimple, lm, latexmatrix = symbolgen.jacobian(RHSf, Cs)
        JacS, JacNumpyS, JacMathS, JacSimpleS, lmS, latexmatrixS = symbolgen.jacobian(RHS, Cs)
        symbolgen.psave(namesl, dlat, filepathf, dlatb)
        symbolgen.csave(Chem, filepathf)
        KS = [str(r"{}".format(Ks[i])) for i in range(len(Ks))]
        EAS = [str(r"{}".format(EAs[i])) for i in range(len(EAs))]
        EAK = KS.copy()
        EAK.extend(EAS)
        symbolgen.fsave(filepathf, equats, dlat, Chem, ChemW, RHS, RHSf, Jac, JacNumpy, JacMath, JacSimple, lm, latexmatrix, JacS, JacNumpyS, JacMathS, JacSimpleS, lmS, latexmatrixS, Cs, EAK, names)
        return Cs, Ks, EAs, reacts, prods, equats, slat, dlat, Chem, ChemD, ChemW, RHS, RHSf, Jac, JacNumpy, JacMath, JacSimple, lm, latexmatrix, JacS, JacNumpyS, JacMathS, JacSimpleS, lmS, latexmatrixS

    def psave(nameslist, LATEXD, fpath, LATEXB):
        filename = fpath
        Fblist = [r"\begin{align*}"]
        for sa, ka in enumerate(LATEXD):
            fig1 = plt.figure(frameon=False)
            ax = fig1.add_axes([0, 0, 0.001, 0.001])
            left, width = .25, .5
            bottom, height = .25, .5
            right = left + width
            top = bottom + height
            ax.set_axis_off()
            ax.text(0.5 * (left + right), 0.5 * (bottom + top), ka, va='center', ha='center')
            fig1.savefig(r'{}\Overall Reaction {}.svg'.format(filename, nameslist[sa]), bbox_inches='tight')
            fig1.savefig(r'{}\Overall Reaction {}.pdf'.format(filename, nameslist[sa]), bbox_inches='tight')
            fig1.savefig(r'{}\Overall Reaction {}.png'.format(filename, nameslist[sa]), bbox_inches='tight')
            plt.close()

        for sb, kb in enumerate(LATEXB):
            Fblist.append(str(r'{}{}{}'.format(r"\mathbf{", kb, "}")))
            Fblist.append(r"\\")
            fig2 = plt.figure(frameon=False)
            fig2.text(0, 0, r'${}{}{}$'.format(r"\mathbf{", kb, "}"), fontsize=25)
            fig2.savefig(r'{}\Overall Reaction B {}.svg'.format(filename, nameslist[sb]), dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.0)
            fig2.savefig(r'{}\Overall Reaction B {}.pdf'.format(filename, nameslist[sb]), dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.0)
            fig2.savefig(r'{}\Overall Reaction B {}.png'.format(filename, nameslist[sb]), dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.0)
            plt.close()
        Fblist.append(r"\end{align*}")

        with open(r"{}\EquationsLatexp.txt".format(filename), "w") as output:
            for eqi in Fblist:
                output.write('"{}"{}'.format("{}".format(eqi), "\n"))
        with open(r"{}\EquationsLatexp.txt".format(filename)) as filein, open(r"{}\EquationsLatexFinal.txt".format(filename), 'w') as fileout:
            fileinl = filein.readlines()
            for line in fileinl:
                linef = line.replace('=', '&=')
                lineff = linef.replace('}}"', r'}} \\ "')
                linefff = lineff.replace('{dZ}', '{dZ}}')
                lineffff = linefff.replace('}}} \\', '}} \\')
                fileout.write(lineffff)
        strf = (open(r"{}\EquationsLatexFinal.txt".format(filename), 'r').read())

        def lf2space(s):
            return " ".join(s.split("\n"))

        eqf = str(lf2space(r"""{}""".format(strf))).replace('"', '')
        eqfb = eqf.replace(r"\mathbf{", r"$\mathbf{")
        eqfc = eqfb.replace(r"}} \\", "}}$ \n")
        eqfd = eqfc.replace("&=", "=")
        eqfe = eqfd.strip(r"\ \\")
        eqff = eqfe.strip(r"\end{align*}")
        eqfg = eqff.strip(r"\begin{align*}")
        eqfh = eqfg.replace(r"\\ $", "$")
        eqfj = eqfh.strip(r" \\")
        eqfk = eqfj.replace(r"  $\m", r"$\m")
        fig3 = plt.figure(frameon=False)
        plt.text(0, 0, eqf, {'color': 'black', 'fontsize': 22}, va="center", ha="left")
        plt.axis('off')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        fig3.savefig(r'{}\Total Reaction.png'.format(filename), format="png", dpi=300, transparent=True, bbox_inches='tight')
        # plt.show()
        plt.close()

        fig4 = plt.figure(frameon=False)
        plt.text(0, 0, eqf, {'color': 'black', 'fontsize': 16}, va="center", ha="left")
        plt.axis('off')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        fig4.savefig(r'{}\Total Reaction.pdf'.format(filename), format="pdf", dpi=300, transparent=True, bbox_inches='tight')
        # plt.show()
        plt.close()
        new_rc_params = {'text.usetex': False,
                         "font.size": 12,
                         "svg.fonttype": 'none'}

        mpl.rcParams.update(new_rc_params)

        fig5 = plt.figure(frameon=False)
        plt.axis('off')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
        ax = fig5.add_axes([0, 0, 0.001, 0.001])
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.set_axis_off()
        ax.text(0.5*(left+right), 0.5*(bottom+top), eqfk, va="center", ha="left")
        fig5.savefig(r'{}\Total Reaction.svg'.format(filename), bbox_inches='tight')
        # plt.show()
        plt.close()

    def csave(LATEXC, fpath):
        filename = fpath
        for s, k in enumerate(LATEXC):
            fig = plt.figure(frameon=False)
            ax = fig.add_axes([0, 0, 0.001, 0.001])
            left, width = .25, .5
            bottom, height = .25, .5
            right = left + width
            top = bottom + height
            ax.set_axis_off()
            ax.text(0.5*(left+right), 0.5*(bottom+top), r"$\bf{}Reaction \ {}{}: \ $".format("{", s + 1, "}") + k, va='center', ha='center')
            fig.savefig(r'{}\Labelled Reaction {}.svg'.format(filename, s + 1), bbox_inches='tight')
            fig.savefig(r'{}\Labelled Reaction {}.pdf'.format(filename, s + 1), bbox_inches='tight')
            fig.savefig(r'{}\Labelled Reaction {}.png'.format(filename, s + 1), bbox_inches='tight')
            plt.close()

        for s, k in enumerate(LATEXC):
            fig = plt.figure(frameon=False)
            ax = fig.add_axes([0, 0, 0.001, 0.001])
            left, width = .25, .5
            bottom, height = .25, .5
            right = left + width
            top = bottom + height
            ax.set_axis_off()
            ax.text(0.5*(left+right), 0.5*(bottom+top), k, va='center', ha='center')
            fig.savefig(r'{}\Reaction {}.svg'.format(filename, s + 1), bbox_inches='tight')
            fig.savefig(r'{}\Reaction {}.pdf'.format(filename, s + 1), bbox_inches='tight')
            fig.savefig(r'{}\Reaction {}.png'.format(filename, s + 1), bbox_inches='tight')
            plt.close()

    def fsave(ffpath, eqns, eqnslat, crxns, crxnsw, rhseq, rhseqf, Jac, JacN, JacMath, JacSimple, lm, latexmatrix, JacSy, JacSyN, JacMathSy, JacSimpleSy, lmSy, latexmatrixSy, C, EAK, nameslist):
        with open(r"{}\Equations.txt".format(ffpath), "w") as output:
            output.write("[")
            el = len(eqns)
            eel = 0
            for eqn in eqns:
                eel += 1
                if eel < el:
                    output.write('{},\n'.format(str(eqn)))
                if eel >= el:
                    output.write('{}]'.format(str(eqn)))

        with open(r"{}\EquationsLatex.txt".format(ffpath), "w") as output:
            for eqnlat in eqnslat:
                output.write('{}\n'.format(str(eqnlat)))

        with open(r"{}\Equations.tex".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "$")
            output.write(r"\documentclass{article}")
            output.write("\n")
            output.write(r"\usepackage{amsmath, nccmath, bm}")
            output.write("\n")
            output.write(r"\usepackage[bottom=0.2in,top=0.2in,left=0.2in,right=0.2in]{geometry}")
            output.write("\n")
            output.write(r"\begin{document}")
            output.write("\n")
            output.write(r"\begin{fleqn}")
            output.write("\n")
            for eqnlat in eqnslat:
                output.write(r"\begin{equation}")
                output.write("\n")
                output.write(r"\begin{split}")
                output.write("\n")
                output.write('{}\n'.format(str(eqnlat).translate(removetable)))
                output.write(r"\end{split}")
                output.write("\n")
                output.write(r"\end{equation}")
                output.write("\n")
                output.write(r"\\")
                output.write("\n")
            output.write(r"\end{fleqn}")
            output.write("\n")
            output.write(r"\end{document}")

        with open(r"{}\ReactionsLatex.txt".format(ffpath), "w") as output:
            for crxn in crxns:
                output.write('{}\n'.format(str(crxn)))

        with open(r"{}\ReactionsLatexWord.txt".format(ffpath), "w") as output:
            for crxnw in crxnsw:
                output.write('{}\n'.format(str(crxnw)))

        with open(r"{}\RHSsymbols.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def RHS(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            ll = len(rhseq)
            eqsss = []
            for rhs in rhseq:
                lr = rhseq.index(rhs)
                if lr < ll:
                    eqsss.append(str("EQ_{}".format(nameslist[rhseq.index(rhs)])))
                    output.write("    EQ_{} = {}\n".format(nameslist[rhseq.index(rhs)], rhs))
                elif lr >= ll:
                    eqsss.append(str("EQ_{}".format(nameslist[rhseq.index(rhs)])))
                    output.write("    EQ_{} = {}\n".format(nameslist[rhseq.index(rhs)], rhs))
            output.write("    return [{}]".format(("{}".format(eqsss)).translate(removetableB)))

        with open(r"{}\RHS.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def RHS(t, y):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            ll = len(rhseqf)
            lr = 0
            eqsss = []
            for rhsff in rhseqf:
                lr += 1
                if lr < ll:
                    eqsss.append(str("EQ_{}".format(nameslist[rhseqf.index(rhsff)])))
                    output.write("    EQ_{} = {}\n".format(nameslist[rhseqf.index(rhsff)], rhsff))
                elif lr >= ll:
                    eqsss.append(str("EQ_{}".format(nameslist[rhseqf.index(rhsff)])))
                    output.write("    EQ_{} = {}\n".format(nameslist[rhseqf.index(rhsff)], rhsff))
            output.write("    return [{}]".format(("{}".format(eqsss)).translate(removetableB)))

        with open(r"{}\Jacobian.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacMathSy)
            jjj = 0
            for i in range(len(JacMathSy)):
                jjj += 1
                Jrow = JacMathSy[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianSympy.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacSy)
            jjj = 0
            for i in range(len(JacSy)):
                jjj += 1
                Jrow = JacSy[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianNumpy.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacN)
            jjj = 0
            for i in range(len(JacN)):
                jjj += 1
                Jrow = JacN[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianMatrix.txt".format(ffpath), 'w') as output:
            output.write('{}'.format(JacSimple))

        with open(r"{}\JacobianLatex.txt".format(ffpath), "w") as output:
            output.write('{}'.format(lm))

        with open(r"{}\RHS.txt".format(ffpath)) as filein, open(r"{}\RightHandSide.txt".format(ffpath), 'w') as fileout:
            fileinl = filein.readlines()
            lfia = len(fileinl)
            lffb = 0
            for line in fileinl:
                lffb += 1
                line = line.replace("'", "")
                line = line.replace("exp", "sp.exp")
                if lffb < lfia:
                    fileout.write('{}'.format(line))
                elif lffb >= lfia:
                    fileout.write('{}'.format(line))

        with open(r"{}\RHSsymbols.txt".format(ffpath)) as filein, open(r"{}\RightHandSideSymbols.txt".format(ffpath), 'w') as fileout:
            fileinl = filein.readlines()
            lfi = len(fileinl)
            lff = 0
            for line in fileinl:
                line = line.replace("'", "")
                line = line.replace("exp", "math.exp")
                lff += 1
                if lff < lfi:
                    fileout.write('{}'.format(line))
                elif lff >= lfi:
                    fileout.write('{}'.format(line))

        pickle.dumps(JacSimple)
        with open(r'{}\JacobianMatrixPickle.txt'.format(ffpath), 'wb') as f:
            pickle.dump(JacSimple, f)

        with open(r"{}\JacobianSymbolic.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacMathSy)
            jjj = 0
            for i in range(len(JacMathSy)):
                jjj += 1
                Jrow = JacMathSy[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianSymbolicSympy.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacSy)
            jjj = 0
            for i in range(len(JacSy)):
                jjj += 1
                Jrow = JacSy[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianSymbolicNumpy.txt".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "[]'")
            removetableB = str.maketrans('', '', "[]'")
            output.write("def Jacob(t, y, *args):\n")
            output.write("    {} = args\n".format(str("{}".format(EAK)).translate(removetable)))
            output.write("    {} = y\n".format(str("{}".format(C)).translate(removetable)))
            output.write("    Jac = [")
            jj = len(JacSy)
            jjj = 0
            for i in range(len(JacSyN)):
                jjj += 1
                Jrow = JacSyN[i][:]
                if i == 0:
                    output.write(('{},\n'.format(Jrow)).replace("'", ""))
                if jjj < jj and i != 0:
                    output.write(('           {},\n'.format(Jrow)).replace("'", ""))
                elif jjj >= jj:
                    output.write(('           {}'.format(Jrow)).replace("'", ""))
            output.write("]\n")
            output.write("    return Jac")

        with open(r"{}\JacobianMatrixSymbolic.txt".format(ffpath), 'w') as output:
            output.write('{}'.format(JacSimpleSy))

        with open(r"{}\JacobianLatexSymbolic.txt".format(ffpath), "w") as output:
            output.write('{}'.format(lmSy))

        with open(r"{}\JacobianLatexSymbolic.txt".format(ffpath)) as filein, open(r"{}\Jacobian.tex".format(ffpath), "w") as output:
            removetable = str.maketrans('', '', "$")
            output.write(r"\documentclass{standalone}")
            output.write("\n")
            output.write(r"\usepackage{amsmath, nccmath, bm}")
            output.write("\n")
            output.write(r"\begin{document}")
            output.write("\n")
            fileinl = filein.readlines()
            for line in fileinl:
                lineb = line.replace("&", ", &")
                linec = lineb.replace(r"\\", r" \\" + " \n")
                output.write(linec)
            output.write("\n")
            output.write(r"\end{document}")

        pickle.dumps(JacSimpleSy)
        with open(r'{}\JacobianMatrixPickleSymbolic.txt'.format(ffpath), 'wb') as f:
            pickle.dump(JacSimpleSy, f)

        try:
            create_pdf(r"{}\Equations.tex".format(ffpath), "{}".format(ffpath))
            os.remove(r"{}\Equations.aux".format(ffpath))
            os.remove(r"{}\Equations.log".format(ffpath))
        except Exception:
            print("Coulnd't convert Equations.tex")
            pass

        try:
            create_pdf(r"{}\Jacobian.tex".format(ffpath), "{}".format(ffpath))
            os.remove(r"{}\Jacobian.aux".format(ffpath))
            os.remove(r"{}\Jacobian.log".format(ffpath))
        except Exception:
            print("Coulnd't convert Jacobian.tex")
            pass

# Generates all necessary lists and values.


# chemical_names, number_of_reactions, Initial_reactions, Equation_list, indvdf, filepath, kvalues, ea_values, r_gas = gui.fullgui()  # Generates all necessary lists and values.

# Calculates the jacobian and all other desired functions

# for key, value in locals().items():
#     if callable(value) and value.__module__ == __name__:
#         l.append(key)
# C_Symbols, KKS, EAS, reacts, prods, equations, slat, dlat, chem, chemD, chemw, rhs, rhsf, jac, jacnumpy, Jacmath, JacSimple, lm, latexmatrix, jacsy, jacnumpysy, jacmathsy, jacsimplesy, lmsy, latexmatrixsy = symbolgen.fullgen(chemical_names, number_of_reactions, Initial_reactions, Equation_list, indvdf, filepath, kvalues, ea_values, r_gas, chemical_names)
