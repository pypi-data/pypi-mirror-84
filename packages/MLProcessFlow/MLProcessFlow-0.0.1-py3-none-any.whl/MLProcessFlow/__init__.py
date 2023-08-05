# Main Function Call
def MLProcessflow(List_Attributes, path, transaction, transaction_type, Experiment_Name="", parameterdict=""):
    import pandas as pd
    if List_Attributes == "" or path == "" or transaction == "" or transaction_type == "":
        print("List of Attributes,Path,Transaction,Transaction Type are required Parameters")
    else:
        if transaction == 'CREATE' and transaction_type == 'Template':
            createTemplate(List_Attributes, path)
            print("Template Successfully Created!")
        if transaction == 'CREATE' and transaction_type == 'Experiment':
            if Experiment_Name != "":
                createExperiment(Experiment_Name, path)
                print("Experiment Successfully Created!")
            else:
                print("Experiment Name required!")
        if transaction == 'UPDATE' and transaction_type == 'Experiment':
            if Experiment_Name != "" and parameterdict != "":
                UpdateExperiment(List_Attributes, Experiment_Name, parameterdict, path)
                print("Experiment Updated Successfully!")
            else:
                print("Experiment Name and Parameters in Dictionary Format are required!")


# Create Template For ProcessFlow
def createTemplate(List_Attributes, path):
    import pandas as pd
    dfAttr = pd.DataFrame({'Experiment': List_Attributes})
    dfAttr.to_csv(path, index=False)


# Create Experiment
def createExperiment(Experiment_Name, path):
    import pandas as pd
    dfreadTemplate_pd = pd.read_csv(path, delimiter=",", encoding='utf-8')
    dfreadTemplate_pd[Experiment_Name] = ''
    dfreadTemplate_pd.to_csv(path, index=False)


# Update Experiment
def UpdateExperiment(List_Attributes, Experiment_Name, parameterdict, path):
    import pandas as pd
    dfExperiment_pd = pd.read_csv(path, delimiter=",", encoding='utf-8')
    for i in range(len(List_Attributes)):
        my_var = 'Parameter_' + str(i)
        my_var = parameterdict.get(List_Attributes[i], "")
        if (my_var != ""):
            dfExperiment_pd[Experiment_Name][i] = my_var
    dfExperiment_pd.to_csv(path, index=False)