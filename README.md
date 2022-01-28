# USED CARS PRICE PREDICTION
This repo contains all the source code and obtained data for the used cars prices prediction model

## About crawlers
### About Selenium
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which
needs to be installed before the below examples can be run.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException:
Message: ‘geckodriver’ executable needs to be in PATH.

The crawling mechanism requires selenium, which mean you need specific version of browser to work with,
<b><u>we use Chrome</u></b> the details version is listed below:

 - Chrome === 98
 - Other browser version will be supported later.

We included a webdriver in the repo itself, but if you want you can change to use the webdriver of your choice.
#### Changing webdriver path:
If you want to change the webdriver path, go to common/check_os, there is a function called: 
get_selenium_chrome_webdriver_path with a variable called defined_path, change it to your desired path to the
chromewebriver in your machine

