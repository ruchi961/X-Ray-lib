# Consists of backend logic and running

## To run follow the instrcutions

please refer down for logic, core idea, motivation

## Pre requirements 

**Windows**
```
python -m venv venv
```

**Linux/MacOS**
```
python3 -m venv venv
```

**Windows**

```
venv\Scripts\activate
```

**Linux/MacOS**
```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

## Main 

**1. Create a json file** 

This is the only step that needs to be created manually or using platforms like cursor, etc where people have subscriptions or free usage. 

This is because it has essiential description of components which are defined by developer.

**Run**
```
cd backend
python check_main.py
```
**Input:** 

> main.json file, schema of compoennts is deined here. 

**Output:**

> Project folder is created with components wise json and single .json file with basic input output etc format  main_data_file.json is created or updated, validation of main.json file is also done here.

**2. Create a json file** 

This can be done **manually by user** to add the json file, 
```
go to the main.json file and edit the files for the content, the basic keys remain the same, just update the values, also all values are required, to run a new project change parameters and re run the entire procedure with changed json   
```

or it can be done with llm, please put your key in the env file under the llm_api_key 
```
GEMINI_API_KEY="KEY_HERE" 
```

or it can be done by using platforms like cursor if user has subscription

**Run**
```
cd backend
python create_workflow.py
```
**Input:** 

> project_name/components.json files, schema of compoennts is defined here. 

**Output:**

> schema is updated in eahc components files and under graphs>worflow_hierarchy.png is created, single.json is created, if llm is used, other validation is done 


**3. Check changes to code**

After the changes to code are done meaning logging is done, run this file to check if proper json logging is done, meaning the keys defined in schema are logged properly in original code of user, run this validates and tells whcih keys are missing 

**Run**
```
cd backend
python check_code.py
```
**Input:** 

> main.json file, and the changes to code are done is original code., enter the project id 

**Output:**

> Code is validated is some keys are missing those are printed else code has all the keys is printed


**4. Run the main server for continuous evaulation and logging,and UI requests to cater**

Thisis the serve which is platform independent and handles the logging as well as catering to ui request, two servers can be dmade for theis purpose but for demo puropese kept one, it also producing reasoning with the help of llm, for giving logging, to debug later what was the overall outcome of the fucntion execution for a query
**Run**
```
cd backend
python flask_server_main.py
```

**Input:** 

> make sure earlier steps are run and done also project_name/schema, main.json and main_data_file.json are properly created/defined also, proper parameters in code 

**Output:**

> in logs folder, component and query wise logs are created, also the single query wise logs are craeted also UI request response of project dta display is handled

**5.Run the frontend.html file for access of UI**

the frontend contains two functionalities, it lists projects, and the nonce projects are select get either query wise all component dta or query plus component data to debug plus see the workflow pictorically to refer to the workflow pictorically.

**Run**
```
run the htnl file by clicking and make sure the flask server is running
```

**Input:** 

> run all steps and create a project and run the flask server to get values in UI, all handling of cases is done for the website.

**Output:**

> see the output of pipeline




ready to go 


* You can check the json file being updated in the specific folder same as project name in the root folder meaning backend/projectname/log/components_json_files

* Also in the project/graph/ folder, workflow_hierarchy.json tells the flow of the project pictorically

* The json file along with components have one more json file for logging the entire request flow named single.json flow



# Frontend
* Javascript
* HTML
* CSS
> No framework but can easily be converted to any framework like vuejs etc , depending on the requirements of real libray and scope 

# Backend
* Flask
* Python
> Choose this as have worked a lot previously with this so for for demo but again as per real application, depending on latency cost, etc decision can be made 


# Files descriptions:
* Backend

> **'.env'**-> contains env for file 


> **'check_main.py'**-> 1st step implementation checks the main.json validate and create project folder with basic components schemas
 
> **'config_system_prompt.py'** -> contains the system prompt for getting the configuration of key value of components for code given.

> **'create_graph.py'** -> create the graph with nodes and edges

> **'create_workflow.py'** ->2nd step create the key value pairs for logging with llm+validate, else validate only

>  **'Demo'** -> Demo code just return dummy values
 
>  **'democ_code'** -> Democ code with implememnntation for llm call of key value pair s generation

> **'flask_server_main.py'** -> main server for ui acces andlogging, does the reasoning with llm as well
 
> **'llm_call.py'** -> implemetation of gemini api but request can be automated to suit all paltforms but since i dint have keys of ther platform so this.

> **'main.json'**-> json file for compoennts to be included descirpiton

> **'main_data_file.json'** -> keeps track of all projects main.json file
 
> **'reasoning_system_prompt.py**'-> for getting reasoning

> **'requirements.txt'** > requirements file

> **'check_code.py'** > check the code if it does really does logging mean sending requets to flask server with the required keys as per components schema


* Frontend

>**'frontend.HTML'** -> UI created with JS fron function and logic handling, html for basic layour with cssfor style, add listeners, used fetch for request reposnse etc 

# Logic and tradeoffs

This section contains core conception, thinking, motivation, origin idea, why xyz was choosen, trade offs.

### Core conception:
When I thought of solving the probleM I thought we need something to find out the flow of business lofic means how componenst are executed how they interact etc, once that is known know where the main logic or evaluation is done meaning were main code gets executed and how decisions are made in that function, once that is known next to log these decisions,
so my pipeline focuses on the same.

1.**Create a json file** -> this is where the develope can define his/her components involved, what is the system about the components


2. **Create another json file** -> based on the above json create a new json file whcih has key value pairs that are to be logged, eg : input:{keyword:"",limit:""}, this can be done manually base like i/o metadat tags are already created project specific tagss or keys need to be updated can be done manually or by using llm, just set create_llm_config : yes in main.json above and this will be automated, also here a pictoric workflow is created based on workflow description from above 


3. There is a need to check if actually logs are made, meaning if developer/autmated logs are made to code othervise nothing will be logged, so that too in check in original code by developer. 


4. Next the **flask server** is started , this flask server is actually the one that logs, Why? because platform independent logging now may the application be in any language vue js node js react python etc with simple request and response the messages are logged to individual project folder and components


5. To vizualize this an ui is made where **Query+all components** can be seen or **Query+specific component** can be seen 



# What could done :

* **Prompt refining** for testing for diverse cases for key value pairs, I tried few but more can be done 
* Using technology based on the requirements like **latency etc**, thisis basic for demo 
* I tried somewhere in code check instead of checking in whole code if key value logging is properly done can locate where localhost:5000 or basically flask server call is made and check first and last 10 lines from that point but the problem is sometimes some abstraction of code may be present so wont work ,reduces memory and time if too long code is used. 
* circulatory log in case json get big, or using nosql schema less database like key values types
* Adding support for uI so instaed of just component + query ican access, component only all queries backend has support for this noly to include in UI , some workflow rending nicely like floating image to refer, on right hand isde or left etc etc
* We can add logging in code with llms, only costly like llm will put logging dynacmically reduces develoepr work but again such will costly though can be optimized in terms of token and what to send 

# Trade offs

Good accuracy to find pin point to debug, but just when developer creates 1 2 step a bit longer for developer, or liitle cost for llm second step ifautomate, but proper key value pairs help understand the bottleneck.


# Loom video link:

https://www.loom.com/share/8aa00582756243d2b3a754f5c1e8a28b


https://www.loom.com/share/af01a1d77ae2427697d4d38877f5d610
