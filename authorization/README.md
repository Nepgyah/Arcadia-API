# Authorization App
Contains views and logic to login via admin or through d2x authentication and handles the generation of JWTs

## Dev note for graphene validation 
With the current graphql set up, the only specification to why a url failed is throught the response key as accessed below
```
response['errors']['messages'][0]
```

We are currently looking up how to edit the errors and append the response code and detail. But until further notice, **frontends will have the responsibility to verify whether or not the jwt token has expired and fresh via our fresh endpoints**. A invalid token simply results in the data of that specific resolver to be None or Null.