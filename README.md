# Final Grade Calculator - The Open University

## Explanation 
Calculating the final grade of a course at the Open University takes into account not only the exam grade but also the assignment grades, with each assignment having a different weight, making the final grade calculation complex.

## What does the bot include? 
![Project Logo](media/start_conversion.PNG)

### Final Grade Calculation 
When you select this option, you need to enter the assignment grades and their weights, as well as your exam grade. The bot will calculate and display your final course grade.

### Minimum Exam Grade Calculation 
When you select this option, you need to enter the assignment grades and their weights, and your desired final grade. The bot will calculate and display the **minimum exam grade** you need to achieve in order to get your desired course grade.

## Assignment Weights 
In every course booklet (where the assignments and guidelines are listed), there is a table with the weight descriptions:
![Project Logo](media/tasks_weight.PNG)
Additionally, at the top of each assignment, the assignment weight is noted:
![Project Logo](media/single_task_weight.PNG)

## Demo

![Project Logo](media/demo.gif)

## Running the Bot

### Running on Console
1. Create a token using [this guide](https://core.telegram.org/bots#how-do-i-create-a-bot).
2. Set the environment variable `BOT_TOKEN`:
    ```bash
    export BOT_TOKEN='your_token_here'
    ```
3. Run the bot with:
    ```bash
    python main.py
    ```

### Running with Docker
1. Create a token using [this guide](https://core.telegram.org/bots#how-do-i-create-a-bot).
2. Edit the `Dockerfile` to include your token. Add the following line:
    ```dockerfile
    ENV BOT_TOKEN='your_token_here'
    ```
3. Build the Docker image:
    ```bash
    docker build -t final-grade-calculator .
    ```
4. Run the Docker container:
    ```bash
    docker run -d --name final-grade-calculator final-grade-calculator
    ```

With these steps, you can choose to run the bot either directly on your console or within a Docker container, depending on your preference.
