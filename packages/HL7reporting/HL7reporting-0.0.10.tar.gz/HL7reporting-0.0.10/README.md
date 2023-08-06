# HL7reporting

[Github Project](https://github.com/pjgibson25/HL7reporting)


## Background 

-----------------------

#### How it Started

My name is PJ Gibson and I am a data analyst with the Indiana State Department of Health.
My Informatics department arranged a grant with a group who could improve the quality of hospital reporting.
We needed to track the progress of this hospital reporting, which required diving into HL7 Admission/Discharge/Transfer (ADT) messages and assessing for data completion and validity.
Enter me.


#### The Goal

The main purpose of this package is to give data quality analysis functions to workers in public health informatics. 




## Functions
-----------------------

<details>
<summary>NSSP_Element_Grabber</summary>
  
<hr style="border:5px solid gray"> </hr>

## Documentation    

    
<b>NSSP_Element_Grabber(data,Timed = True, Priority_only=False, outfile='None')</b>
    

    Creates dataframe of important elements from PHESS data.

    NOTE:  Your input should contain column titles:
		MESSAGE, PATIENT_VISIT_NUMBER, PATIENT_MRN,
		FACILITY_NAME
    
    	if you don't have visitnum, mrn, or facname, create empty cols
 	appended to your message column
    
    Parameters
    ----------
    data: pandas DataFrame, required, from PHESS sql pull
    
    Timed:  Default is True.  Prints total runtime at end.
    Priority_only:  Default is False.  
        If True, only gives priority 1 or 2 elements
    outfile:  Default is 'None':
        Replace with file name for dataframe to be wrote to as csv
        Will be located in working directory.
        DO NOT INCLUDE .csv IF YOU CHOOSE TO MAKE ONE
    
    Returns
    -------
    dataframe with columns of NSSP priority elements for each message (row)

   
## Code Examples 

    

```
# read in data
data1 = pd.read_csv('somefile.csv',engine='python')

# process through NSSP_Element_Grabber() function
parsed_df = NSSP_Element_Grabber(data1,Timed=False,
                                    Priority_only=True,outfile='None')

```

*if you don't have mrn, visit_num, or facility_name

```
data1 = pd.read_csv('somefile.csv',engine='python')

# create new dataframe with correct column names
cols = ['MESSAGE','PATIENT_MRN', 'PATIENT_VISIT_NUMBER', 'FACILITY_NAME']
new_input_dataframe = pd.DataFrame(columns=cols)

# define new dataframe column using our data
new_input_dataframe['MESSAGE'] = data1['message'] # replace message according to correct column title of data1

# process through NSSP_Element_Grabber() function
parsed_df = NSSP_Element_Grabber(new_input_dataframe, Timed=False,
                                    Priority_only=True,outfile='None')
```

## Visualization of Output

<img src="https://github.com/pjgibson25/HL7reporting/raw/master/pics/nssp_element_grabber.png" alt="NSSP_Element_Grabber_Visualization">
<br>
<hr style="border:5px solid gray"> </hr>


</details>




 


        
        
        
        
 




## FAQs
-----------------------

#### Where can I access function documentation outside of this location?

Within a Jupyter Notebook document, you can type:

``FunctionNameHere?`` 

into a jupyter notebook cell and then run it with `SHIFT` + `ENTER`.
The output will show you all the function documentation including a brief description and argument descriptions.


#### Why Python?

I work entirely in Python.
In the field of public health informatics, R is the most popular programming language.
I have created this package to run as intuitively as possible with a minimal amount of python knowledge.
I could be wrong, but I believe that one day, public health informatics may become Python-dominant, so this package could help as an introduction to the environment to those unfamiliar.

#### For plottting, what if I want to make small changes such as color changes, formatting, or simple customizing?

Right now I don't have things set up for that sort of work.  My best solution would be for you to dive into my Github reposiory python file linked [here](https://github.com/pjgibson25/HL7reporting/blob/master/HL7reporting/__init__.py).  You can copy the defined functions into your document and make minor adjustments as you see fit.


#### Why isn't the NSSP_Element_Grabber() function working?

The most common problem in this situation is a incorrectly formatted input.  The input needs to be a pandas dataframe containing the following columns:

`['MESSAGE','PATIENT_MRN','PATIENT_VISIT_NUMBER','FACILITY_NAME'] `

caps DOES matter.  If your raw data file does not contain MRN, visit number, or facility name, you may create a dataframe with all NaN values for these columns and the function should still work properly.


#### My question isn't listed above...what should I do?

feel free to contact me at:

PGibson@isdh.IN.gov 

with any additional questions.

## The Author
PJ Gibson - Data Analyst for Indiana State Department of Health

## Special Thanks
* Harold Gil - Director of Public Health Informatics for Indiana State Department of Health.
Harold assigned me this project, gave me relevant supporting documentation, and helped me along the way with miscellaneous troubleshooting.
* Matthew Simmons - Data Analyst for Indiana State Department of Health.
Matthew helped walk me through some troubleshooting and was a supportive figure throughout the project.
* Shuennhau Chang, Logan Downing, Ryan Hastings, Nicholas Hinkley, Rachel Winchell.
Members of my informatics team that also supported me indirectly!
