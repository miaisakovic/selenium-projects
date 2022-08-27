# Selenium Projects
A collection of the following automation projects developed with Selenium:
1. Gather the top three travel options for going from Kitchener GO to Union Station GO at 5 pm the next day
2. Upload a new profile picture on Instagram
3. Download the latest UWaterloo Math News Article

## Table of Contents
* [Setup](#setup)
  * [For Linux](#for-linux)
  * [For MacOS](#for-macos)
  * [After Installing Initial Requirements](#after-installing-initial-requirements)
  * [Set Environment Variables](#set-environment-variables)
* [How to Use A Project](#how-to-use-a-project)

## Setup 
### For Linux
If Python has not been previously installed, run the following:
```
$ sudo apt install python3.9
$ python3.9 --version
```

### For MacOS
If Homebrew has not been previously installed, follow the instructions listed [here](https://brew.sh/).

If Python has not been previously installed, run the following:
```
$ brew install python@3.9
$ python3.9 --version
```

### After Installing Initial Requirements
If Google Chrome has not been installed on your local machine, download the Chrome installer [here](https://www.google.com/intl/en_ca/chrome/).

Clone this repository:
```
$ git clone <selenium-projects URL>
``` 
When asked to enter credentials, input your username and personal access token.

Install the required dependencies included in requirements.txt:
```
$ pip3.9 install -r requirements.txt
```

### Set Environment Variables
Create a copy of .env.template named .env:
```
$ cd selenium-projects
$ cp .env.template .env
``` 
Open the newly created file and fill in the variables:
```
INSTAGRAM_USERNAME=""
INSTAGRAM_PASSWORD=""
INSTAGRAM_PROFILE_PICTURE=""
LOCAL_FOLDER_FOR_ARTICLE=""
``` 
**INSTAGRAM_USERNAME**\
Assign your Instagram username to this variable. 

**INSTAGRAM_PASSWORD**\
Assign your Instagram password to this variable. 

**INSTAGRAM_PROFILE_PICTURE**\
Assign the absolute path to a JPEG or PNG image you would like to be your Instagram profile picture. 

**LOCAL_FOLDER_FOR_ARTICLE**\
Assign the relative path to a folder where UW Math News article(s) should be saved (this folder does not need to exist). 

## How to Use A Project
Each time you would like to use a project, run the following command:
```
$ python3.9 <relative path to one of the project files>
```
