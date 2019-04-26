# Google Maps
Writing automatic tests for Google Maps Website
                                                                                                    
# Testing Google Maps web application with Selenium

The goal of the QA task is to create an automation test that will test Google Maps web application. Our recommendation is to use Selenium webdriver.

1. The first step in auto test should be fast checking if maps.google.com is up.

2. Test should check if “direction” feature works properly when the user wants to go from Budapest to Belgrade by car, but skipping the highways and driving the longest route from the offered routes.

3. At the end, test checks if distance and time duration are present on details page.

## Getting started

In this project is used:
1. Python version 3.6.5
2. Google Chrome version 74.0.3729.108
3. Selenium version 3.141.0
4. Chrome Driver version 74.0.3729.6 downloaded from [here](https://chromedriver.storage.googleapis.com/index.html?path=74.0.3729.6/)

# Tasks

## First

For the first task, we are checking is Google maps website returning 200 as HTTP status code
There are two methods for checking HTTP status code.

In the method `get_http_status_selenium` we are checking HTTP status code with Selenium, and in the `get_http_status_requests` we are using Python library requests.

Both of them can be used in `is_google_maps_up` for checking is website up and will return the same result, and in this example `get_http_status_requests`is used. 

We are logging the message in both cases. Here is the log we get when site is up:
```
2019-04-26 21:06:23,549    INFO    Google maps site is up and running.
```

## Second

In the second task, we are automatically testing choosing the longest route from Budapest to Belgrade, with avoiding highways and displaying distance in kilometers, and displaying details page for the choosen route.

So, step by step we are entering start and end point of the route, choosing car as a vehicle and choosing option for avoiding higways and displaying distance in kilometers.

We are displaying logs for all the actions:
```
2019-04-26 21:06:26,071    INFO    Going to page for choosing directions
2019-04-26 21:06:33,869    INFO    Starting point is Budapest
2019-04-26 21:06:36,281    INFO    Destination is Belgrade
2019-04-26 21:06:37,110    INFO    Choosing directions for a car
2019-04-26 21:06:37,750    INFO    Clicking options
2019-04-26 21:06:38,101    INFO    Checking option for avoiding highways
2019-04-26 21:06:38,563    INFO    Checking option for displaying distance in kilometers

```
After that we are looking for the longest route.
So, here we are making the list contained of all the routes we got, and choosing the maximum distance by using max() method from Python.
We are clicking twice on the longest route, as the first click only shows us warnings about the route, and the second one is opening the details page.
We are also logging this steps:
```
2019-04-26 21:06:44,815    INFO    First click is showing warnings
2019-04-26 21:06:45,219    INFO    Second click is showing details page
2019-04-26 21:06:45,470    INFO    Longest route: 394 km
```
Longest route is also displayed.

## Third

The third task is to check are time and distance present on the details page.
So, this test is done after the second one, as we need to go through the steps from the second one to get to the details page.
There is an private method `__are_time_and_distance_present` for checking this requirements, which we call at the end of the second `check_path` method.
This method returns True or False value and can be called with passing True or False argument

We are also logging if elements are present. If they are, here is the log we get:
```
2019-04-26 21:06:50,296    INFO    Time and distance are present on the details page

```

### Author
Jana Đurović
