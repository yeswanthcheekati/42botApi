# API.AI - sample webhook implementation in Python

This is a webhook implementation that gets API.AI query response and returns a corresponding response by scraping the necessary data from the 42hertz website.

The app has been deployed to heroku. API.AI accepts only public urls, so local hosts will not be supported The data flows as:

#### API.AI   ->    heroku webhook url(post)    ->    app functions(processing)   ->    heroku webhook url(post)    ->    API.AI 

The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.

