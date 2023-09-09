# Swagbucks daily reward automatizer tool

## Purpose

This project was created for you to be able to automatize completing the daily rewards on [Swagbucks](https://www.swagbucks.com).

## Setup

You need to create a file named `user_config.yaml` containing the following information:

- `email`: the email associated with your account
- `password`: the password to your account

You also need to have [Python](https://www.python.com) and [Selenium](https://selenium-python.readthedocs.io/index.html) installed.

## Automatization

In order to completely automatize the process, you need a cron job (on Linux) to do the task in the background for you. You can use [Crontab](https://crontab.guru/), I've included a shell script for you to run in the cron job. You can view the logs in the `log.txt` file.

## Running the shell script

`./run.sh ${your_path_to_python_file}`
