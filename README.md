# Bjumper Backend Test

## Table of Contents
1. [Summary](#summary)
2. [Requirements](#requirements)
    - [Notes](#notes)
3. [Instructions](#instructions)
4. [Evaluation Criteria](#evaluation-criteria)
5. [Submission](#submission)

## Summary

This test is designed to evaluate the skills of backend candidates with a focus on Python and Django. The goal is to create an app that backs up repositories using the [GitHub API](https://docs.github.com/en/rest) and saves them in a separate database.

## Requirements

The app must be able to handle the following logic from an API using HTTP requests:
* **Fetch users**: The endpoint must fetch the user information and display some of it in our API.
   * Input: username
   * Response: the information about the selected user if it exists in our DB and all the repositories linked to it.
* **Backup user**:
   * Input: username
   * Behaviour: If the user exists on **GitHub**, it must store a "backup" user in the DB with the following information:
     * Username
     * GitHub URL
* **Delete user backup**:
  * Input: username
  * Behaviour: The selected user "backup" must be deleted from our DB, along with the linked repositories.
* **Backup repository**:
   * Input: repository URL (GitHub URL) and username
   * Behaviour: The repository is stored in our DB as a "backup" **only if the user exists in our DB**. It must validate that the username owns the repository on GitHub before creating the backup. The "backup" of the repository must store the following information:
     * Owner user
     * GitHub Repository URL
     * Repository name
* **Delete repository**:
   * Input: repository URL
   * Behaviour: The repository "backup" is deleted from our DB if it exists.

### Notes:
* We do not expect an actual backup of the repository, just a few fields. The goal of the exercise is to evaluate how candidates interact with APIs and databases.
* The goal of the exercise is not to spend more than 2 or 3 hours on it. If there is anything missing after that time, feel free to explain what's missing in the submission email.
* The use of libraries is encouraged; we don't expect candidates to reinvent the wheel.
* Feel free to use Django and Django REST Framework.
* We encourage the use of PostgreSQL for the database, but it is not mandatory.

## Instructions

Candidates are required to:

1. Create a new **private** repository on GitHub named `Bjumper_Backend_Test`.
2. Develop a web application that enables searching GitHub users. While the primary focus is on Python, candidates may use Django or any other Python framework.
3. Upload the solution to the created repository.

## Evaluation Criteria

We value quality over quantity. When reviewing your submission, we will consider the following:

- **Functionality**: The application should work as expected and handle different scenarios gracefully.
- **Code Quality**: Well-structured, readable, and maintainable code.
- **User Experience**: Though not the primary focus, a clean and user-friendly API is highly valued.
- **Documentation**: Clear instructions on how to set up and run your project and use the API are essential.
- **Best Practices**: Compliance with industry standards and best practices in coding and security.

## Submission

Once you have completed the exercise, please send an email with the link to your private repository to salcazar@bjumper.com. Remember to provide temporary access to the repository.

We appreciate your effort and time in participating in this test and look forward to reviewing your submission!
