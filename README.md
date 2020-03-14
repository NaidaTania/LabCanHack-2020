# Nurse Watson - Backend

A video demo of the product can be found [here](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9b099f4b-41d3-440f-8c88-02fb714c824b/Our_Video_2.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAT73L2G45HQA7JC73%2F20200314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200314T075211Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEG4aCXVzLXdlc3QtMiJHMEUCIQDY%2BoBjWT0vmcSy1zC6U8WU3bs6EAB1gs0GEKb0dShcxwIgDipZWVxS3ZDA%2BV7l0sKRhb2ORayQTZZH03j%2BWsP1Sy4qtAMIVxAAGgwyNzQ1NjcxNDkzNzAiDKAFeis1WV6f3fjQ2CqRA%2FPNwykQvuszt%2BlDhdrJswGUNBxI29AG5vGe%2F3xP9CvG7KmnAQmhw8lMLZD17qu2yKWl1GDSxMOTNloTyxyCa7q%2FrooL5qoFkUN%2Bp5mqaQ%2Bi7kFW8dRDmhN67J4TnvQmXdUlai1QQdHCeoV%2FHtfNIEANnktzQE8PZK2t7%2FGaPTgy8kpU8jXtg61AxN5rICQ7s40nf232JXvyZ3yveeUma30YIDh4kwPtbT1vVW6ITyHvrZ5xKP%2BaSRNzRY9Wd6J2wtxqq%2BqS7U0DQutVHpnX9KyJWntmg9rKiTfHAydiLhZ2SgilVhKln6gS9oCkQBoRuBXaO380zMLcf7e6RB3paoRDC7l1vXJ%2BlnCkKnNee1ix7DIA89p%2FMLYMJRwVi7j7SaPfqItkWY7UWzn%2FUBGfIso0C%2F9xsa%2BCZ8wDdkuR%2FElnFgFnV5IxcmOORlTXhKnoEii913DyWe6fwy6l52KfUUJPBFFSS4spZn8nTROvB5MlmV1XuscGRaMbeuC6%2Fo6KKngyrrkEsIigCu1CmtdSPVSDMKTksfMFOusBx6lJOr3C0Uw34MSgnXrEnLCT3N5oxYw71z2clvtpNQvGcoug91oL4sb5CWCQLc%2FkFryEX4zBFwn4YJK6aDDRmPL46G9FN95NidFHISFZ3zmsjihpBO6GUtNzIEkvneRb%2Bc2XE6fChDZfXCqCbmgVMn8oPQlY3WtYR3vV%2BzgdvWyR7nfcuMwLxhtPME3maB%2BXQOwREYJ5MC4nKBhdYavC49ETTVmKQleWAgVzyraGySMluGjb%2FTqDubQ8Zue78a0VsWzW0qYVK2M6jtrCnW89yxjve97ZzBEnrJOQs%2B2lg7XwrHbeaSssUWGkXA%3D%3D&X-Amz-Signature=b82a72dc04df8a159fd0bfa531b363f7ef5a2e2736c57e19c01990d68b5e5a20&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Our_Video_2.mp4%22)  

# Endpoints:
## /symptoms
**POST**:
- Input: the user description of their health problem
```
{
	"uid" : "1234xxxx",
	"text" : "I have a headache",
	"suggestions" : []
}
```
- Output: A list of possible medically worded symptoms
```
{
  "uid" : "1234xxxx",
  "suggestions": [
        [
            "Headache",
            "Headache after trauma",
            "Headache and weakness",
            "Confusion and headache"
        ],
        [
            "Neck ache or pain",
            "Shoulder ache or pain"
        ]
    ]
}

```

## /predict
**POST**:
- Input: A list of the symptoms that the user has confirmed
```
{
	"uid" : "1234xxxx",
	"text" : "I have a headache",
	"suggestions" : ["Headache after trauma","Neck ache or pain"]
}

```
- Output: A list of other symptoms related to possible diagnoses to be recommended to user based on Apriori Algorithm
```
{
    "uid": "1234xxxx",
    "text": "You may experience these commonly related symptoms?",
    "suggestions": [
        "Unsteady gait (Trouble walking)",
        "Vertigo (Room spinning)",
        "Loss of balance",
        "Headache and weakness"
    ]
}

```


## /diagnosis
- Input: A list of the symptoms that the user has confirmed
```
{
	"uid" : "1234xxxx",
	"text" : "I have a headache",
	"suggestions" : ["Headache after trauma","Neck ache or pain","Loss of balance"]
}

```
- Output: A list of diagnoses and the percentage confidence based on the matching symptoms from the dataset
```
{
    "uid": "1234xxxx",
    "text": "Your possible diagnosis based on percentage of symptoms",
    "diagnosis": {
        "Vertebral artery dissection:neck artery tear": "33%"
    }
}

```

Dataset used: https://www.kaggle.com/plarmuseau/sdsort#diagn_title.csv
