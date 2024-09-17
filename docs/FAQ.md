# FAQ

## Frequently Asked Questions

### How do I get this running?

(assuming python3 is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
git clone https://github.com/reactive-firewall/multicast.git multicast
cd ./multicast
git checkout stable
# make clean ; make test ; make clean ;
make install ;
python3 -m multicast --help ;
```
#### DONE

If all went well `multicast` is now installed and working :tada:


### How do I use this to receive some UDP Multicast?

(assuming project is setup and installed and you want to listen on 0.0.0.0)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast HEAR --use-std --port 59595 --join-mcast-groups 224.0.0.1 --bind-group 224.0.0.1
```

Caveat: RCEV is much more usefull if actually used in a loop like:

```bash
# cd /MY-AWSOME-DEV-PATH
while true ; do # unitl user ctl+c inturupts
python3 -m multicast RECV --use-std --port 59595 --join-mcast-groups 224.0.0.1 --bind-group 224.0.0.1
done
```


### How do I use this to send UDP Multicast?

(assuming project is setup and installed)

```bash
# cd /MY-AWSOME-DEV-PATH
python3 -m multicast SAY --mcast-group 224.1.1.2 --port 59595 --message "Hello World!"
```


### What is the basic API via python (instead of bash like above):

#### Caveat: this module is still a BETA
[Here is how it is tested right now](https://github.com/reactive-firewall/multicast/blob/cdd577549c0bf7c2bcf85d1b857c86135778a9ed/tests/test_usage.py#L251-L554)

```python3
import mulicast as mulicast
from multiprocessing import Process as Process

# setup some stuff
_fixture_PORT_arg = int(59595)
_fixture_mcast_GRP_arg = """224.0.0.1"""  # only use dotted notation for multicast group addresses
_fixture_host_BIND_arg
_fixture_HEAR_args = [
	"""--port""", _fixture_PORT_arg,
	"""--join-mcast-groups""", _fixture_mcast_GRP_arg,
	"""--bind-group""", _fixture_mcast_GRP_arg"
]

# spwan a listening proc

def inputHandle()
	buffer_string = str("""""")
	buffer_string += multicast.recv.hearstep([_fixture_mcast_GRP_arg], _fixture_PORT_arg, _fixture_host_BIND_arg, _fixture_mcast_GRP_arg)
	return buffer_string

def printLoopStub(func):
	for i in range( 0, 5 ):
		print( str( func() ) )

p = Process(
				target=multicast.__main__.McastDispatch().doStep,
				name="HEAR", args=("HEAR", _fixture_HEAR_args,)
			)
p.start()

# ... probably will return with nothing outside a handler function in a loop
```
and elsewhere (like another function or even module) for the sender:
```python3

# assuming already did 'import mulicast as mulicast'

_fixture_SAY_args = [
	"""--port""", _fixture_PORT_arg,
	"""--mcast-group""", _fixture_mcast_GRP_arg,
	"""--message""", """'test message'"""
]
try:
	multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
	# Hint: use a loop to repeat or different arguments to varry message.
except Exception:
	p.join()
	raise RuntimeException("multicast seems to have failed, blah, blah")

# clean up some stuff
p.join() # if not already handled don't forget to join the process and other overhead
didWork = (int(p.exitcode) <= int(0)) # if you use a loop and need to know the exit code

```
#### Caveat: the above examples assume the reader is knowledgeable about general `IPC` theory and the standard python `multiprocessing` module and its use.


### What are the defaults?

#### The default multicast group address is 224.0.0.1

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L185-L187):
> The Value of "224.0.0.1" is chosen as a default multicast group as per RFC-5771
> on the rational that this group address will be treated as a local-net multicast
> (caveat: one should use link-local for ipv6)

#### The default multicast Time-to-Live (TTL) is 1

From [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1)
> ... If the
> upper-layer protocol chooses not to specify a time-to-live, it should
> default to 1 for all multicast IP datagrams, so that an explicit
> choice is required to multicast beyond a single network.

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L214-L217):
> A Value of 1 (one TTL) is chosen as per [RFC-1112 §6.1](https://www.rfc-editor.org/rfc/rfc1112#section-6.1) on the rational that an
> explicit value that could traverse byond the local connected network should be
> chosen by the caller rather than the default vaule. This is inline with the principle
> of none, one or many.

#### The default multicast destination port is 59559

From the [documentation](https://github.com/reactive-firewall/multicast/blob/v1.4/multicast/__init__.py#L155):
> Arbitrary port to use by default, though any dynamic and free port would work.

> :exclamation: Caution: it is best to specify the port in use at this time as the default has yet to be properly assigned ( see related reactive-firewall/multicast#62 )


### What does exit code _x_ mean?

#### Python function return code meanings

`0` is the default and implies *success*, and means the process has essentially (or actually) returned nothing (or `None`)

`1` is used when a *single* result is returned (caveat: functions may return a single `tuple` instead of `None` to indicate exit code `1` by returning a `boolean` success value, and result (which may also be encapsulated as an iteratable if needed) )

`2` is used to indicate a *value and reason* are returned (caveat: functions may return a single `tuple` with a single value and reason and the value can be a `tuple`)

`-1` is used to mean *many* of unspecified length and otherwise functions as `1`

#### CLI exit code meanings

`0` *success*

`1` *none-sucsess* - and is often accompanied by warnings or errors

`2 >` *failure* of specific reason


#### Everything Else
_(extra exit code meanings)_

Other codes (such as `126`) may or may not have meanings (such as skip) but are not handled within the scope of the Multicast Project at this time.