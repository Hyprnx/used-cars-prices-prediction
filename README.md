# USED CARS PRICE PREDICTION
<div id="top"></div>
This repo contains all the source code and obtained data for the used cars prices prediction model

## Purpose of this projects
<!-- PROJECT LOGO -->
<br/>
<div align="center">
  <a href="https://github.com/Hyprnx/used-cars-prices-prediction">
    <img src="README_resource/Vector.png" alt="Logo" width="85%">
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

<br/>

## Authors
- [Nguyen Thanh Tuan](https://github.com/nttuan8) - Director of DSLab
- [To Duc Anh](https://github.com/hyprnx) - DSLab member
- [Tran Minh Khoa](https://github.com/khoa2181) - DSEB member
- [Duong Thu Phuong](https://github.com/dtphuong2612) - DSEB member
- [Nguyen Anh Tu](https://github.com/tunachiu) - DSLab member
- [Kieu Son Tung](https://github.com/nttuan8) - DSEB member
- [Nguyen Son Tung](https://github.com/209sontung) - DSLab member
<p align="right">(<a href="#top">back to top</a>)</p>

<br/>

## The process

### The Data making
To make the model best fit with Vietnamese market, we have search for top e-commerce websites that sell used cars to
crawl selling post of that sites.

### Getting the required fields
Since data have a lot of missing fields because each e-commerce site has different data field information, we have also
scrape <a href = https://www.auto-data.net>autodata.net</a> to fill in the missing fields. We will leave the crawled 
data and crawler open source, if anyone is interested, you can use it for free of charge, no permission required.

Since finding and matching cars takes too many time, we decided to build a Machine Learning model to predict and fill
in the missing fields with precision of 99.2%.
<p align="right">(<a href="#top">back to top</a>)</p>

<br/>

## About crawlers

### The process
We mainly use requests and beautifulsoup package in Python to send requests and extract information. Sometimes,
the protection to prevent DoS attack stop us from scraping the website, therefore, we have to simulate user activities 
using Selenium

### About Selenium
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which
needs to be installed before the below examples can be run.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException:
Message: ‘geckodriver’ executable needs to be in PATH.

The crawling mechanism requires selenium, which mean you need specific version of browser to work with,
<b><u>we use Chrome</u></b> the details version is listed below:

 - Chrome === 98
 - Other browser version will be supported later.

We included a webdriver in the repo itself, but if you want you can change to use the webdriver of your choice:


#### Changing webdriver path:
If you want to change the webdriver path, go to common/check_os, there is a function called: 
get_selenium_chrome_webdriver_path with a variable called defined_path, change it to your desired path to the
chromewebriver in your machine

<p align="right">(<a href="#top">back to top</a>)</p>

<br/>

## Getting Started
Open Terminal / cmd and do the following:
### Create and activate virtual environment
#### Create
 ```sh
  python -m venv <envname>
  ```

#### Activate

- On Mac:
  ```sh
  source <envname>/bin/activate
  ```
- On Windows:
  ```sh
  <envname>\Scripts\activate
  ```

### Install requirements.txt
  ```sh
  pip install -r requirement.txt
  ```
<p align="right">(<a href="#top">back to top</a>)</p>


### Start using the model
We included our crawled data, but if you want to crawl the newest data, do the following

#### Re-crawl the data
Head to [crawl.py](crawlers/crawl.py) and run it

<u><b>Disclaimer</b></u>: Due to the update of the website or changing website structure, some crawlers might not work

#### Using the model:
If you want to re train the model, you can head to the notebook and choose run all to get the model results.

<p align="right">(<a href="#top">back to top</a>)</p>

<br/>

## License
Distributed under the GNU General Public License v3.0 License. See `LICENSE.txt` for more information.
<p align="right">(<a href="#top">back to top</a>)</p>

<br/>

## Contact us
[To Duc Anh](mailto:toducanh2001@gmail.com)

[Tran Minh Khoa](mailto:khoatran2181@gmail.com)

[Duong Thi Thu Phuong](mailto:duongthithuphuong26122001@gmail.com)

[Kieu Son Tung](mailto:sontungkieu412@gmail.com)

Project Link: [Used cars prediction](https://github.com/Hyprnx/used-cars-prices-prediction)

<p align="right">(<a href="#top">back to top</a>)</p>


