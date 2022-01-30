# USED CARS PRICE PREDICTION
This repo contains all the source code and obtained data for the used cars prices prediction model
## Purpose of this projects
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Hyprnx/used-cars-prices-prediction">
    <img src="README_resource/Vector.png" alt="Logo" width="900" height="400">
  </a>

  <h3 align="center">USED CARS PRICE PREDICTION</h3>
</div>

The global used cars market was estimated at $828.24 billion in 2019 and is projected to reach $1,355.15 billion
by 2027. In Vietnam, Used Car market in terms of sales volume increased at a double digit CAGR over the review period
2013-2018. The market was observed to be at the early growth stage owing to the faster vehicle replacement rate,
reduction in new car launch time, growing middle class population, increasing average ticket size and reduction in
import duty on new cars. In Vietnam, people prefer to buy a used car as new ones are expensive and for middle or lower
income group people, used cars have become more popular choices. Vietnamese government is expecting new policies that
ban motorbikes in the urban area so that the demand for used cars is expected to rocket.

Due to the increasing demand for used cars in Vietnam, we have built a prediction model to predict used cars' prices
to make it easier for Vietnamese to purchase cars.


## Authors
- [@Nguyen Thanh Tuan](https://github.com/nttuan8) - Director of DSLab
- [@To Duc Anh](https://github.com/hyprnx) - DSLab member
- [@Tran Minh Khoa](https://github.com/khoa2181) - DSEB member
- [@Duong Thu Phuong](https://github.com/dtphuong2612) - DSEB member
- [@Nguyen Anh Tu](https://github.com/tunachiu) - DSLab member
- [@Kieu Son Tung](https://github.com/nttuan8) - DSEB member
- [@Nguyen Son Tung](https://github.com/209sontung) - DSLab member


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

