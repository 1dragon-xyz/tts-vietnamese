# User story 1: 

As a user, I want to be able to know how to config the tts app as well as knowing how to use it.

Precondition: user has cloned the repo

Non-functional requirements: the app should only support cli for now.

Scenario 1:
WHEN user first open the app
THEN user see a onboarding wizard which provide a short introductions, then let user choose between: see tutorial, configure settings, destination folder, or skip the onboarding wizard

Scenario 2:
GIVEN user is at onboarding wizard
WHEN user choose to see tutorial
THEN user see a tutorial which provide a short introductions on how to use the app

Scenario 3:
GIVEN user is at onboarding wizard
WHEN user choose to configure settings
THEN user see a settings page which allows user to configure the language of the tts

Scenario 4:
GIVEN user is at onboarding wizard
WHEN user choose to skip the onboarding wizard
THEN user see the main screen of the app which allow user to choose the source file to be converted to speech

Scenario 5:
GIVEN user is at main screen
WHEN user input the source file path
THEN system confirm the source file path and ask user to confirm if he want to convert the source file to speech

Scenario 6:
GIVEN user confirmed to convert the source file to speech
WHEN system starts conversion
THEN system displays conversion progress with an estimated time to completion and shows the destination folder where the converted file will be saved

Scenario 7:
GIVEN system has finished converting the source file to speech
WHEN conversion is complete
THEN system displays a success message, presents the user with the file destination, and asks if the user wants to convert another file or exit


