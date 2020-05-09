<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/abhimanoj/NewsFeed/">
    <img src="images/logo.jpeg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">News Feed</h3>
  <p align="center">
    <pre>This app is used for getting daily news based on topic.</pre>
    <br />
    <a href="https://gitlabcom/abhimanoj/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://gitlabcom/abhimanoj/">View Demo</a>
    ·
    <a href="https://github.com/abhimanoj/NewsFeed/issues">Report Bug</a>
    ·
    <a href="https://github.com/abhimanoj/NewsFeed/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Push and Pull the code](#Push&Pull)
* [Contact](#contact) 



<!-- ABOUT THE PROJECT -->
## About The Project

[![News Feed Tool Screen Shot][product-screenshot]](https://www.limbictechnologies.com)

We’re creating a new solution in order to news feed in bulk instead of doing it one per one.
The goal isn’t to do a “quick and dirty” news feed process, but to help news feed operators to
send targeted message by type of need or type of business.
The first version of the solution will gather information from the public marketplace in order to
gather projects request and allow our team to define proposals in bulk for them.
First marketplace will be bing.com, as they propose an API.


### Built With
  
* [JQuery](https://jquery.com)
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)



<!-- GETTING STARTED -->
## Getting Started

# Clone secrets and fablib repositories
git clone https://github.com/abhimanoj/NewsFeed.git 

# Change into project directory
cd <project_name>

# Make virtual environment
mkvirtualenv <project_name>

# Activate virtual environment
workon <project_name>

# Install requirements
pip install -r requirements.txt

# Setup (if necessary)
fab loc setup

# Start the development server
python manage.py runserver

### Prerequisites

Install requirements
* Python
```sh
python3
django==2.2.1
```

### Installation
 
1. Clone the repo
```sh
git clone https://github.com/abhimanoj/NewsFeed.git
```
2. Install pip packages
```sh
pip install -r requirements.txt
```
3. Start the development server (Run command)
```sh
python manage.py runserver
```
4. Run unit test command
```sh
python -Wall manage.py test
```


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/abhimanoj/NewsFeed/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Push&Pull

1. Clone the Project
2. Create your developer Branch (`git checkout -b develop`)
3. Commit your Changes (`git commit -m 'Add some changes in develop'`)
4. Push to the Branch (`git push origin develop`)
5. Open a Pull Request

<!-- CONTACT -->
## Contact

Abhimanoj Yadav - [@twitter_handle](https://twitter.com/abhimanoz) - email

Project Link: [https://github.com/abhimanoj/NewsFeed](https://github.com/abhimanoj/NewsFeed/issues)



<!-- MARKDOWN LINKS & IMAGES --> 
[product-screenshot]: images/screenshot.png




## Set time interval  
1. schedule.every(10).minutes.do(job)
2. schedule.every().hour.do(job)
3. schedule.every().day.at("10:30").do(job)
4. schedule.every(5).to(10).minutes.do(job)
5. schedule.every().monday.do(job)
6. schedule.every().wednesday.at("13:15").do(job)
7. schedule.every().minute.at(":17").do(job)
