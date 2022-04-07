import json
import sys

configfile = "config.json"

inputfile = "test.json"


table_names = []

def parse(filename):
    
    with open(filename) as f:
        
        try:
            return json.load(f)
        
        except ValueError as e:
            print('invalid json: %s' % e)           
            sys.exit()


def checkConfig(configJSON):
    
    print("\n\nVerifying config file......")
    
    #checks if JSON file has only one key called "schema", and if it is an array
    if(len(list(configJSON.keys())) != 1):
        print("Error in config syntax")
        sys.exit()
    else:
        if(list(configJSON.keys())[0] != 'schema'):
            print("Error in config syntax")
            sys.exit()
        else:
            if(isinstance(configJSON['schema'], list) == False):
                print("Error in config syntax")
                sys.exit()
            
    
    for table in configJSON['schema']:
        #check presence of key name
        
        table_names.append(table['name'])
        
        primary_key_ctr = 0
        
        
        for fields in table['fields']:
            #check presence of fields
            
            req_param = ["column_name","type","isPrimary","isForeign","ref"]
            
            #checks if all parameters are passed anf in correct order
            if(list(fields.keys()) != req_param):
                print("Missing parameters or parameters in incorrect order")
            
            #checks for correct datatypes
            if( type(list(fields.values())[0]) != str  ):
                
                print("Invalid datatype for: " + list(fields.keys())[0])
                print("Required datatype: String")
                sys.exit()
            
            if( type(list(fields.values())[2]) != bool  ):
                
                print("Invalid datatype for: " + list(fields.keys())[2])
                print("Required datatype: Boolean")
                sys.exit()
            
            if( type(list(fields.values())[3]) != bool  ):
                
                print("Invalid datatype for: " + list(fields.keys())[3])
                print("Required datatype: Boolean")
                sys.exit()
            
            if( type(list(fields.values())[1]) != bool and type(list(fields.values())[1]) != str and type(list(fields.values())[1]) != int and type(list(fields.values())[1]) != float ):
                
                print("Invalid datatype for: " + list(fields.keys())[1])
                print("Required datatypes: string, numeric, bool")
                sys.exit()
            
            if( type(list(fields.values())[4]) != str and type(list(fields.values())[4]) != type(None) ):
                
                print("Invalid datatype for: " + list(fields.keys())[4])
                print("Required datatype: string, null")
                print(type(list(fields.values())[4]))
                sys.exit()
            
            
            if(fields['isPrimary'] == True):
                primary_key_ctr += 1
        
        #checks for primary key error
        if(primary_key_ctr > 1):
            print("Error! Mulitple primary keys in " + table['name'])
            sys.exit()
    
    print("Verified config file!")


def checkInput(inputfile, configJSON):
    
    print("\n\nVerifying input file......")
    
    jobj = parse(inputfile)
    
    tab_idx = -1

    
    #checks if table name exists
    for i in range(0, len(table_names)):
        
        if(jobj['table'] == table_names[i]):
            
            tab_idx = i
        
    if(tab_idx == -1):
        
        print("Invalid table name!")
        
        sys.exit()
    
    #checks if correct number of values are provided
    if(len(jobj['values']) != len(configJSON['schema'][tab_idx]['fields'])):
        
        print("Invalid number of input values for table " + configJSON['schema'][tab_idx]['name'])
        print("Required number of inputs: " + str(len(configJSON['schema'][tab_idx]['fields'])))
        
        sys.exit()
    
    
    idx = 0
    
    #checks if all inputs are of correct data types
    for fields in configJSON['schema'][tab_idx]['fields']:
        
        if(idx >= len(configJSON['schema'][tab_idx])):
            break
        
        if(type(jobj['values'][idx]) != type(fields['type'])):
            
            print("Data type does not match column data type")
            print("Required data type: " + str(type(fields['type'])))
            print("Your data type: " + str(type(jobj['values'][idx])))
            sys.exit()
        
        idx += 1
    
    print("Verified input file!")
    

def run():
    
    #check config file
    configJSON = parse(configfile)
    
    checkConfig(configJSON)
    
    #check input file
    checkInput(inputfile, configJSON)

run()

