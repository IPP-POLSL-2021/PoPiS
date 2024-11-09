import pandas as pd

import time


def getResults(Correlation, electionSelections, type):
    str = ""
    if type == "procentowe":
        str = "_proc"
    match electionSelections:
        case"województwa":
            print(
                f"./Data/wyniki_gl_na_listy_po_wojewodztwach{str}_sejm_utf8.csv")
            Results = pd.read_csv(
                f"./Data/wyniki_gl_na_listy_po_wojewodztwach{str}_sejm_utf8.csv", sep=";",  decimal=",")
            Results = Results.drop(labels=["Województwo"], axis=1)
            # print(Results.columns)
        case"okręgi":

            Results = pd.read_csv(
                f"./Data/wyniki_gl_na_listy_po_okregach{str}_sejm_utf8.csv", sep=";",  decimal=",")
            # print("Columns in the DataFrame:")
            # print(Results.columns)
            # print(Results.head())
            Results = Results.drop(labels=["Nr okręgu"], axis=1)
            # print(Results)
        case "powiaty":
            Results = pd.read_csv(
                f"./Data/wyniki_gl_na_listy_po_powiatach{str}_sejm_utf8.csv", sep=";",  decimal=",")
            # print("Columns in the DataFrame:")
            # print(Results.columns)
            # print(Results.head())
            Results = Results.drop(labels=["TERYT Powiatu",
                                           "Powiat",
                                           "Województwo",
                                           "Nr okręgu"], axis=1)
        case "gminy":
            Results = pd.read_csv(
                f"./Data/wyniki_gl_na_listy_po_gminach{str}_sejm_utf8.csv", sep=";",  decimal=",")
            # print("Columns in the DataFrame:")
            # print(Results.columns)
            # print(Results.head())
            Results = Results.drop(labels=["TERYT Gminy",
                                           "Gmina",
                                           "Powiat",
                                           "Województwo",
                                           "Nr okręgu"
                                           ], axis=1)
        # Results.describe()
        case "obwody":
            Results = pd.read_csv(
                f"./Data/wyniki_gl_na_listy_po_obwodach{str}_sejm_utf8.csv", sep=";",  decimal=",")
            Results = Results.drop(labels=["Nr komisji",
                                           "Siedziba",
                                           "TERYT Gminy",
                                           "Gmina",
                                           "Powiat",
                                           "Województwo",
                                           "Nr okręgu",
                                           ], axis=1)
    # if type != "procętowe":
    #     Results = Results.drop(labels=["Liczba uwzględnionych komisji", "Komisja otrzymała kart do głosowania",
    #                                    "Nie wykorzystano kart do głosowania",
    #                                    "Liczba wyborców, którym wydano karty do głosowania w lokalu wyborczym oraz w głosowaniu korespondencyjnym (łącznie)",
    #                                    "Liczba wyborców głosujących na podstawie zaświadczenia o prawie do głosowania",
    #                                    "Liczba kopert zwrotnych, w których nie było oświadczenia o osobistym i tajnym oddaniu głosu",
    #                                    "Liczba kopert zwrotnych, w których nie było koperty na kartę do głosowania",
    #                                    "Liczba kopert zwrotnych, w których znajdowała się niezaklejona koperta na kartę do głosowania",
    #                                    "Liczba kart wyjętych z urny", "W tym liczba kart wyjętych z kopert na kartę do głosowania",
    #                                    "Liczba kopert zwrotnych, w których oświadczenie nie było podpisane", "Liczba kart nieważnych",
    #                                    "Liczba kart ważnych",
    #                                    "W tym z powodu postawienia znaku „X” wyłącznie obok nazwiska kandydata na liście, której rejestracja została unieważniona",
    #                                    "KOMITET WYBORCZY POLSKA JEST JEDNA", "KOMITET WYBORCZY WYBORCÓW RUCHU DOBROBYTU I POKOJU",
    #                                    "KOMITET WYBORCZY NORMALNY KRAJ", "KOMITET WYBORCZY ANTYPARTIA", "KOMITET WYBORCZY RUCH NAPRAWY POLSKI",
    #                                    "KOMITET WYBORCZY WYBORCÓW MNIEJSZOŚĆ NIEMIECKA"], axis=1)
    columns_to_drop = [
        'Nr okręgu', 'Liczba uwzględnionych komisji', 'Komisja otrzymała kart do głosowania',
        'Nie wykorzystano kart do głosowania',
        'Liczba wyborców, którym wydano karty do głosowania w lokalu wyborczym oraz w głosowaniu korespondencyjnym (łącznie)',
        'Liczba wyborców głosujących na podstawie zaświadczenia o prawie do głosowania',
        'Liczba kopert zwrotnych, w których nie było oświadczenia o osobistym i tajnym oddaniu głosu',
        'Liczba kopert zwrotnych, w których oświadczenie nie było podpisane',
        'Liczba kopert zwrotnych, w których nie było koperty na kartę do głosowania',
        'Liczba kopert zwrotnych, w których znajdowała się niezaklejona koperta na kartę do głosowania',
        'Liczba kart wyjętych z urny',
        'W tym liczba kart wyjętych z kopert na kartę do głosowania',
        'Liczba kart nieważnych',
        'Liczba kart ważnych',
        'W tym z powodu postawienia znaku „X” wyłącznie obok nazwiska kandydata na liście, której rejestracja została unieważniona',
        'KOMITET WYBORCZY POLSKA JEST JEDNA',
        'KOMITET WYBORCZY WYBORCÓW RUCHU DOBROBYTU I POKOJU',
        'KOMITET WYBORCZY NORMALNY KRAJ',
        'KOMITET WYBORCZY ANTYPARTIA',
        'KOMITET WYBORCZY RUCH NAPRAWY POLSKI',
        'KOMITET WYBORCZY WYBORCÓW MNIEJSZOŚĆ NIEMIECKA'
    ]

    # Drop only the columns that exist in the DataFrame
    Results = Results.drop(
        columns=[col for col in columns_to_drop if col in Results.columns], axis=1)
    # print(Results)
    Corr_Matrix = Results.corr()
    Corr_Matrix_Larger_Than = Corr_Matrix > Correlation
    Corr_Matrix = Corr_Matrix[Corr_Matrix_Larger_Than]
    Corr_Matrix=round(Corr_Matrix,2)
    # print(Corr_Matrix)

    return Corr_Matrix, Results
