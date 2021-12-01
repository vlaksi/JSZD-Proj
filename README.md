# Sprint DSL for SCRUM

This project provides a Domain-specific language that helps to generate and prepare the sprint for the SCRUM framework. 

## Overview

The idea behind this Domain-specific language is that someone can generate all user stories, tasks, and other parts of the sprint. With that, he will be able to manage and create sprints faster and in an easier way. After that, he can make some queries and see if everything seems okay for the next sprint. Besides that, users can check if some of the participants in the sprint have enough jobs and ect.


## Menu

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
  Then, in your project, you will get virtualenv where you can install all needed dependencies and etc.  
  
  ![image](https://user-images.githubusercontent.com/45834270/143786245-7efc5852-c25d-4f95-98e3-d5f6eec723f9.png)

  <br/>
  
## Activate env
  
  If you are on Windows(if you are on Mac, try bin instead of the Scripts), activate env with 
  ```
  .\<nameOfEnv>\Scripts\activate
  ```
  ie. for our example
  
  ![image](https://user-images.githubusercontent.com/45834270/143786351-a3dc0b2c-fb2f-41a0-8ada-d7a21a3a784b.png)

  And after you did that, you will have activated your virtual env, you can see name of your env next to the route of the current directory.
  
  ![image](https://user-images.githubusercontent.com/45834270/143786471-afff5acf-afac-408f-9f46-884630929198.png)
  
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

 <br/>
 
 
