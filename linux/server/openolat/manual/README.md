# Creating Courses, Tests in OpenOLAT

## Importing Questions

Format:
```
type	MC
Title	Cyber Security Training
Question	Which of the following are considered 'sensitive personal data' under the Data Protection Act 2019?
Points	10
2.5 	Health status
2.5 	Ethnic social origin
2.5 	Genetic data
2.5 	Biometric data
-2.5	Name and address
-2.5  	Email address

type	SC
Title	Cyber Security Training
Question	A data controller must ensure personal data is kept for no longer than is ________ for the purposes for which it was collected.
Points	10
10	Necessary
0	Convenient
0	Economical
0	Indefinite
```

Explanation:
- First question:
  - The question type is MC - [Multi-choice](https://docs.openolat.org/manual_user/learningresources/Test_question_types/#mc)
  - Maximum points for this question are: 10 points
  - Correct choices are the first 4 choices indicated by the corresponding `2.5` i.e. each correct choice earns partial credit.
  - Wrong choices are the last two indicated by the corresponding `-2.5`i.e. choosing a wrong answer deducts 2.5 points.
- Second question:
    - The question type is MC - [Single-choice](https://docs.openolat.org/manual_user/learningresources/Test_question_types/#sc)
    - Maximum points for this question are: 10 points
    - Correct choices are the first 4 choices indicated by the corresponding `1`.
    - Wrong choices are the last two indicated by the corresponding `0`.

## Creating a Course/Test
- Authoring
- Create a Course or Test (if just a test from Question Bank)

## Editing an Existing Test
- To access Course level settings for a Test:
  - Select the Test or Course
  - Under `Administration` menu, select `Settings`
  - Select `Share` tab
  - Ensure the:
    - `Usage` is set to a `Standalone`.
    - `Access for participants` is set to `Private Member management by administration`.
- Select `Options` tab to access or change top-level settings for a test e.g.
  - Attempts
  - Showing results
  - Showing answers
  Proceed as follows:
  - Click on "Courses"
  - Select the test.
  - Click on `Start Test`
  - Under the `Administration` menu, select `Settings`
  - Navigate to the `Options tab`
  - Make the changes
  - Save
- To indicate questions that will feature in the test i.e. edit content of the test, select `Edit Content`:
  - Ensure it has a `Section` part. If it has one, click on `+Add Elements` menu, select `Test Part`. 
  - If it has a `Section` but no questions, also click on `+Add Elements` and select `Import questions from pool` (It's recommended you create a pool of Questions in the `Question bank` section)
    - Select the questions you want to import from your `Question bank`
    - At the bottom click the button `Select`
- Randomize a number of questions e.g. you have imported 30 questions but any given quiz attempt will only feature 15 from that pool.
  - Select the `Section`
  - Set the following features:
    - `Random order of questions or sections?` to `Yes`
    - `Number of questions in this section` to `15`
    - Save
- Change scoring:
  - Select the test (title of the Quiz)
  - From there you can change
    - Passed cut value
    - Set a time limit
  - Save

## Adding Participants to a Test
Steps:
- Ensure users have already been imported
- Select the Test or Course
- Under `Administration` menu, select `Members management`
- Click on `+Add member`
- Select `Bulk search`
- Copy and paste the usernames (one on each line) it can either be usernames or email or organizations.
- Ensure `E-mail notification` is false or off.
- Finish

## View Test Results
Steps:
- Ensure users have already been imported
- Select the Test or Course
- Under `Administration` menu, select `Assessment tool`
