## This is Machine Learning Project 

### Software and account Requirement.
    
    
###    1. [Github Account](https://github.com/)
###    2. [Heroku Account](https://id.heroku.com/login)
###    3. [VS Code IDE](https://code.visualstudio.com/)
###    4. [GIT cli](https://git-scm.com/downloads)   
###    5. [GIT Documentation](https://git-scm.com/docs/gittutorial)
###    6. [GITHUN Action](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)


### Creating Conda Environment

```
      1. Configure conda environment in environment variables if its not already configured
```

```
      2. conda create -p <env_name> python=3.7 -y
```

```
      3. conda activate venv/

```

```
      4. create requirements.txt and start adding required dependencies of project in it and execute this file
          To Exceute this file use command as below

          pip install -r requirements.txt
```

```
      5. create app.py file
```

```
      6. to add files to git

            git add .
            git add filename
            git add filename1 filename2
```

      7. To check versions maintained by git

```
            git log
```

      8. To check the status of git

```
            git status
```

#### Note : To ignoew file/folders we could add those details inside git.ignore


```
      9. To create version/commit all changes by git


            git commit -m "message"
```


```
      10.   To send version / changes to git hub

            git push origin main

            origin is a variable which consists git url https://github.com/vaibhavyaramwar/Machine_Learning_Project.git

            to check the value of origin run below command

            git remote -v
```

```

            To check remote url 

                  git remote -v
```

```
            Revert git commit

                  git revert <commit to revert>

```

```
      To setup CICD pipline in Heroku we need 3 Information

            1. HEROKU_EMAIL = vaibhav.yaramwar@gmail.com
            2. HEROKU_API_KEY = 
            3. HEROKU_API_NAME = ml-cicd-test

```

```
      create dockerfile : name of file should be Dockerfile
      create .dockerignore file
```

      BUILD DOCKER IMAGE

```
      docker build -t <image_name>:<tagname> .
```

Note : name of image always be in lower case


To List Docker Image

```
      docker images

```

Run Docker Image

```
      docker run -p 5000:5000 -e PORT=5000 da5758f1ab10
```

To check running container in docker

```
      docker ps
```

To Stop Docker Container

```
      docker stop <container_id>
```

```
      python setup.py install
```


#### The below command will look for all the local packages and build the local packages

```
      pip install -e .
```

```
    Create below packages under housing package

      housing/component/__init__.p
      housing/config/__init__.py
      housing/entity/__init__.py
      housing/exception/__init__.p
      housing/logger/__init__.py
      housing/pipeline/__init__.py
```

install ipykernal

```
      pip install ipykernal
```

