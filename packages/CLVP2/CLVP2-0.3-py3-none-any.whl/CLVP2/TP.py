from .modules import *


class CLV(object):

    
    @staticmethod
    def train(file_path):
        
        df = Utils.read_csv_file(file_path)

        if df['isSuccess']:
            

            remove_columns =['Country', 'City','Province','CountryId','VisitLastDate',
                     'VisitFirstDate','LastPurchaseDate',
                     'FirstPurchaseDate','CityId','ChurnValue','CustomerId']

            cleaning = CleaningData(remove_columns=remove_columns)

            data = cleaning.Remove_Columns(df['data'])
            data = cleaning.Remove_Nulls(data)
            data = cleaning.Remove_Most_Frequent(data)
            data = cleaning.Reset_Index(data)


            spliting  =  Splitting_Data(windows=5,shift=1)
            x = spliting.Dividing_Data(data,train=1)
            #print(x['isSuccess'])
            if x['isSuccess']:
                
                non_time_series,time_series,features_non_time_series,features_time_series =  x['data'][0],x['data'][1],x['data'][2],x['data'][3]
                data = spliting.Creating_Dataset(non_time_series,time_series)
                x_non_time_series,x_time_series,y_train = spliting.Shuffling_Seprating_Data(data)
                x_train_non_time_series,x_validation_non_time_series,x_test_non_time_series,x_train_time_series,x_validation_time_series,x_test_time_series,y_train,y_validation,y_test = spliting.Split_Data(x_non_time_series,x_time_series,y_train )
                x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,scaler1,scaler2 = spliting.Normalize_data(x_train_non_time_series,x_validation_non_time_series,x_test_non_time_series,x_train_time_series,x_validation_time_series,x_test_time_series)

                s1 = spliting.save_model(scaler1,'scaler1','ScalerFiles')
                s2 = spliting.save_model(scaler2,'scaler2','ScalerFiles')
                
                if s1['isSuccess'] and s2['isSuccess']:
                                
                    y_train = np.array(y_train)
                    y_validation = np.array(y_validation)
                    y_test = np.array(y_test)

                    automating =  automated_parameter_selection(x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,y_train,y_validation,y_test)
                    best_parameters = automating.run()

                    results=automating.train_save_best_model(best_parameters)
                    if results['isSuccess']:
                            


                        return {"model_url":results['data'],"scaler1_url":s1['data'],"scaler2_url":s2['data'],"non_time_series_features":x['data'][2],"isSuccess":results['isSuccess']}


                    else:
                        print("error code: "+str(results['error']['code']))
                        print("error message: "+str(results['error']['message']))
                        return {"isSuccess":results["isSuccess"]} 

                else:
                    if not s1['isSuccess']:
                        print("error code: "+str(s1['error']['code']))
                        print("error message: "+str(s1['error']['message']))
                        return {"isSuccess":s1["isSuccess"]} 
                    
                    else:

                        print("error code: "+str(s2['error']['code']))
                        print("error message: "+str(s2['error']['message']))
                        return {"isSuccess":s2["isSuccess"]} 


                    
            else:
                
                print("error code: "+str(x['error']['code']))
                print("error message: "+str(x['error']['message']))
                return {"isSuccess":x["isSuccess"]} 
 
                    
        else:
            print("error code: "+str(df['error']['code']))
            print("error message: "+str(df['error']['message']))
            return {"isSuccess":df["isSuccess"]} 

    @staticmethod
    def predict(file_path,model_url,scaler1_url,scaler2_url,non_time_series_features):
        

        df = Utils.read_csv_file(file_path)

        if df['isSuccess']:
            remove_columns =['Country', 'City','Province','CountryId','VisitLastDate',
                     'VisitFirstDate','LastPurchaseDate',
                     'FirstPurchaseDate','CityId','ChurnValue','CustomerId']

            cleaning = CleaningData(remove_columns=remove_columns)

            data = cleaning.Remove_Columns(df['data'])
            data = cleaning.Remove_Nulls(data)
            data = cleaning.Remove_Most_Frequent(data)
            data = cleaning.Reset_Index(data)
            spliting  =  Splitting_Data(windows=5,shift=1)
            x = spliting.Dividing_Data(data,train=0)
            #print(data)
            
            
            if x['isSuccess']:
                
                non_time_series,time_series =  x['data'][0],x['data'][1]
                non_time_series_columns= [i for i in non_time_series.columns]
                if  len(non_time_series_columns)==len(non_time_series_features):
                
                    non_time_series = np.array(non_time_series.values)
                    time_series = np.array(time_series.values)

                    try:
                        model = tf.keras.models.load_model(model_url)
                    except:
                        return print("error code 5: the model file does not exist")

                    try:
                        
                        pickle_in = open(scaler1_url+".pickle","rb")
                        scaler1 = pickle.load(pickle_in)
                        
                        pickle_in = open(scaler2_url+".pickle","rb")
                        scaler2 = pickle.load(pickle_in)
                    except:
                        return print("error code 6: the scalar file does not exist")


                    non_time_series = scaler1.transform(non_time_series)
                    time_series = scaler2.transform(time_series)
                    x = model.predict([non_time_series,time_series])
                    data['output'] = x

                    name = Utils().generate_file_name("results")
                    path = Utils().save_pipeline("output")
                    final_name=path+'\\'+name
                    try : 
                        data.to_csv(final_name+".csv", index=False, header=True)
                        return final_name
                    except:
                        return print("error code 8: the results file not saved")
                    
                else:
                           
                    return print("error code 7: missing features columns")

            
            
            else:
                print("error code: "+str(x['error']['code']))
                
                return print("error message: "+str(x['error']['message']))

        else:
            print("error code: "+str(df['error']['code']))
            
            return print("error message: "+str(df['error']['message']))

            

