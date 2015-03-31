# repocket

A simple rule-based processor for tags on pocket articles. 

## How it works?

1. First time you run `repocket`, it will ask for your credentials (_consumer key_ and _access token_). After that, it will read saved credentials every time you run it.
2. It downloads *N* newest items from your Pocket account.
3. Every downloaded item is matched against set of rules, each of them associated with a set of tags.
4. If there is a match, `repocket` will add those tags and mark item as modified.
5. If there is one or more modified items, it will commit changes to the server.
6. Happy reading!

## Usage

    repocket (--process-all | --dry-run | --count <count>)


Available options:

- `--process-all` - download and process _all_ stored; 
- `--dry-run` - changed items won't be commited to server;
- `--count <count>` - specify number of newest items to process (default: 25).


## Rule syntax

### Basic syntax

Rules are read from 'rules' section of YAML file located at `~/.repocket.yml`.

Each rule is a map, containing two keys:

- **rule** - regexp, which will be matched against item's URL;
- **tags** - list of tags that will be added to item on match.

Example:

    - rule: .*github\.com.*
      tags: [programming, github, coding]
    - rule: .*blog\.*
      tags: [blog]

If there is no rules specified in YAML file, two rules above are used and then saved to `repocket.yml`.

### Dynamic tags

You can also generate individual tags using regex named groups. For each of the specified tags will be formatted using standard `.format()` [substitution syntax](https://docs.python.org/2/library/string.html#format-examples).

Example:

    - rule: .*github\.com/([a-z0-9]+)/.*
      tags: [programming, github, '{0}']

Result:

     Title:	lensvol/repocket
     URL:	https://github.com/lensvol/repocket
     Added tags:	github, programming, lensvol