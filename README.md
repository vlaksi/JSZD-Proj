# Sprint DSL for SCRUM

This project provides a Domain-specific language that helps to generate and prepare the sprint for the SCRUM framework.

## Overview

The idea behind this Domain-specific language is that someone can generate all user stories, tasks, and other parts of the sprint. With that, he will be able to manage and create sprints faster and in an easier way. After that, he can make some queries and see if everything seems okay for the next sprint. Besides that, users can check if some of the participants in the sprint have enough jobs and ect.

## Example

```sh
person Perica {
    position: fe_dev;
    age: 25;
}

person Jovica {
    position: fe_dev;
    age: 25;
    birthday: 1998-03-19;
}

person Bajo {
    position: fe_dev;
    age: 22;
}

person Vladislav {
    position: fe_dev;
    age: 23;
}

sprint EndGameS0 {
    description: Start & setup a project;
    startDate: 2021-03-07;
    endDate: 2021-03-21;
    minNumberOfUSPerSprint: 3;
    maxNumberOfUSPerSprint: 9;

    story Setup_NextJS {
        acceptanceCriteria: Can open & run FE project;
        description: Find on the next js documentation how to setup base project on next;
        
        estimation: 5;
        labels: FE BE QA;
        reporter: Vladislav;
        assigne: Bajo;
    }

    story Create_Readme {
        acceptanceCriteria: Readme is available;
        description: Add smth to the readme pls guys ;

        estimation: 3;
        labels: BE;

        reporter: Jovica;
    }

    story Check_endpoints {
        acceptanceCriteria: Readme is available;
        description: Add smth to the readme pls guys ;

        estimation: 3;
        labels: QA;

        reporter: Bajo;
    }
}

```

## Menu

<details>
    <summary> How to use it </summary>
    
## 1. Install virtual env

![1-install-virtual-env](https://user-images.githubusercontent.com/45834270/171293138-280ef88d-ad3b-45a9-855e-659b5fa6b8f6.gif)


## 2. Install our scrum interpreter
    
```sh
pip install git+https://github.com/vlaksi/testiranje-jszd.git
```

![2-install-scrumlang](https://user-images.githubusercontent.com/45834270/171293314-9f367d94-00cc-47ef-9c06-f9d5518d5588.gif)

## 3. Start your exapmle

![3-start-your-example](https://user-images.githubusercontent.com/45834270/171293329-2a8d9ed9-8451-477d-b975-add2c45aa936.gif)

    
## 4. Write your program & add config
    
![4-add-your-mogram-and-config](https://user-images.githubusercontent.com/45834270/171293334-ea284424-d1ba-47b0-8514-e6b636af3099.gif)

## 5. Start your program & see results

![5-start-you-example-and-see-results](https://user-images.githubusercontent.com/45834270/171293342-4646054a-122e-40ed-acb7-7847f6036408.gif)

    
</details>

<details>
 <summary> Virtual env usage </summary> 
  
## How to setup env

1. You need first to install **virtualenv**. So, open terminal **as administrator** and run

```sh
python -m virtualenv <nameOfEnv>
```

eg. create env with name jszd-env

```sh
python -m virtualenv jszd-env
```

on macOS:

```sh
virtualenv jszd-env
```

Then, in your project, you will get virtualenv where you can install all needed dependencies and etc.

![image](https://user-images.githubusercontent.com/45834270/143786245-7efc5852-c25d-4f95-98e3-d5f6eec723f9.png)

  <br/>
  
## Activate env
  
  If you are on Windows, activate (with powershell) env with 
  ```
  .\<nameOfEnv>\Scripts\activate
  ```
  ie. for our example
  
  ![image](https://user-images.githubusercontent.com/45834270/143786351-a3dc0b2c-fb2f-41a0-8ada-d7a21a3a784b.png)

And after you did that, you will have activated your virtual env, you can see name of your env next to the route of the current directory.

![image](https://user-images.githubusercontent.com/45834270/143786471-afff5acf-afac-408f-9f46-884630929198.png)

  <br/>
    
  If you are on macOS, activate env with 
   ```
   source .\<nameOfEnv>\bin\activate
  ```
  <br/>

## Deactivate env

It is a way easier then activation, you only need to type

```sh
deactivate
```

ie. for our example

![image](https://user-images.githubusercontent.com/45834270/143786524-156f1bcf-a4aa-401e-a251-2cbfea882893.png)

  <br/>

## Check env dependencies

```sh
pip list
```

ie. for our example

![image](https://user-images.githubusercontent.com/45834270/143786569-9fce8794-7c9c-44dc-a388-77c40af0578b.png)

  <br/>
  
## References

1. Setup virtual env: [link](https://www.youtube.com/watch?v=4jt9JPoIDpY)
2. Introduction to textX: [link](https://www.youtube.com/watch?v=CN2IVtInapo)

<br/><br/>

</details>
 
 
<details>
 <summary> Packages </summary>
 
 <br/>

## Install dependencies

```sh
pip install -r requirements.txt
```

## Update requirements with new dependencies

Do not forget to activate virtual env when you run this command !! (Otherwise you will update req with all dependencies from your machine !!)

```sh
pip freeze > requirements.txt
```

Eg. I installed textX (new dependencies to the env) and after that I updated requirements.

![image](https://user-images.githubusercontent.com/45834270/143787942-977afae0-39f7-4627-8cdd-fbb23df3e04b.png)

  <br/>
 
 </details>
 
 <details>
 <summary> References </summary> <br/>
 
## References
 
1. More info about project request, can be found here: [link](https://www.igordejanovic.net/courses/jsd/projekat/)
 
<br/> </details>

<details> </br>
 <summary> Dictionary </summary>
 
 - **Scrum**: Scrum is a framework within which people can address complex adaptive problems, while productively and creatively delivering products of the highest possible value.
 
<br/> </details>
 
 <details>
 <summary> External tracking systems API comunnication </summary>
    
## Test accounts that we use in this project
    gmail: malibajojszd@gmail.com
    password: malibajojszd123
    
## Trello
 Documentation: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/
    
 How to generate Key and Token:
 1. Login into your Trello Account. You can do it with gmail.
 2. Go to this link https://trello.com/app-key to get the API Key.
 3. On the same page, click on generate token to generate a token which needs to be used to get authorization for your boards, lists & cards.
 
    Key for malibajojszd: 9519ec4ca00591297f8bb4e7e184a841
   
    Token for malibajojszd: 013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82    
</details>

## Jira

Documentation: https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/

How to generate Token:

1.  Login into your Atlasian Account. You can do it with gmail.
2.  Go to this link https://id.atlassian.com/manage-profile/security/api-tokens to get the API Key.
3.  Click Create API Token, then Enter a label for you token and click Create.
4.  Click Copy to Clipboard and paste it on your script or save it in a file.

    Token for malibajojszd: Pc21zflIwX1pxv6KQTKx2B84

</details>
