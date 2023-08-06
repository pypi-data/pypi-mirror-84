# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:40:27 2019

@author: jittima
"""

import numpy as np
from colorama import Fore,Style,Back
from time import sleep
from pyzik.pandly import del_columns,derive, norme, delta, f_input
import pandas as pd
pd.DataFrame.del_columns = del_columns
pd.DataFrame.derive = derive
pd.DataFrame.norme = norme
pd.DataFrame.delta = delta
import traceback


class TestFunctions():
    from pyzik.pandly import give_me_crypto as __give_me_crypto,get_SPY as __get_SPY,SPY_KEY as __SPY_KEY
    __EXTRA_DELIMITER = '|'
    
    def __init__(self):
        print("Test functions init....")
        (_,_,_,text)=traceback.extract_stack()[-2]
        def_name = text[:text.find('=')].strip()
        self.__def_name = def_name
        self.__soluce = None
    
    def add_extra(self,url,delimiter='\t',url_type="gd"):
        url0 = "https://drive.google.com/uc?export=download&id="+url if url_type == "gd" else url
        self.__soluce = pd.read_csv(url0,delimiter=delimiter)
        self.__qcol = self.__soluce.columns[0]
        self.__scol = self.__soluce.columns[1]
    
    def get_soluce(self,question,output,**d):
        extdel = d.get('delimiter',None)
        if extdel != None:
            TestFunctions.__EXTRA_DELIMITER = extdel[0] 
        ask = f"Le niveau d'aide demandé est : <{output}>\nVoulez vous vraiment obtenir de l'aide ?"
        r = f_input(ask,output='str',choice=['o','n'])
        if r == 'n':
            return None
        try:
            txt = self.__soluce.loc[self.__soluce[self.__qcol]==question,self.__scol].tolist()[0]
        except:
            print("error, question not exist")
            return None
        if TestFunctions.__EXTRA_DELIMITER in txt:
            txt = '\n'.join(txt.split(TestFunctions.__EXTRA_DELIMITER))
        print(f"Solution à la question {question}\n\n{txt}")
        return output

    
    def __f_crypt(y,key,option="crypt"):
        clair = sorted(r"ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz0123456789²&é'(-è_çà)#{[|^@]}?,;.:/!§*+µ$£%=",key=str.lower)
        clair = "".join(clair)
        crypte = "".join([clair[(key+i)%len(clair)] for i,_ in enumerate(clair)])
        if option == "crypt":
            return "".join([crypte[clair.find(i)] for i in y])
        else:
            clair = "".join([crypte[(-key+i)%len(crypte)] for i,_ in enumerate(crypte)])
            return "".join([clair[crypte.find(i)] for i in y])
    
    def __change_to_list(x):
        try:
            y = iter(x)
            next(y)
        except:
            x = [x]
        return x
    
    def __type_of(x):
        x = TestFunctions.__change_to_list(x)
        types_number = [float,np.float64,np.float32,np.float16,int,complex,np.int32,np.int16,np.int64]
        types_str = [str,np.str_]
        resultats=[]
        for elem in x:
            if type(elem) in types_number:
                resultats.append('number')
            elif type(elem) in types_str:
                resultats.append('str')
            else:
                resultats.append('unknow')
        return resultats
    
    def __animation():
        anim = r"-/|\o"
        for i in range(20):
            sleep(0.05)
            print(anim[i % len(anim)],end='\r',flush=True)
            
    def __check_info(df):
        return False if "bound method DataFrame.info" in str(df.info) else True

    
        
    def check_func(self,func,attempt_res,*arg,**d):
        resultat = TestFunctions.__change_to_list(func(*arg))
        attempt_res = TestFunctions.__change_to_list(attempt_res)
        type_results = TestFunctions.__type_of(resultat)
        l_arg = ', '.join([str(a) for a in list(arg)])
        l_res = ', '.join([str(r) for r in resultat])  if not isinstance(resultat,str) else [resultat]
        l_att = ', '.join([str(a) for a in attempt_res]) if not isinstance(attempt_res,str) else [attempt_res]
        txt = f"Your fonction return {func.__name__}({l_arg})= {l_res} - the attempted value is {l_att}\n"
        print(txt)
        #○print(resultat,attempt_res,type_results)
        final_result = True
        for rv,av,typ in zip(resultat,attempt_res,type_results):
            if typ == 'number':
                try:
                    assert np.isclose(av,rv).all()
                except:
                    final_result = False
            if typ in ['str','unknow']:
                try:
                    assert av.strip() == rv.strip()
                except:
                    final_result = False
        txt_result = f'{Fore.GREEN}SUCCESS{Style.RESET_ALL}, u can continue' if final_result else f'{Fore.RED}FAILLED{Style.RESET_ALL}, u must retry'
        print(f">>> the test is {txt_result}")
        return final_result
    
    def check_df(self,df,*t,opt='exist',suspense = False,**d):
        """
        test si les arguments (str) sont des colonnes de la dataframe df
        """
        reussi = f"{Fore.GREEN} test passed {Style.RESET_ALL}"
        echec = f"{Fore.RED} test failled {Style.RESET_ALL}"
        resultat = True
        if len(t)==1 and isinstance(t[0],str) and '/' in t[0]:
            t = (t[0].strip('/')).split('/')
        for elem in t:
            if suspense: 
                TestFunctions.__animation()
            if opt == 'exist':
                if elem in list(df):
                    print(f"column '{elem}' exist ==> {reussi}")
                elif elem == '__info':
                    if not TestFunctions.__check_info(df):
                        print(f"There is no information in your dataframe ==> {echec}")
                        print(f"Warning - unnamed dataframe\nPlz write ma_dataframe.info='something'")
                        resultat = False
                    else:
                        print(f"An info = '{df.info}' is present in the dataframe ==> {reussi}")
                else:
                    print(f"Column '{elem}' is not present ==> {echec}")
                    resultat = False
            elif opt == 'noexist':
                if elem not in list(df):
                    print(f"Column '{elem}' is not present ==> {reussi}")
                else:
                    print(f"Column '{elem}' is still present ==> {echec}")
                    resultat = False  
        return resultat

    # def check_op2(self,df,y,func,*x,**d):
    #     # fonction qui vérifie qu'une colonne est une fonction de plusieurs autres
    #     # df : dataframe
    #     # y colonne à évaluer
    #     # func : fonction lambda crypté de plusieurs variables
    #     #*x colonnes 
    #     #local_args : dict d'autres grandeurs qui ne sont pas des colonnes
    #     k = d.get('ñ',0)
    #     local_args =d.get("local_args",None) #de la forma {"A_f":0.90,...} extra valeurs
    #     if k == TestFunctions.__SPY_KEY:
    #         print("la méthode check_op ne fonctionne pas quand elle est décorée")
    #         exp_u = TestFunctions.__f_crypt(func,TestFunctions.__SPY_KEY,"crypt")
    #         print(func,exp_u)
    #         (_,_,_,text)=traceback.extract_stack()[-2]
    #         print(text)
    #         df_name = text[text.index('_op2(')+5:text.index(',')].strip()
    #         txt = f"{self.__def_name}.check_op2({df_name},'{y}','{exp_u}',{','.join(list(x))})"
    #         return None
    #     func_txt = TestFunctions.__f_crypt(func,TestFunctions.__SPY_KEY,"decrypt")
    #     funcd = eval(func_txt)
    #     txt, args_count = [],0
    #     for arg in x:
    #         txt.append(f"""df['{arg}']""")
    #         args_count += 1
    #     if local_args is not None:
    #         for arg in local_args:
    #             txt.append(f"""{local_args[arg]}""")
    #             args_count += 1
    #     txt = ",".join(txt)
    #     try:
    #         if args_count == 1:
    #             df[f"__eval_{y}"] = funcd(eval(txt))
    #         else:
    #             df[f"__eval_{y}"] = funcd(*eval(txt))
    #         resultat = np.isclose(df[y].fillna(0),df[f"__eval_{y}"].fillna(0))
    #         #☻print(resultat)
    #     except:
    #         print(f"Rien ne va, votre crypto est mauvais\n{funcd}")
    #         return None
    #     final_result = False
    #     if resultat.all():
    #         final_result = True
    #         print(f"La fonction qui définie {y} convient -> {Back.GREEN} Le test est réussi"+Style.RESET_ALL)
    #     else:
    #         print(f"La fonction qui définie {y} ne convient pas -> {Back.RED} echec"+Style.RESET_ALL)
    #     df.del_columns(f"__eval_{y}")
    #     return final_result
    
    def check_op2(self,df,y,func,*x,**d):
    # fonction qui vérifie qu'une colonne est une fonction de plusieurs autres
    # df : dataframe
    # y colonne à évaluer
    # func : fonction lambda crypté de plusieurs variables
    #*x colonnes ou extra args
        k = d.get('ñ',0)
        if k == TestFunctions.__SPY_KEY:
            print("la méthode check_op2 ne fonctionne pas quand elle est décorée")
            exp_u = TestFunctions.__f_crypt(func,TestFunctions.__SPY_KEY,"crypt")
            print(func,exp_u)
            (_,_,_,text)=traceback.extract_stack()[-2]
            df_name = text[text.index('_op2(')+5:text.index(',')].strip()
            return None
        func_txt = TestFunctions.__f_crypt(func,TestFunctions.__SPY_KEY,"decrypt")
        funcd = eval(func_txt)
        txt, args_count = [],0
        for arg in x:
            if arg in df.columns.to_list():
                txt.append(f"""df['{arg}']""")
            else:
                txt.append(f"""{arg}""")
            args_count += 1
        txt = ",".join(txt)
        try:
            if args_count == 1:
                df[f"__eval_{y}"] = funcd(eval(txt))
            else:
                df[f"__eval_{y}"] = funcd(*eval(txt))
            resultat = np.isclose(df[y].fillna(0),df[f"__eval_{y}"].fillna(0))
            #☻print(resultat)
        except:
            print(f"Rien ne va, votre crypto est mauvais\n{funcd}")
            return None
        final_result = False
        if resultat.all():
            final_result = True
            print(f"La fonction qui définie {y} convient -> {Back.GREEN} Le test est réussi"+Style.RESET_ALL)
        else:
            print(f"La fonction qui définie {y} ne convient pas -> {Back.RED} echec"+Style.RESET_ALL)
        df.del_columns(f"__eval_{y}")
        return final_result
    
    def check_op(self , df , y , exp , suspense=True , **d):
        """
        vérifie que colonne la colonne y est définie par l'expression mathémétique exp
        Exemple: soit df une dataframe possédant 't' comme colonne de temps et 'x' vérifiant
            x = 3*t-9
            >check_op(self,df,'x','6iHiéA2|ç') retourne :
                La fonction x=3*t-9 convient ->  Le test est réussi
        """
        print("..")
        k = d.get('ñ',0)
        if k == TestFunctions.__SPY_KEY:
            print("la méthode check_op ne fonctionne pas quand elle est décorée")
            exp_u = TestFunctions.__f_crypt(exp,TestFunctions.__SPY_KEY,"crypt")
            (_,_,_,text)=traceback.extract_stack()[-2]
            df_name = text[text.index('_op(')+4:text.index(',')].strip()
            txt = f"{self.__def_name}.check_op({df_name},'{y}','{exp_u}')"
            print(txt)
            return None
        
        expd = TestFunctions.__f_crypt(exp,TestFunctions.__SPY_KEY,"decrypt")
        
        try:
            df[f"__eval_{y}"] = df.eval(expd)
            resultat = np.isclose(df[y].fillna(0),df[f"__eval_{y}"].fillna(0))
            #☻print(resultat)
        except:
            print(f"Rien ne va, votre crypto est mauvais\n{expd}")
            return None
        if suspense:
            TestFunctions.__animation()
        final_result = False
        if resultat.all():
            final_result = True
            print(f"La fonction {y}={expd} convient -> {Back.GREEN} Le test est réussi"+Style.RESET_ALL)
        else:
            print(f"La fonction qui définie {y} ne convient pas -> {Back.RED} echec"+Style.RESET_ALL)
        df.del_columns(f"__eval_{y}")
        return final_result
    
    
    def check_specop(self,df,y,exp,**d):
        """
        vérifie que colonne la colonne y est définie par l'expression mathémétique spéciale (genre dérivée)
        Exemple: soit df une dataframe possédant 't' comme colonne de temps et 'x' vérifiant
            df['dv'] = df['v'].shift(-1) - df['v'].shift(1)
            >check_op(self,df,'dv','6iHiéA2|ç') retourne :
                La fonction convient ->  Le test est réussi
        """
        k = d.get('ñ',0)
        if k == TestFunctions.__SPY_KEY:
            print("la méthode check_specop ne fonctionne pas quand elle est décorée")
            if '"' in exp:
                print(f'il ne faut pas utiliser de guillement double " dans l'' expression {exp}')
                return None
            exp_u = TestFunctions.__f_crypt(exp,TestFunctions.__SPY_KEY,"crypt")
            (_,_,_,text)=traceback.extract_stack()[-2]
            df_name = text[text.index('cop(')+4:text.index(',')].strip()
            txt = f"{self.__def_name}.check_specop({df_name},'{y}','{exp_u}')"
            print(txt)
            return None
        ym = f"__eval_{y}"
        expd = TestFunctions.__f_crypt(exp,TestFunctions.__SPY_KEY,"decrypt")
        if d.get('debug',False)==True:
            print("exp=",exp,"expd=",expd)
        try:
            exp_tot = f"df['{ym}']={expd}"
            exec(exp_tot)
            resultat = np.isclose(df[y].fillna(0),df[ym].fillna(0))
        except:
            print(f"Rien ne va, votre crypto est mauvais")
            return None
        final_result = False
        if resultat.all():
            final_result = True
            print(f"La fonction qui définie {y} convient -> {Back.GREEN} Le test est réussi"+Style.RESET_ALL)
        else:
            print(f"La fonction qui définie {y} ne convient pas -> {Back.RED} echec"+Style.RESET_ALL)
        df.del_columns(ym)
        return final_result

    def check_graph(self,txt_c,level=0,suspense=True,**d):
        """
        nunez = alt+164
        """
        TestFunctions.__SPY = TestFunctions.__get_SPY()
        k = d.get('ñ',0)
        if k == TestFunctions.__SPY_KEY:
            txt_k = TestFunctions.__give_me_crypto(level).split('||')[2]
            #txt_k = TestFunctions.__give_me_crypto(0)
            txt = f"{self.__def_name}.check_graph({txt_k},level={level})"
            print(txt)
            return txt
        secret = TestFunctions.__f_crypt(txt_c,TestFunctions.__SPY_KEY,"decrypt")
        try:
            dd = eval(secret)
            t = dd['method']
        except:
            print(f"Rien ne va, votre crypto est mauvais\n {secret}")
            return None
        same = TestFunctions.__dict_compare(dd,TestFunctions.__SPY[-1-level])
        if suspense:
            TestFunctions.__animation()
        final_result = False
        if len(same) == len(dd):
            print(f"Votre {t} {dd} est correct ==> {Fore.GREEN} test réussi {Style.RESET_ALL}")
            final_result = True
        else:
            print(f"Votre {t} de level={level} n'est pas correct ==> {Fore.RED} echec au test {Style.RESET_ALL}")
        return final_result
    
    def __dict_compare(d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return same 
    
    def check_var(self,glob_var,*variables,**d):
        if isinstance(variables,str):
            variables=list(variables)
        final_result = True
        for var in variables:
            TestFunctions.__animation()
            if var in glob_var:
                print(f"variable {var} exist ... test success")
            else:
                print(f"variable {var} not exist ... failled, RETRY...")
                final_result = False
        return final_result
    
    def check_var_fnct_other_var(self,glob_var,var1,fnct,*var2s,converters={},**d):
        """

        Parameters
        ----------
        glob_var : globals()
            obligatoire
        var1 : str
            variable a tester.
        fnct : fonction tq var1 = f(var2s)
            DESCRIPTION.
        *var2s : tuple de str
            DESCRIPTION.

        Returns
        -------
        bool
            True or False.

        """
        assert isinstance(var1,str),f"{var1} doit être de type str"
        for v in var2s:
            assert isinstance(v,str),f"{v} doit être de type str"
        if var1 in glob_var:
            value = glob_var[var1]
            value = converters.get(var1,lambda x:x)(value)
            if converters != None:
                pass
            value_other = []
            for v in var2s:
                value_other.append(converters.get(v,lambda x:x)(glob_var[v]))
            if np.all(value == fnct(*tuple(value_other))):
                print(f"{var1} correct défine")
                return True
            else:
                print(f"{var1} isnt correct défine, please retry definition of {var1}")
                return False
        else:
            print(f"variable {var1} n'est pas définie ... recommencez")
            return False
            
            
    
    def check_var_value(self,glob_var,variable,value,func = None,**d):
        """ input:
            *glob_var = globals()
            *variables: str, name of variable
            *value: expected value
            *func: callable (typiccaly lambda), if use, expected value = func(value)
        """
        assert isinstance(variable,str),"variable must be str"
        if func != None:
            assert callable(func),"func is not a callable ..."
            value = func(value)
        TestFunctions.__animation()
        if variable in glob_var:
            print(f'Variable "{variable}" exist '+u"\U0001F600")
            chk = True
            if isinstance(value,float):
                chk = np.isclose(value,glob_var[variable])
            else:
                chk = value == glob_var[variable]
            if chk:
                print(f'your variable is correct defined\nContinu')
                return True
            else:
                print('your variable isnt correct defined\nplease retry')
                return False
        else:
            print('error, u not defined the good variable\nplease retry'+u"\U0001F629")
            return False
        
    def check_var_type(self,glob_var,variable,stype=(int,float),**d):
        if variable not in glob_var:
            return False
        else:
            _variable = glob_var[variable]
        chk = isinstance(_variable,stype)
        if not chk:
            print(f"variable/instance '{variable}' must be {stype} but not {type(_variable)}")
            return False
        else:
            print(f"variable/instance '{variable}' type success")
            return True


    def var_exist(self,var,glob_var,**d):
        if var in glob_var():
            print(f"variable {var} est définie ... continuez")
            return True
        else:
            print((f"variable {var} n'est pas définie ... recommencez"))
            return False
            
        