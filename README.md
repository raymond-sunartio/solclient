# solclient

Python solclient interface. It uses ctypes to interact with solclient C API. It exposes only a subset of the solclient C API. User should be able to subscribe to particular topic and receive messages sent on that topic.

For more information of solclient C API, please visit: https://docs.solace.com/API-Developer-Online-Ref-Documentation/c/index.html

### Using kerberos authentication

To use kerberos authentication, set the following session properties when creating a session:

```python
    sessionProps = {
        ... 
        solClient.SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME: 'AUTHENTICATION_SCHEME_GSS_KRB',
        solClient.SOLCLIENT_SESSION_PROP_KRB_SERVICE_NAME: 'YOUR_KERBEROS_SERVICE_NAME',
        ...
    }
    
    ...
    
    solClient.solClient_session_create(
        sessionProps,
        context_p,
        session_p,
        sessionFuncInfo
    )
```

To use custom kerberos config:


To run the script using kerberos authentication:


For more information on how to use keytab for kerberos authentication, please visit: https://kb.iu.edu/d/aumh
