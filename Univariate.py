class Univariate():
    def QuanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            if dataset[columnName].dtype=='O':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan, qual
    
    def UniVariate(dataset,quan):
        descriptive=pd.DataFrame(index=["mean","median","mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
                               "IQR","1.5rule","Lesser","Greater","Min","Max"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["mean"]=dataset[columnName].mean()
            descriptive[columnName]["median"]=dataset[columnName].median()
            descriptive[columnName]["mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
        return descriptive
    
    def freqTable(columnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","CumSum"])
        freqTable["Unique_Values"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"]=(freqTable["Frequency"]/103)
        freqTable["CumSum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable
     
    
    def checkOutliers(quan,descriptive):
        lesser=[]
        greater=[]
        for columnName in quan:
           if (descriptive[columnName]["Lesser"]>descriptive[columnName]["Min"]):
                lesser.append(columnName)
           if (descriptive[columnName]["Greater"]<descriptive[columnName]["Max"]):
                greater.append(columnName)
        return lesser,greater
    
    def replaceOutliers(lesser,greater,dataset,descriptive):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]=descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]
        return dataset
    