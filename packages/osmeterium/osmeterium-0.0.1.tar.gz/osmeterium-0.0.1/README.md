# OSMeterium
> The osmeterium is a defensive organ found in all papilionid larvae, in all stages. 

## Usage
### Async
```py
t = run_command_async('ping -c www.google.com',
        (lambda x: print('Hey this stdout output {0}'.format(x))),
        (lambda x: print('Hey this strerr output {0}'.format(x))),
        (lambda y: print('This is exit code ${0}'.format(y))),
        (lambda: print('Command success'))) #  return a Thread Object
t.join()
```
### Sync
```py
t = run_command('ping -c www.google.com',
        (lambda x: print('Hey this stdout output {0}'.format(x))),
        (lambda x: print('Hey this strerr output {0}'.format(x))),
        (lambda y: print('This is exit code ${0}'.format(y))),
        (lambda: print('Command success')))
```
